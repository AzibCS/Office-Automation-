"""
ORCHESTRATOR/ORCHESTRATOR_BRAIN.PY
====================================
Central Orchestrator — Multi-Agent System Brain

Architecture:
┌──────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                           │
│                                                               │
│   User Request → [Intent Detection] → [Agent Router]         │
│                                          │                    │
│          ┌───────────────────────────────┤                    │
│          ▼       ▼        ▼       ▼      ▼                    │
│       IT Agent  Email  HR Agent  Finance  Documents           │
│          │       │        │       │         │                 │
│          └───────┴────────┴───────┴─────────┘                 │
│                       Message Queue (A2A)                     │
│                       MCP Server                              │
└──────────────────────────────────────────────────────────────┘

A2A Protocol:
  - Orchestrator publishes tasks to Message Queue
  - Sub-agents subscribe and process their tasks
  - Sub-agents can collaborate by publishing to each other
  - All messages are tracked in history
"""

import os
import time
import threading
from typing import Optional
from langchain_openai import ChatOpenAI

from config import OPENAI_API_KEY, AGENT_IDS
from message_queue.queue import message_queue, A2AMessage


os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# ── LLM for intent detection ──────────────────────────────────────────────────

def _get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ── Intent detection ──────────────────────────────────────────────────────────

EMAIL_KEYWORDS = [
    "email", "mail", "send", "reply", "inbox", "message", "gmail",
    "smtp", "imap", "subject", "recipient", "forward", "compose",
    "write to", "contact", "notify"
]

IT_KEYWORDS = [
    "computer", "laptop", "wifi", "internet", "password", "login",
    "software", "install", "error", "crash", "slow", "printer",
    "network", "screen", "keyboard", "virus", "update", "windows",
    "system", "restart", "freeze", "not working", "broken", "connection",
    "vpn", "access", "reset", "boot", "driver", "it support", "technical",
    "device", "hardware", "monitor", "cable", "usb", "mouse"
]

HR_KEYWORDS = [
    "hr", "hire", "recruit", "cv", "resume", "candidate", "interview",
    "onboard", "onboarding", "employee", "salary", "leave", "policy",
    "payroll", "job description", "staff", "screening", "shortlist",
    "performance", "appraisal", "human resources", "vacancy", "position"
]

FINANCE_KEYWORDS = [
    "finance", "financial", "expense", "budget", "invoice", "payment",
    "revenue", "cost", "profit", "loss", "tax", "account", "balance",
    "ledger", "cash flow", "report", "spending", "pkr", "usd", "money",
    "salary", "payable", "receivable", "quarterly", "fiscal", "audit"
]

DOCS_KEYWORDS = [
    "document", "file", "pdf", "drive", "google drive", "folder",
    "search document", "find file", "summarize", "contract", "policy",
    "manual", "report", "doc", "read file", "extract", "compare doc"
]


def detect_intent(user_message: str) -> list:
    """
    Detect which agents should handle the message.
    Returns list of agent types.
    """
    msg = user_message.lower()

    matches = []
    if any(kw in msg for kw in EMAIL_KEYWORDS):
        matches.append("email")
    if any(kw in msg for kw in IT_KEYWORDS):
        matches.append("it_support")
    if any(kw in msg for kw in HR_KEYWORDS):
        matches.append("hr")
    if any(kw in msg for kw in FINANCE_KEYWORDS):
        matches.append("finance")
    if any(kw in msg for kw in DOCS_KEYWORDS):
        matches.append("documents")

    # Default fallback
    if not matches:
        matches.append("it_support")

    return matches


def detect_intent_llm(user_message: str) -> list:
    """
    LLM-powered intent detection for complex/ambiguous messages.
    Falls back gracefully.
    """
    try:
        llm = _get_llm()
        prompt = f"""You are an intent detector for an office automation system.

User message: "{user_message}"

Available agents:
- it_support: IT problems, computer issues, software/hardware
- email: send/read/reply/search emails
- hr: CV screening, hiring, onboarding, HR policy, employees
- finance: expenses, invoices, budgets, financial reports
- documents: Google Drive files, PDFs, document search/summary

Respond with ONLY a JSON array of agent names that should handle this request.
Examples:
  "my laptop is slow" → ["it_support"]
  "email Ahmed and check HR policy" → ["email", "hr"]
  "analyze expenses and generate invoice" → ["finance"]

JSON array only, no explanation:"""

        resp = llm.invoke(prompt)
        text = resp.content.strip().strip("```json").strip("```").strip()
        import json
        agents = json.loads(text)
        if isinstance(agents, list) and agents:
            return agents
    except Exception:
        pass

    return detect_intent(user_message)  # fallback to keyword


# ── Orchestrator Core ─────────────────────────────────────────────────────────

