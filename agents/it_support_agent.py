"""
AGENTS/IT_SUPPORT_AGENT.PY
===========================
IT Support Agent — uses ChromaDB knowledge base + GPT-4o-mini.
Auto-creates IT tickets in SQLite.
"""
import os

def _get_llm():
    from langchain_openai import ChatOpenAI
    from config import OPENAI_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

IT_KEYWORDS = [
    "computer","laptop","wifi","internet","password","login","software",
    "install","error","crash","slow","printer","network","screen","keyboard",
    "mouse","virus","update","windows","system","restart","freeze","blue screen",
    "not working","broken","connection","vpn","access","reset","boot","driver",
    "device","hardware","monitor","usb","teams","zoom","outlook","email"
]

def detect_it_issue(text: str):
    t = text.lower()
    matched = [kw for kw in IT_KEYWORDS if kw in t]
    return len(matched) > 0, matched

def solve_it_problem(state: dict) -> dict:
    problem   = state.get("it_problem", "")
    user_name = state.get("user_name", "User")
    is_it, matched = detect_it_issue(problem)

    if not is_it and problem.strip():
        state["it_solution"] = "⚠️ This doesn't appear to be an IT issue. Please use the correct agent tab."
        state["it_handled"]  = False
        return state

    # Search ChromaDB knowledge base first
    kb_context = ""
    try:
        from database.vector_db import semantic_search
        hits = semantic_search(problem, collection_name="it_knowledge", top_k=3)
        if hits:
            kb_context = "\n\n".join([f"Past solution: {h['text']}" for h in hits[:2]])
    except Exception:
        pass

    try:
        llm    = _get_llm()
        kb_sec = f"\n\nKnowledge Base Reference:\n{kb_context}" if kb_context else ""
        prompt = f"""You are a professional IT Support Agent.

Employee "{user_name}" reports: "{problem}"
Detected keywords: {', '.join(matched) if matched else 'general IT issue'}{kb_sec}

Provide:
1. **Diagnosis** (1-2 sentences)
2. **Step-by-step Solution** (numbered, clear)
3. **Prevention Tip** (1 sentence)
4. If hardware repair needed: "Contact IT dept at ext. 100"

Be friendly, professional, concise."""

        response = llm.invoke(prompt)
        state["it_solution"] = response.content
        state["it_handled"]  = True

        # Save ticket to DB
        try:
            from database.sqlite_db import log_it_ticket, log_agent
            tid = log_it_ticket(user_name, problem, response.content)
            state["ticket_id"] = tid
            log_agent("IT Support Agent", "solve_problem", problem, response.content)
        except Exception:
            pass

    except Exception as e:
        state["it_solution"] = f"❌ Error: {e}. Check OPENAI_API_KEY in config.py."
        state["it_handled"]  = False

    return state
