"""
DATABASE/SQLITE_DB.PY
======================
SQLite + SQLAlchemy ORM — All tables for the FYP system.

Tables:
  users, tasks, agent_logs, messages, emails,
  candidates, hr_queries, finance_records,
  documents_meta, it_tickets, notifications, whatsapp_logs
"""

import os
import sys
import json
import time
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from sqlalchemy import (
    create_engine, Column, Integer, String, Text,
    Float, DateTime, Boolean, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import StaticPool

Base = declarative_base()


# ── Models ────────────────────────────────────────────────────────────────────

class TaskLog(Base):
    __tablename__ = "tasks"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    timestamp   = Column(DateTime, default=datetime.utcnow)
    user_name   = Column(String(100))
    user_role   = Column(String(50))
    user_input  = Column(Text)
    agents_used = Column(String(200))
    response    = Column(Text)
    elapsed_ms  = Column(Integer, default=0)
    source      = Column(String(50), default="ui")  # ui | whatsapp | api


class AgentLog(Base):
    __tablename__ = "agent_logs"
    id         = Column(Integer, primary_key=True, autoincrement=True)
    timestamp  = Column(DateTime, default=datetime.utcnow)
    agent_name = Column(String(100))
    action     = Column(String(200))
    input_data = Column(Text)
    output     = Column(Text)
    success    = Column(Boolean, default=True)
    elapsed_ms = Column(Integer, default=0)


class MessageLog(Base):
    __tablename__ = "messages"
    id        = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    msg_id    = Column(String(20))
    sender    = Column(String(100))
    receiver  = Column(String(100))
    topic     = Column(String(50))
    payload   = Column(Text)
    status    = Column(String(20), default="pending")


class EmailLog(Base):
    __tablename__ = "emails"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    timestamp   = Column(DateTime, default=datetime.utcnow)
    direction   = Column(String(10))   # sent | received
    from_addr   = Column(String(200))
    to_addr     = Column(String(200))
    subject     = Column(String(500))
    body        = Column(Text)
    status      = Column(String(20), default="sent")
    auto_reply  = Column(Boolean, default=False)


class Candidate(Base):
    __tablename__ = "candidates"
    id             = Column(Integer, primary_key=True, autoincrement=True)
    timestamp      = Column(DateTime, default=datetime.utcnow)
    name           = Column(String(200))
    job_title      = Column(String(200))
    score          = Column(Integer, default=0)
    recommendation = Column(String(100))
    strengths      = Column(Text)
    weaknesses     = Column(Text)
    summary        = Column(Text)
    cv_filename    = Column(String(200))
    status         = Column(String(50), default="screened")


class HRQuery(Base):
    __tablename__ = "hr_queries"
    id        = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_name = Column(String(100))
    action    = Column(String(100))
    question  = Column(Text)
    answer    = Column(Text)


class FinanceRecord(Base):
    __tablename__ = "finance_records"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    timestamp   = Column(DateTime, default=datetime.utcnow)
    user_name   = Column(String(100))
    action      = Column(String(100))
    input_data  = Column(Text)
    result      = Column(Text)
    total_amount= Column(Float, default=0.0)


class DocumentMeta(Base):
    __tablename__ = "documents_meta"
    id           = Column(Integer, primary_key=True, autoincrement=True)
    timestamp    = Column(DateTime, default=datetime.utcnow)
    file_name    = Column(String(500))
    file_id      = Column(String(200))
    source       = Column(String(50), default="drive")
    content_len  = Column(Integer, default=0)
    summary      = Column(Text)
    doc_type     = Column(String(100))
    embedded     = Column(Boolean, default=False)


class ITTicket(Base):
    __tablename__ = "it_tickets"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    timestamp   = Column(DateTime, default=datetime.utcnow)
    ticket_id   = Column(String(20))
    user_name   = Column(String(100))
    problem     = Column(Text)
    solution    = Column(Text)
    status      = Column(String(30), default="resolved")
    priority    = Column(String(20), default="normal")


class Notification(Base):
    __tablename__ = "notifications"
    id        = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    title     = Column(String(200))
    message   = Column(Text)
    level     = Column(String(20), default="info")   # info | warning | error | success
    read      = Column(Boolean, default=False)
    agent     = Column(String(100))


class WhatsAppLog(Base):
    __tablename__ = "whatsapp_logs"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    timestamp   = Column(DateTime, default=datetime.utcnow)
    direction   = Column(String(10))   # inbound | outbound
    from_number = Column(String(50))
    to_number   = Column(String(50))
    message     = Column(Text)
    agents_used = Column(String(200))
    status      = Column(String(20), default="sent")


# ── Engine & Session ──────────────────────────────────────────────────────────

_engine  = None
_Session = None


def get_engine():
    global _engine
    if _engine is None:
        from config import DB_PATH
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        _engine = create_engine(
            f"sqlite:///{DB_PATH}",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(_engine)
    return _engine


def get_session() -> Session:
    global _Session
    if _Session is None:
        _Session = sessionmaker(bind=get_engine())
    return _Session()


def init_db():
    """Initialize DB — creates all tables if not exist."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    return True


# ── Helper Functions ──────────────────────────────────────────────────────────

def log_task(user_name: str, user_role: str, user_input: str,
             agents_used: list, response: str, elapsed_ms: int = 0,
             source: str = "ui"):
    try:
        s = get_session()
        s.add(TaskLog(
            user_name=user_name, user_role=user_role,
            user_input=user_input,
            agents_used=", ".join(agents_used),
            response=response, elapsed_ms=elapsed_ms, source=source,
        ))
        s.commit()
        s.close()
    except Exception:
        pass


def log_agent(agent_name: str, action: str, input_data: str,
              output: str, success: bool = True, elapsed_ms: int = 0):
    try:
        s = get_session()
        s.add(AgentLog(
            agent_name=agent_name, action=action,
            input_data=str(input_data)[:2000],
            output=str(output)[:3000],
            success=success, elapsed_ms=elapsed_ms,
        ))
        s.commit()
        s.close()
    except Exception:
        pass


def log_email(direction: str, from_addr: str, to_addr: str,
              subject: str, body: str, auto_reply: bool = False):
    try:
        s = get_session()
        s.add(EmailLog(
            direction=direction, from_addr=from_addr,
            to_addr=to_addr, subject=subject,
            body=str(body)[:2000], auto_reply=auto_reply,
        ))
        s.commit()
        s.close()
    except Exception:
        pass


def log_candidate(name: str, job_title: str, score: int,
                  recommendation: str, strengths: list,
                  weaknesses: list, summary: str, cv_filename: str = ""):
    try:
        s = get_session()
        s.add(Candidate(
            name=name, job_title=job_title, score=score,
            recommendation=recommendation,
            strengths=", ".join(strengths),
            weaknesses=", ".join(weaknesses),
            summary=summary, cv_filename=cv_filename,
        ))
        s.commit()
        s.close()
    except Exception:
        pass


def log_it_ticket(user_name: str, problem: str, solution: str,
                  priority: str = "normal"):
    try:
        s    = get_session()
        count = s.query(ITTicket).count()
        tid   = f"IT-{datetime.now().strftime('%Y%m%d')}-{count+1:04d}"
        s.add(ITTicket(
            ticket_id=tid, user_name=user_name,
            problem=problem, solution=solution, priority=priority,
        ))
        s.commit()
        s.close()
        return tid
    except Exception:
        return "IT-ERROR"


def log_finance(user_name: str, action: str, input_data: str,
                result: str, total_amount: float = 0.0):
    try:
        s = get_session()
        s.add(FinanceRecord(
            user_name=user_name, action=action,
            input_data=str(input_data)[:2000],
            result=str(result)[:3000],
            total_amount=total_amount,
        ))
        s.commit()
        s.close()
    except Exception:
        pass


def log_whatsapp(direction: str, from_number: str, to_number: str,
                 message: str, agents_used: list = None, status: str = "sent"):
    try:
        s = get_session()
        s.add(WhatsAppLog(
            direction=direction, from_number=from_number,
            to_number=to_number, message=message,
            agents_used=", ".join(agents_used or []),
            status=status,
        ))
        s.commit()
        s.close()
    except Exception:
        pass


def add_notification(title: str, message: str, level: str = "info", agent: str = "System"):
    try:
        s = get_session()
        s.add(Notification(title=title, message=message, level=level, agent=agent))
        s.commit()
        s.close()
    except Exception:
        pass


def get_dashboard_stats() -> dict:
    """Get real stats from DB for dashboard."""
    try:
        s = get_session()
        stats = {
            "total_tasks":       s.query(TaskLog).count(),
            "total_emails":      s.query(EmailLog).count(),
            "total_candidates":  s.query(Candidate).count(),
            "total_it_tickets":  s.query(ITTicket).count(),
            "total_finance":     s.query(FinanceRecord).count(),
            "total_whatsapp":    s.query(WhatsAppLog).count(),
            "unread_notifs":     s.query(Notification).filter_by(read=False).count(),
            "recent_tasks":      [],
            "recent_tickets":    [],
            "agent_usage":       {},
        }
        # Recent tasks
        recent = s.query(TaskLog).order_by(TaskLog.timestamp.desc()).limit(5).all()
        for t in recent:
            stats["recent_tasks"].append({
                "time":    t.timestamp.strftime("%H:%M"),
                "user":    t.user_name,
                "agents":  t.agents_used,
                "input":   t.user_input[:60],
                "elapsed": t.elapsed_ms,
            })
        # Agent usage counts
        from sqlalchemy import func
        rows = s.query(AgentLog.agent_name, func.count(AgentLog.id))\
                .group_by(AgentLog.agent_name).all()
        for name, cnt in rows:
            stats["agent_usage"][name] = cnt

        s.close()
        return stats
    except Exception as e:
        return {"error": str(e), "total_tasks": 0, "total_emails": 0,
                "total_candidates": 0, "total_it_tickets": 0,
                "total_finance": 0, "total_whatsapp": 0,
                "unread_notifs": 0, "recent_tasks": [],
                "recent_tickets": [], "agent_usage": {}}


def get_task_history(limit: int = 50) -> list:
    try:
        s = get_session()
        rows = s.query(TaskLog).order_by(TaskLog.timestamp.desc()).limit(limit).all()
        result = []
        for r in rows:
            result.append({
                "id":        r.id,
                "time":      r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "user":      r.user_name,
                "role":      r.user_role,
                "input":     r.user_input,
                "agents":    r.agents_used,
                "response":  r.response,
                "elapsed":   r.elapsed_ms,
                "source":    r.source,
            })
        s.close()
        return result
    except Exception:
        return []


def get_notifications(unread_only: bool = False) -> list:
    try:
        s = get_session()
        q = s.query(Notification).order_by(Notification.timestamp.desc())
        if unread_only:
            q = q.filter_by(read=False)
        rows = q.limit(20).all()
        result = [{"id": r.id, "time": r.timestamp.strftime("%H:%M"),
                   "title": r.title, "message": r.message,
                   "level": r.level, "agent": r.agent} for r in rows]
        s.close()
        return result
    except Exception:
        return []


def mark_notifications_read():
    try:
        s = get_session()
        s.query(Notification).filter_by(read=False).update({"read": True})
        s.commit()
        s.close()
    except Exception:
        pass
