"""
TOOLS/GMAIL_SEND.PY
====================
Send email via Gmail SMTP.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(state: dict) -> dict:
    """
    Send an email.
    state must contain: recipient, subject, body
    """
    from config import GMAIL_EMAIL, GMAIL_APP_PASSWORD

    recipient = state.get("recipient", "")
    subject   = state.get("subject", "No Subject")
    body      = state.get("body", "")

    if not recipient:
        state["send_status"] = "❌ No recipient specified."
        return state

    try:
        msg               = MIMEMultipart("alternative")
        msg["Subject"]    = subject
        msg["From"]       = GMAIL_EMAIL
        msg["To"]         = recipient
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        state["send_status"] = f"✅ Email sent to {recipient}"

    except Exception as e:
        state["send_status"] = f"❌ Failed to send email: {e}"

    return state