class Orchestrator:
    """
    Central orchestrator that:
    1. Receives user requests
    2. Detects intent (which agents needed)
    3. Publishes tasks to Message Queue (A2A)
    4. Collects responses from agents
    5. Merges and returns final answer
    """

    def __init__(self):
        self.agent_id   = AGENT_IDS["orchestrator"]
        self.mq         = message_queue
        self._lock      = threading.Lock()
        self._responses = {}  # task_id -> response

    def route(self, user_message: str, user_name: str = "User",
              use_llm_intent: bool = True) -> dict:
        """
        Main entry point.
        Returns:
          {
            "agents_used":  ["it_support", ...],
            "responses":    {"it_support": "...", ...},
            "final_answer": "merged response",
            "task_ids":     {"it_support": "msg-id", ...},
            "mq_messages":  [list of all queue messages],
          }
        """
        start_time = time.time()

        # 1. Detect which agents to use
        if use_llm_intent:
            agents = detect_intent_llm(user_message)
        else:
            agents = detect_intent(user_message)

        result = {
            "agents_used":  agents,
            "responses":    {},
            "final_answer": "",
            "task_ids":     {},
            "elapsed_ms":   0,
            "mq_messages":  [],
        }

        # 2. Publish task to Message Queue for each agent (A2A dispatch)
        task_ids = {}
        for agent_type in agents:
            agent_receiver = AGENT_IDS.get(agent_type, f"agent-{agent_type}-001")
            msg_id = self.mq.send(
                sender=self.agent_id,
                receiver=agent_receiver,
                topic="task",
                payload={
                    "user_message": user_message,
                    "user_name":    user_name,
                    "agent_type":   agent_type,
                },
                priority=2,
            )
            task_ids[agent_type] = msg_id

        result["task_ids"] = task_ids

        # 3. Execute agents (invoke their LangGraphs directly)
        responses = {}
        for agent_type in agents:
            try:
                resp = self._invoke_agent(agent_type, user_message, user_name)
                responses[agent_type] = resp

                # Publish result back to queue (A2A result message)
                self.mq.send(
                    sender=AGENT_IDS.get(agent_type, agent_type),
                    receiver=self.agent_id,
                    topic="result",
                    payload={"response": resp, "agent_type": agent_type},
                    reply_to=task_ids.get(agent_type),
                )
            except Exception as e:
                responses[agent_type] = f"❌ Agent error: {e}"

        result["responses"] = responses

        # 4. Merge responses
        if len(responses) == 1:
            result["final_answer"] = list(responses.values())[0]
        else:
            parts = []
            agent_labels = {
                "it_support": "💻 IT Support",
                "email":      "📧 Email Agent",
                "hr":         "🧑‍💼 HR Agent",
                "finance":    "💰 Finance Agent",
                "documents":  "📂 Documents Agent",
            }
            for agent_type, resp in responses.items():
                label = agent_labels.get(agent_type, agent_type.upper())
                parts.append(f"**{label}:**\n{resp}")
            result["final_answer"] = "\n\n---\n\n".join(parts)

        result["elapsed_ms"]  = round((time.time() - start_time) * 1000)
        result["mq_messages"] = self.mq.get_all_messages_for_display(limit=30)

        return result

    def _invoke_agent(self, agent_type: str, user_message: str, user_name: str) -> str:
        """
        Invoke the correct LangGraph agent.
        This is the A2A execution layer.
        """
        if agent_type == "it_support":
            from graph.it_graph import it_graph
            state  = {"user_name": user_name, "it_problem": user_message}
            result = it_graph.invoke(state)
            return result.get("it_solution", "No solution returned.")

        elif agent_type == "email":
            from agents.auto_reply_agent import generate_reply
            state  = {"email_content": user_message, "sender_name": user_name, "sender_email": ""}
            result = generate_reply(state)
            return result.get("body", "No reply generated.")

        elif agent_type == "hr":
            from graph.hr_graph import hr_graph
            state  = {"action": "hr_query", "query": user_message, "user_name": user_name}
            result = hr_graph.invoke(state)
            return result.get("output", "No HR response.")

        elif agent_type == "finance":
            from graph.finance_graph import finance_graph
            state  = {"action": "query", "question": user_message, "user_name": user_name}
            result = finance_graph.invoke(state)
            return result.get("output", "No finance response.")

        elif agent_type == "documents":
            from graph.documents_graph import documents_graph
            state  = {"action": "qa", "query": user_message, "user_name": user_name, "documents": []}
            result = documents_graph.invoke(state)
            return result.get("output", "No documents response.")

        else:
            return f"Unknown agent type: {agent_type}"

    def get_queue_status(self) -> dict:
        return {
            "stats":    self.mq.get_stats(),
            "messages": self.mq.get_all_messages_for_display(limit=50),
        }

    def broadcast(self, message: str, sender_name: str = "Orchestrator"):
        """Broadcast a message to all agents."""
        self.mq.send(
            sender=self.agent_id,
            receiver="broadcast",
            topic="broadcast",
            payload={"message": message, "from": sender_name},
        )


# ── Singleton ─────────────────────────────────────────────────────────────────

orchestrator = Orchestrator()


# ── Legacy helper (backward compat) ──────────────────────────────────────────

def route_to_agent(user_message: str, user_name: str = "User") -> dict:
    """Legacy wrapper kept for backward compatibility."""
    result = orchestrator.route(user_message, user_name)
    return {
        "user_message": user_message,
        "agent_used":   ", ".join(result["agents_used"]),
        "response":     result["final_answer"],
        "agents_used":  result["agents_used"],
        "responses":    result["responses"],
    }
