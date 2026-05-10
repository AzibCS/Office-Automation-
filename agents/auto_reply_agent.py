"""
AGENTS/AUTO_REPLY_AGENT.PY
===========================
Generates intelligent AI replies to incoming emails.
"""

import os


def _get_llm():
    from langchain_openai import ChatOpenAI
    from config import OPENAI_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.3)


def generate_reply(state: dict) -> dict:
    """LangGraph node: generate a reply to an email."""
    email_content = state.get("email_content", "")
    sender_name   = state.get("sender_name", "Sir/Madam")

    try:
        llm = _get_llm()
        prompt = f"""You are a professional email assistant for an office.

You received an email from {sender_name}:
"{email_content}"

Write a polite, professional, and helpful reply.
- Keep it concise (3-5 sentences)
- Address the sender by name
- Acknowledge their message
- Answer any questions if possible
- Close professionally

Your reply:"""

        response = llm.invoke(prompt)
        state["body"] = response.content

    except Exception as e:
        state["body"] = f"Thank you for your email. We will get back to you shortly.\n\n[Auto-reply error: {e}]"

    return state
