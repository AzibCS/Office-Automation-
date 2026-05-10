"""
UI/APP.PY — Office Automation Agents Pro v7.0 — FYP FINAL
==========================================================
Tabs: Login | Dashboard | Orchestrator | IT | Email | HR | Finance | Documents | WhatsApp | History
"""
import sys, os, time, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st

st.set_page_config(
    page_title="Office Automation Agents Pro",
    layout="wide", page_icon="🏢",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; }
.main { padding-top: 0.3rem; background: #f8fafc; }
.stApp { background: #f8fafc; }

/* Login card */
.login-wrap { display:flex; justify-content:center; align-items:center; min-height:80vh; }
.login-card {
    background: white; border-radius: 20px; padding: 40px 48px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.12); max-width: 420px; width:100%;
    border: 1px solid #e2e8f0;
}
.login-logo { text-align:center; font-size:48px; margin-bottom:8px; }
.login-title { text-align:center; font-size:24px; font-weight:800; color:#1e293b; margin-bottom:4px; }
.login-sub { text-align:center; font-size:13px; color:#64748b; margin-bottom:28px; }

/* Header */
.main-header {
    background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #0f172a 100%);
    color: white; padding: 14px 24px; border-radius: 14px; margin-bottom: 16px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.header-title { font-size:22px; font-weight:800; letter-spacing:-0.3px; }
.header-sub { font-size:11px; color:#94a3b8; margin-top:2px; }

/* Metric cards */
.metric-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:16px; }
.metric-card {
    background:white; border:1px solid #e2e8f0; border-radius:14px;
    padding:16px 20px; box-shadow:0 2px 8px rgba(0,0,0,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(0,0,0,0.1); }
.metric-icon { font-size:28px; margin-bottom:6px; }
.metric-num { font-size:32px; font-weight:800; color:#1e293b; line-height:1; }
.metric-label { font-size:12px; color:#64748b; margin-top:4px; font-weight:500; }
.metric-delta { font-size:11px; color:#16a34a; font-weight:600; }

/* Agent cards */
.agent-status-card {
    background:white; border:1px solid #e2e8f0; border-radius:12px;
    padding:14px 18px; display:flex; align-items:center; gap:12px;
    box-shadow:0 2px 6px rgba(0,0,0,0.05);
}
.agent-dot { width:10px; height:10px; border-radius:50%; background:#16a34a; flex-shrink:0; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }

/* Response boxes */
.resp-box {
    background:white; border-left:4px solid #2563eb; border-radius:0 12px 12px 0;
    padding:18px 22px; margin:10px 0; box-shadow:0 2px 8px rgba(0,0,0,0.07);
    line-height:1.7; white-space:pre-wrap;
}
.resp-green  { border-left-color:#16a34a; }
.resp-purple { border-left-color:#7c3aed; }
.resp-orange { border-left-color:#ea580c; }
.resp-teal   { border-left-color:#0d9488; }
.resp-red    { border-left-color:#dc2626; }

/* Chat */
.chat-user  { background:linear-gradient(135deg,#2563eb,#1d4ed8); color:white; padding:10px 16px; border-radius:18px 18px 4px 18px; margin:6px 0 6px auto; max-width:75%; display:inline-block; float:right; clear:both; font-size:14px; }
.chat-agent { background:white; color:#1e293b; padding:12px 16px; border-radius:18px 18px 18px 4px; margin:6px 0; max-width:80%; display:inline-block; float:left; clear:both; font-size:14px; border:1px solid #e2e8f0; box-shadow:0 2px 6px rgba(0,0,0,0.06); line-height:1.6; white-space:pre-wrap; }
.chat-wrap  { overflow:hidden; margin-bottom:6px; }

/* Sections */
.sec-hdr {
    background:linear-gradient(90deg,#1e293b,#334155); color:white;
    padding:10px 18px; border-radius:10px; margin:14px 0 10px 0;
    font-weight:700; font-size:14px; letter-spacing:0.2px;
}
.sec-blue   { background:linear-gradient(90deg,#1d4ed8,#3b82f6) !important; }
.sec-green  { background:linear-gradient(90deg,#15803d,#22c55e) !important; }
.sec-purple { background:linear-gradient(90deg,#6d28d9,#a855f7) !important; }
.sec-teal   { background:linear-gradient(90deg,#0f766e,#14b8a6) !important; }
.sec-orange { background:linear-gradient(90deg,#c2410c,#f97316) !important; }
.sec-wa     { background:linear-gradient(90deg,#15803d,#16a34a) !important; }

/* Badges */
.badge { padding:3px 10px; border-radius:20px; font-size:11px; font-weight:700; display:inline-block; }
.badge-green  { background:#dcfce7; color:#15803d; }
.badge-blue   { background:#dbeafe; color:#1d4ed8; }
.badge-purple { background:#f3e8ff; color:#6d28d9; }
.badge-orange { background:#ffedd5; color:#c2410c; }
.badge-red    { background:#fee2e2; color:#dc2626; }
.badge-yellow { background:#fef9c3; color:#854d0e; }
.badge-mcp    { background:#0d9488; color:white; }
.badge-a2a    { background:#7c3aed; color:white; }
.badge-wa     { background:#16a34a; color:white; }

/* Queue messages */
.qmsg { background:white; border:1px solid #e2e8f0; border-radius:8px; padding:8px 12px; margin-bottom:5px; font-size:12px; font-family:monospace; }
.qmsg-task   { border-left:3px solid #2563eb; }
.qmsg-result { border-left:3px solid #16a34a; }
.qmsg-status { border-left:3px solid #f59e0b; }
.qmsg-broadcast { border-left:3px solid #7c3aed; }

/* Candidate */
.cand-card { background:white; border:1px solid #e2e8f0; border-radius:12px; padding:16px; margin-bottom:10px; box-shadow:0 2px 6px rgba(0,0,0,0.05); }
.score-bar  { height:8px; border-radius:4px; background:#e2e8f0; margin:8px 0 4px 0; }
.score-fill { height:8px; border-radius:4px; }

/* WhatsApp */
.wa-bubble-out { background:#dcf8c6; border-radius:18px 4px 18px 18px; padding:10px 14px; margin:6px 0 6px auto; max-width:75%; display:inline-block; float:right; clear:both; font-size:14px; }
.wa-bubble-in  { background:white; border-radius:4px 18px 18px 18px; padding:10px 14px; margin:6px 0; max-width:75%; display:inline-block; float:left; clear:both; font-size:14px; border:1px solid #e2e8f0; }

/* History table */
.hist-row { background:white; border:1px solid #e2e8f0; border-radius:8px; padding:10px 14px; margin-bottom:6px; font-size:13px; }

/* Notification */
.notif { border-radius:10px; padding:10px 14px; margin-bottom:6px; font-size:13px; }
.notif-info    { background:#eff6ff; border-left:4px solid #2563eb; }
.notif-success { background:#f0fdf4; border-left:4px solid #16a34a; }
.notif-warning { background:#fffbeb; border-left:4px solid #f59e0b; }
.notif-error   { background:#fef2f2; border-left:4px solid #dc2626; }

/* A2A flow */
.a2a-flow { background:#0f172a; color:#e2e8f0; border-radius:12px; padding:16px 20px; font-family:monospace; font-size:12px; line-height:2; }
.a2a-arrow { color:#22c55e; }
.a2a-agent { color:#60a5fa; font-weight:700; }
.a2a-topic { color:#fbbf24; }

div[data-testid="stForm"] { border:none !important; padding:0 !important; }
</style>""", unsafe_allow_html=True)

# ── Session defaults ──────────────────────────────────────────────────────────
_defs = {
    "logged_in": False, "username": "", "user_role": "", "user_name": "",
    "orch_chat": [], "coord_chat": [], "docs_chat": [], "wa_chat": [],
    "pending_email": None, "monitor_log": [], "hr_results": None,
    "uploaded_cvs": [], "drive_documents": [], "mcp_running": False,
    "system_start": time.time(), "wa_log": [],
}
for k, v in _defs.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── DB init ───────────────────────────────────────────────────────────────────
try:
    from database.sqlite_db import init_db
    init_db()
except Exception:
    pass

# ── MCP auto-start ────────────────────────────────────────────────────────────
try:
    from mcp_server import start_mcp_server, is_mcp_running
    if not is_mcp_running():
        start_mcp_server()
    st.session_state.mcp_running = True
except Exception:
    st.session_state.mcp_running = False

# ── Monitor logs ──────────────────────────────────────────────────────────────
try:
    from tools.gmail_auto_reply_monitor import get_pending_logs, is_running, start_monitor, stop_monitor
    for lg in get_pending_logs():
        st.session_state.monitor_log.append(lg)
except Exception:
    def is_running(): return False
    def start_monitor(): pass
    def stop_monitor(): pass

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div style="display:flex;justify-content:center;align-items:center;min-height:85vh">
    <div style="background:white;border-radius:20px;padding:44px 52px;box-shadow:0 20px 60px rgba(0,0,0,0.13);max-width:420px;width:100%;border:1px solid #e2e8f0">
        <div style="text-align:center;font-size:52px;margin-bottom:8px">🏢</div>
        <div style="text-align:center;font-size:26px;font-weight:800;color:#1e293b;margin-bottom:4px">Office Automation Pro</div>
        <div style="text-align:center;font-size:13px;color:#64748b;margin-bottom:30px">Multi-Agent System · FYP v7.0</div>
    </div></div>""", unsafe_allow_html=True)

    col = st.columns([1,1.6,1])[1]
    with col:
        st.markdown("")
        username = st.text_input("👤 Username", placeholder="admin / hr / finance / it / demo")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
        if st.button("🚀 Sign In", use_container_width=True):
            from config import USERS
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in  = True
                st.session_state.username   = username
                st.session_state.user_role  = USERS[username]["role"]
                st.session_state.user_name  = USERS[username]["name"]
                try:
                    from database.sqlite_db import add_notification
                    add_notification(f"{USERS[username]['name']} logged in", f"Role: {USERS[username]['role']}", "info", "System")
                except Exception:
                    pass
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        st.markdown("""<div style="background:#f8fafc;border-radius:10px;padding:12px 16px;margin-top:12px;font-size:12px;color:#64748b">
        <b>Demo credentials:</b><br>
        admin / admin123 &nbsp;|&nbsp; hr / hr123<br>
        finance / finance123 &nbsp;|&nbsp; demo / demo123
        </div>""", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP (after login)
# ══════════════════════════════════════════════════════════════════════════════

# ── Top header ────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([3, 1.5, 1])
with c1:
    mcp_b = "🟢" if st.session_state.mcp_running else "🔴"
    mon_b = "🟢" if is_running() else "🟡"
    st.markdown(f"""
    <div class="main-header">
      <div>
        <div class="header-title">🏢 Office Automation Agents Pro</div>
        <div class="header-sub">LangGraph · OpenAI · MCP · A2A Protocol · ChromaDB · SQLite · WhatsApp</div>
      </div>
      <div style="text-align:right;font-size:12px">
        {mcp_b} MCP &nbsp; {mon_b} Monitor<br>
        <span style="color:#94a3b8">👤 {st.session_state.user_name} ({st.session_state.user_role})</span>
      </div>
    </div>""", unsafe_allow_html=True)
with c3:
    if st.button("🚪 Logout", use_container_width=True):
        for k in ["logged_in","username","user_role","user_name"]:
            st.session_state[k] = "" if k != "logged_in" else False
        st.rerun()

# ── Tabs ──────────────────────────────────────────────────────────────────────
TABS = ["🏠 Dashboard","🤖 Orchestrator","💻 IT Support","📧 Email",
        "🧑‍💼 HR","💰 Finance","📂 Documents","💬 WhatsApp","📋 History"]
tabs = st.tabs(TABS)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    try:
        from database.sqlite_db import get_dashboard_stats, get_notifications
        stats = get_dashboard_stats()
        notifs = get_notifications(unread_only=True)
    except Exception:
        stats = {"total_tasks":0,"total_emails":0,"total_candidates":0,"total_it_tickets":0,
                 "total_finance":0,"total_whatsapp":0,"unread_notifs":0,"recent_tasks":[],
                 "agent_usage":{}}
        notifs = []

    try:
        from database.vector_db import collection_stats
        vdb = collection_stats()
        total_vecs = sum(vdb.values()) if isinstance(vdb, dict) and "error" not in vdb else 0
    except Exception:
        vdb, total_vecs = {}, 0

    # Metrics row
    m = st.columns(6)
    metrics = [
        ("📋","Tasks",stats.get("total_tasks",0),"green"),
        ("📧","Emails",stats.get("total_emails",0),"blue"),
        ("🧑‍💼","Candidates",stats.get("total_candidates",0),"purple"),
        ("💻","IT Tickets",stats.get("total_it_tickets",0),"orange"),
        ("💬","WhatsApp",stats.get("total_whatsapp",0),"wa"),
        ("🧠","Vectors",total_vecs,"teal"),
    ]
    for col, (icon, label, val, color) in zip(m, metrics):
        with col:
            st.markdown(f"""<div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-num">{val}</div>
            <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    c1, c2, c3 = st.columns([1.2, 1.2, 1])

    with c1:
        st.markdown('<div class="sec-hdr sec-blue">🤖 Agent Status</div>', unsafe_allow_html=True)
        agents = [("💻","IT Support Agent","agent-it-001"),("📧","Email Agent","agent-email-001"),
                  ("🧑‍💼","HR Agent","agent-hr-001"),("💰","Finance Agent","agent-finance-001"),
                  ("📂","Documents Agent","agent-docs-001"),("💬","WhatsApp Agent","agent-whatsapp-001"),
                  ("🔄","Auto-Reply","agent-autoreply-001")]
        for icon, name, aid in agents:
            usage = stats.get("agent_usage", {}).get(name, 0)
            st.markdown(f"""<div class="agent-status-card" style="margin-bottom:6px">
            <div class="agent-dot"></div>
            <div style="flex:1"><b style="font-size:13px">{icon} {name}</b><br>
            <span style="font-size:11px;color:#64748b">{aid}</span></div>
            <span class="badge badge-green">{usage} calls</span>
            </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec-hdr">📨 A2A Message Queue</div>', unsafe_allow_html=True)
        try:
            from message_queue import message_queue
            msgs = message_queue.get_all_messages_for_display(limit=8)
            if msgs:
                for msg in msgs:
                    tc = {"task":"qmsg-task","result":"qmsg-result","status":"qmsg-status","broadcast":"qmsg-broadcast"}.get(msg["topic"],"qmsg")
                    st.markdown(f"""<div class="qmsg {tc}">
                    <b>{msg['time']}</b> [{msg['topic'].upper()}]
                    <b>{msg['sender']}</b> → <b>{msg['receiver']}</b><br>
                    <span style="color:#64748b">{msg['preview'][:90]}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.caption("No messages yet. Use Orchestrator tab.")
        except Exception as e:
            st.caption(f"Queue: {e}")

        st.markdown('<div class="sec-hdr">🧠 ChromaDB Collections</div>', unsafe_allow_html=True)
        if vdb and "error" not in vdb:
            for cname, cnt in vdb.items():
                pct = min(100, int(cnt/10))
                st.markdown(f"""<div style="margin-bottom:6px">
                <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:2px">
                <b>{cname}</b><span>{cnt} vectors</span></div>
                <div style="background:#e2e8f0;border-radius:4px;height:6px">
                <div style="background:#7c3aed;width:{pct}%;height:6px;border-radius:4px"></div></div>
                </div>""", unsafe_allow_html=True)
        else:
            st.caption("No collections yet. Load documents or run data loader.")

    with c3:
        st.markdown('<div class="sec-hdr sec-purple">🔔 Notifications</div>', unsafe_allow_html=True)
        if notifs:
            for n in notifs[:6]:
                cls = {"info":"notif-info","success":"notif-success","warning":"notif-warning","error":"notif-error"}.get(n.get("level","info"),"notif-info")
                st.markdown(f"""<div class="notif {cls}">
                <b>{n['title']}</b><br>
                <span style="font-size:11px;color:#64748b">{n['time']} · {n['agent']}</span>
                </div>""", unsafe_allow_html=True)
            if st.button("✅ Mark all read", key="mark_read"):
                from database.sqlite_db import mark_notifications_read
                mark_notifications_read(); st.rerun()
        else:
            st.success("✅ No unread notifications")

        st.markdown('<div class="sec-hdr" style="margin-top:12px">⏱️ System Info</div>', unsafe_allow_html=True)
        uptime = int(time.time() - st.session_state.system_start)
        st.markdown(f"""<div style="background:white;border:1px solid #e2e8f0;border-radius:10px;padding:12px 16px;font-size:13px">
        <b>Uptime:</b> {uptime}s<br>
        <b>MCP:</b> {'🟢 Running :8765' if st.session_state.mcp_running else '🔴 Stopped'}<br>
        <b>Monitor:</b> {'🟢 Active' if is_running() else '🟡 Stopped'}<br>
        <b>DB:</b> 🟢 SQLite Connected<br>
        <b>VectorDB:</b> {'🟢 ChromaDB' if total_vecs>0 else '🟡 Empty'}<br>
        <b>User:</b> {st.session_state.user_name}
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-hdr sec-green" style="margin-top:12px">📊 Data Loader</div>', unsafe_allow_html=True)
        if st.button("🚀 Load All Datasets into ChromaDB", use_container_width=True, key="load_datasets"):
            with st.spinner("Embedding all datasets..."):
                try:
                    from data_loader.loader import load_all_datasets
                    load_all_datasets()
                    st.success("✅ All datasets embedded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    # A2A Architecture
    st.markdown('<div class="sec-hdr" style="margin-top:4px">🏗️ Live A2A Architecture</div>', unsafe_allow_html=True)
    try:
        from message_queue import message_queue
        all_msgs = message_queue.get_all_messages_for_display(limit=6)
        flow_lines = []
        for msg in reversed(all_msgs):
            topic_color = {"task":"#fbbf24","result":"#22c55e","status":"#60a5fa","broadcast":"#a78bfa"}.get(msg["topic"],"#e2e8f0")
            flow_lines.append(f'<span class="a2a-agent">{msg["sender"]}</span> <span class="a2a-arrow">──[<span style="color:{topic_color}">{msg["topic"]}</span>]──►</span> <span class="a2a-agent">{msg["receiver"]}</span> <span style="color:#64748b;font-size:11px">({msg["time"]})</span>')
        flow_html = "<br>".join(flow_lines) if flow_lines else '<span style="color:#64748b">No messages yet. Send a task via Orchestrator to see A2A flow.</span>'
        st.markdown(f'<div class="a2a-flow">{flow_html}</div>', unsafe_allow_html=True)
    except Exception:
        pass

    if st.button("🔄 Refresh Dashboard", key="dash_refresh"):
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ORCHESTRATOR
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="sec-hdr sec-blue">🤖 Orchestrator <span class="badge badge-a2a">A2A</span> <span class="badge badge-mcp">MCP</span></div>', unsafe_allow_html=True)
    st.info("💡 Type anything — the Orchestrator detects intent and routes to the right agent(s) automatically. Try: *'My laptop crashed, email Ahmed about it and check our IT budget'*")

    for entry in st.session_state.orch_chat:
        if entry["role"] == "user":
            st.markdown(f'<div class="chat-wrap"><div class="chat-user">👤 {entry["content"]}</div></div>', unsafe_allow_html=True)
        else:
            badges = " ".join([f'<span class="badge badge-blue">{a}</span>' for a in entry.get("agents",[])])
            ms = entry.get("elapsed_ms", 0)
            st.markdown(f'<div class="chat-wrap"><div class="chat-agent">{badges} <small style="color:#94a3b8">({ms}ms)</small><br><br>{entry["content"]}</div></div>', unsafe_allow_html=True)

    with st.form("orch_form", clear_on_submit=True):
        inp = st.text_area("Your message", placeholder="Describe any task — IT, email, HR, finance, documents...", height=90)
        c1, c2 = st.columns([4,1])
        with c1: sub = st.form_submit_button("📤 Send to Orchestrator", use_container_width=True)
        with c2: use_llm = st.checkbox("LLM Intent", value=True)

    if sub and inp.strip():
        st.session_state.orch_chat.append({"role":"user","content":inp.strip()})
        with st.spinner("🔄 Orchestrator routing..."):
            try:
                from Orchestrator.orchestrator_brain import orchestrator
                result = orchestrator.route(inp.strip(), st.session_state.user_name, use_llm_intent=use_llm)
                st.session_state.orch_chat.append({
                    "role":"agent","content":result["final_answer"],
                    "agents":result["agents_used"],"elapsed_ms":result["elapsed_ms"],
                })
                try:
                    from database.sqlite_db import log_task, add_notification
                    log_task(st.session_state.user_name, st.session_state.user_role,
                             inp.strip(), result["agents_used"], result["final_answer"],
                             result["elapsed_ms"])
                    add_notification("Task completed", f"Agents: {', '.join(result['agents_used'])}", "success", "Orchestrator")
                except Exception:
                    pass
                st.rerun()
            except Exception as e:
                st.error(f"Orchestrator error: {e}")

    with st.expander("📨 Message Queue Live Feed"):
        try:
            from message_queue import message_queue
            for msg in message_queue.get_all_messages_for_display(limit=15):
                tc = {"task":"qmsg-task","result":"qmsg-result","status":"qmsg-status","broadcast":"qmsg-broadcast"}.get(msg["topic"],"qmsg")
                st.markdown(f'<div class="qmsg {tc}"><b>{msg["time"]}</b> [{msg["topic"].upper()}] <b>{msg["sender"]}</b>→<b>{msg["receiver"]}</b> <span style="color:#64748b">{msg["preview"][:100]}</span></div>', unsafe_allow_html=True)
        except Exception:
            st.caption("Queue unavailable")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — IT SUPPORT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="sec-hdr sec-blue">💻 IT Support Agent</div>', unsafe_allow_html=True)
        it_name = st.text_input("Your Name", value=st.session_state.user_name, key="it_name")
        it_prob = st.text_area("Describe Your IT Problem", placeholder="e.g. WiFi not connecting, laptop freezes, can't login...", height=160)
        pri_col, btn_col = st.columns([1,2])
        with pri_col:
            priority = st.selectbox("Priority", ["Normal","High","Urgent"], key="it_pri")
        with btn_col:
            it_btn = st.button("🔍 Get Solution", use_container_width=True, key="it_btn")

        if it_btn and it_prob.strip():
            with st.spinner("🔄 IT Agent analyzing..."):
                try:
                    from graph.it_graph import it_graph
                    result = it_graph.invoke({"user_name":it_name,"it_problem":it_prob})
                    sol = result.get("it_solution","")
                    tid = result.get("ticket_id","")
                    if tid:
                        st.success(f"✅ Ticket created: **{tid}**")
                    if result.get("it_handled"):
                        st.markdown(f'<div class="resp-box">{sol}</div>', unsafe_allow_html=True)
                    else:
                        st.warning(sol)
                except Exception as e:
                    st.error(f"Error: {e}")

    with c2:
        st.markdown('<div class="sec-hdr sec-orange">📬 Auto-Reply Monitor</div>', unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("▶️ Start Monitor", use_container_width=True, disabled=is_running(), key="mon_on"):
                start_monitor(); st.rerun()
        with b2:
            if st.button("⏹️ Stop", use_container_width=True, disabled=not is_running(), key="mon_off"):
                stop_monitor(); st.rerun()

        status_html = '<div style="background:#dcfce7;border:1px solid #16a34a;padding:8px 14px;border-radius:8px;margin:8px 0">🟢 <b>Auto-reply ACTIVE</b></div>' if is_running() else '<div style="background:#fef9c3;border:1px solid #ca8a04;padding:8px 14px;border-radius:8px;margin:8px 0">🟡 <b>Auto-reply OFF</b></div>'
        st.markdown(status_html, unsafe_allow_html=True)

        if st.session_state.monitor_log:
            with st.expander("📋 Activity Log", expanded=True):
                for log in reversed(st.session_state.monitor_log[-20:]):
                    st.caption(log)

        st.markdown('<div class="sec-hdr" style="margin-top:14px">🎫 Recent IT Tickets</div>', unsafe_allow_html=True)
        try:
            from database.sqlite_db import get_session
            from database.sqlite_db import ITTicket
            s    = get_session()
            tix  = s.query(ITTicket).order_by(ITTicket.timestamp.desc()).limit(5).all()
            s.close()
            for t in tix:
                st.markdown(f"""<div class="hist-row">
                <b>{t.ticket_id}</b> &nbsp; <span class="badge badge-{'green' if t.status=='resolved' else 'orange'}">{t.status}</span><br>
                <small style="color:#64748b">{t.user_name} · {t.timestamp.strftime('%Y-%m-%d %H:%M')}</small><br>
                {t.problem[:80]}...</div>""", unsafe_allow_html=True)
        except Exception:
            st.caption("No tickets yet.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — EMAIL
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="sec-hdr sec-teal">📧 Email Coordinator <span class="badge badge-a2a">A2A</span></div>', unsafe_allow_html=True)

    for entry in st.session_state.coord_chat:
        if entry["role"] == "user":
            st.markdown(f'<div class="chat-wrap"><div class="chat-user">👤 {entry["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-wrap"><div class="chat-agent">📧 {entry["content"]}</div></div>', unsafe_allow_html=True)

    if st.session_state.pending_email:
        p = st.session_state.pending_email
        st.warning(f"**📧 Ready to Send**\n\n**To:** {p.get('name','')} `{p.get('email','')}`\n**Subject:** {p.get('subject','')}\n\n{p.get('body','')[:300]}...")
        cy, cn = st.columns(2)
        with cy:
            if st.button("✅ Confirm & Send", use_container_width=True, key="send_yes"):
                try:
                    from tools.gmail_send import send_email
                    from database.sqlite_db import log_email
                    send_email({"recipient":p["email"],"subject":p["subject"],"body":p["body"]})
                    log_email("sent", __import__("config").GMAIL_EMAIL, p["email"], p["subject"], p["body"])
                    st.session_state.coord_chat.append({"role":"agent","content":f"✅ Email sent to {p.get('name',p['email'])}!"})
                    st.session_state.pending_email = None; st.rerun()
                except Exception as e:
                    st.error(f"Send failed: {e}")
        with cn:
            if st.button("❌ Cancel", use_container_width=True, key="send_no"):
                st.session_state.pending_email = None; st.rerun()

    with st.form("coord_form", clear_on_submit=True):
        coord_inp = st.text_area("Message", placeholder="'Email Ahmed about 3pm meeting' or 'Draft reply to Hassan about project delay'", height=80)
        coord_sub = st.form_submit_button("📤 Send", use_container_width=True)

    if coord_sub and coord_inp.strip():
        st.session_state.coord_chat.append({"role":"user","content":coord_inp.strip()})
        with st.spinner("🔄 Processing..."):
            try:
                import re
                from agents.auto_reply_agent import generate_reply
                from tools.email_search import find_email_by_name
                m = re.search(r'(?:email|send|message|contact|write to|notify)\s+([A-Za-z]+)', coord_inp, re.IGNORECASE)
                if m:
                    tname    = m.group(1)
                    contacts = find_email_by_name(tname)
                    if contacts:
                        c        = contacts[0]
                        reply    = generate_reply({"email_content":coord_inp,"sender_name":st.session_state.user_name})
                        st.session_state.pending_email = {"name":c["name"],"email":c["email"],"subject":f"Message from {st.session_state.user_name}","body":reply.get("body",coord_inp)}
                        st.session_state.coord_chat.append({"role":"agent","content":f"📧 Found **{c['name']}** ({c['email']}). Drafted — please review and confirm."})
                    else:
                        st.session_state.coord_chat.append({"role":"agent","content":f"🔍 Could not find **{tname}**'s email. Please provide their email directly."})
                else:
                    reply = generate_reply({"email_content":coord_inp,"sender_name":st.session_state.user_name})
                    st.session_state.coord_chat.append({"role":"agent","content":reply.get("body","")})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('<div class="sec-hdr sec-teal" style="font-size:13px">📥 Read Inbox</div>', unsafe_allow_html=True)
    if st.button("📬 Fetch Latest Emails", key="fetch_emails"):
        with st.spinner("Connecting to Gmail..."):
            try:
                from tools.gmail_read import read_emails
                result = read_emails({})
                for em in result.get("emails", []):
                    st.markdown(f"""<div class="hist-row">
                    <b>From:</b> {em['from_name']} &lt;{em['from_email']}&gt;&nbsp;&nbsp;
                    <b>Subject:</b> {em['subject']}<br>
                    <small style="color:#64748b">{em['body'][:200]}...</small>
                    </div>""", unsafe_allow_html=True)
                if not result.get("emails"):
                    st.info(f"📭 {result.get('email_error','No emails found.')}")
            except Exception as e:
                st.error(f"Error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — HR
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="sec-hdr sec-purple">🧑‍💼 HR Operations Agent</div>', unsafe_allow_html=True)
    hr_user   = st.text_input("Your Name", value=st.session_state.user_name, key="hr_user")
    hr_action = st.selectbox("HR Action", ["🔍 Screen CVs","❓ HR Policy Q&A","📝 Interview Questions","📋 Onboarding Checklist","📄 Draft Job Description"], key="hr_action")

    if hr_action.startswith("🔍"):
        jd = st.text_area("Job Description", placeholder="Paste full job description...", height=120, key="hr_jd")
        uploaded = st.file_uploader("Upload CV Files (PDF, DOCX, TXT)", accept_multiple_files=True, type=["pdf","docx","txt"], key="cv_up")
        if uploaded:
            for f in uploaded:
                if not any(c["name"]==f.name for c in st.session_state.uploaded_cvs):
                    try:
                        # Try proper PDF parsing
                        if f.name.endswith(".pdf"):
                            import io
                            pdf_bytes = f.read()
                            try:
                                import pdfplumber
                                text = ""
                                with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                                    for page in pdf.pages:
                                        text += (page.extract_text() or "") + "\n"
                            except Exception:
                                try:
                                    import PyPDF2
                                    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
                                    text = " ".join(p.extract_text() or "" for p in reader.pages)
                                except Exception:
                                    text = pdf_bytes.decode("utf-8","ignore")
                        else:
                            text = f.read().decode("utf-8","ignore")
                        st.session_state.uploaded_cvs.append({"name":f.name,"content":text})
                    except Exception:
                        st.session_state.uploaded_cvs.append({"name":f.name,"content":f.read().decode("utf-8","ignore")})
            st.success(f"✅ {len(st.session_state.uploaded_cvs)} CV(s) loaded")

        if st.session_state.uploaded_cvs:
            st.caption("CVs: " + ", ".join(c["name"] for c in st.session_state.uploaded_cvs))
            if st.button("🗑️ Clear CVs", key="clr_cvs"): st.session_state.uploaded_cvs=[]; st.rerun()

        if st.button("🚀 Screen Candidates", key="hr_screen", use_container_width=True):
            if not jd.strip(): st.warning("Enter job description")
            elif not st.session_state.uploaded_cvs: st.warning("Upload CVs first")
            else:
                with st.spinner(f"Screening {len(st.session_state.uploaded_cvs)} candidates..."):
                    try:
                        from graph.hr_graph import hr_graph
                        result = hr_graph.invoke({"action":"screen_cvs","job_description":jd,"cvs":st.session_state.uploaded_cvs})
                        st.session_state.hr_results = result.get("results",[])
                        # Save to DB
                        try:
                            from database.sqlite_db import log_candidate
                            for r in st.session_state.hr_results:
                                log_candidate(r.get("name",""), jd[:100], r.get("score",0),
                                              r.get("recommendation",""), r.get("strengths",[]),
                                              r.get("weaknesses",[]), r.get("summary",""))
                        except Exception:
                            pass
                    except Exception as e:
                        st.error(f"Error: {e}")

        if st.session_state.hr_results:
            st.markdown('<div class="sec-hdr sec-purple" style="font-size:13px">📊 Screening Results</div>', unsafe_allow_html=True)
            for i, r in enumerate(st.session_state.hr_results, 1):
                score = r.get("score",0)
                rec   = r.get("recommendation","")
                color = "#16a34a" if score>=70 else ("#ca8a04" if score>=50 else "#dc2626")
                rb    = {"Highly Recommended":"badge-green","Recommended":"badge-blue","Maybe":"badge-yellow","Not Recommended":"badge-red"}.get(rec,"badge-yellow")
                with st.expander(f"#{i} {r.get('name','Unknown')} — {score}/100", expanded=i==1):
                    st.markdown(f"""<div class="cand-card">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                    <b style="font-size:16px">{r.get('name','')}</b>
                    <span class="badge {rb}">{rec}</span></div>
                    <div class="score-bar"><div class="score-fill" style="width:{score}%;background:{color}"></div></div>
                    <small style="color:{color}"><b>Score: {score}/100</b></small><br><br>
                    {r.get('summary','')}
                    </div>""", unsafe_allow_html=True)
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        if r.get("strengths"):
                            st.markdown("**✅ Strengths:**")
                            for s in r["strengths"]: st.markdown(f"- {s}")
                    with sc2:
                        if r.get("weaknesses"):
                            st.markdown("**⚠️ Weaknesses:**")
                            for w in r["weaknesses"]: st.markdown(f"- {w}")

    elif hr_action.startswith("❓"):
        q = st.text_area("HR Question", placeholder="e.g. How many leaves per year? What is the recruitment process?", height=100)
        if st.button("🔍 Get Answer", key="hr_qa", use_container_width=True) and q.strip():
            with st.spinner("HR Agent thinking..."):
                try:
                    # Try ChromaDB HR policies first
                    from database.vector_db import rag_answer, collection_stats
                    stats2 = collection_stats()
                    if stats2.get("hr_policies",0) > 0:
                        ans = rag_answer(q, "hr_policies", top_k=4, user_name=hr_user)
                    else:
                        from graph.hr_graph import hr_graph
                        result = hr_graph.invoke({"action":"hr_query","query":q,"user_name":hr_user})
                        ans = result.get("output","")
                    st.markdown(f'<div class="resp-box resp-purple">{ans}</div>', unsafe_allow_html=True)
                    from database.sqlite_db import log_agent
                    log_agent("HR Agent","hr_qa",q,ans[:500])
                except Exception as e:
                    st.error(f"Error: {e}")

    elif hr_action.startswith("📝"):
        iq_jd   = st.text_area("Job Description", height=100, key="iq_jd")
        iq_name = st.text_input("Candidate Name", key="iq_name")
        iq_cv   = st.text_area("CV Summary (optional)", height=80, key="iq_cv")
        if st.button("📝 Generate Questions", key="iq_btn", use_container_width=True):
            with st.spinner("Generating..."):
                try:
                    from graph.hr_graph import hr_graph
                    r = hr_graph.invoke({"action":"interview_questions","job_description":iq_jd,"candidate_name":iq_name or "Candidate","cv_content":iq_cv})
                    st.markdown(f'<div class="resp-box resp-purple">{r.get("output","")}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    elif hr_action.startswith("📋"):
        ob1, ob2 = st.columns(2)
        with ob1: ob_title = st.text_input("Job Title", key="ob_title")
        with ob2: ob_dept  = st.text_input("Department", key="ob_dept")
        if st.button("📋 Generate Checklist", key="ob_btn", use_container_width=True):
            with st.spinner("Generating..."):
                try:
                    from graph.hr_graph import hr_graph
                    r = hr_graph.invoke({"action":"onboarding","job_title":ob_title or "Employee","department":ob_dept or "General"})
                    st.markdown(f'<div class="resp-box resp-purple">{r.get("output","")}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    elif hr_action.startswith("📄"):
        jd1, jd2 = st.columns(2)
        with jd1: jd_role = st.text_input("Role", key="jd_role")
        with jd2: jd_dept = st.text_input("Department", key="jd_dept")
        jd_req = st.text_area("Key Requirements", height=80, key="jd_req")
        if st.button("📄 Draft JD", key="jd_btn", use_container_width=True):
            with st.spinner("Drafting..."):
                try:
                    from graph.hr_graph import hr_graph
                    r = hr_graph.invoke({"action":"job_description","job_title":jd_role,"department":jd_dept,"query":jd_req})
                    st.markdown(f'<div class="resp-box resp-purple">{r.get("output","")}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — FINANCE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="sec-hdr sec-green">💰 Finance Agent</div>', unsafe_allow_html=True)
    fin_user   = st.text_input("Your Name", value=st.session_state.user_name, key="fin_user")
    fin_action = st.selectbox("Finance Action", ["❓ Finance Q&A","📊 Analyze Expenses","🧾 Summarize Invoice","📈 Generate Report","⚖️ Budget vs Actual"], key="fin_act")

    if fin_action.startswith("❓"):
        fin_q   = st.text_area("Question", placeholder="e.g. What is the tax rate for IT services in Pakistan?", height=100)
        fin_ctx = st.text_area("Additional context (optional)", height=70, key="fin_ctx")
        if st.button("🔍 Ask Finance Agent", key="fin_qa", use_container_width=True) and fin_q.strip():
            with st.spinner("Finance Agent analyzing..."):
                try:
                    # Try ChromaDB finance docs first
                    from database.vector_db import rag_answer, collection_stats
                    fstats = collection_stats()
                    if fstats.get("finance_docs",0) > 0:
                        ans = rag_answer(fin_q, "finance_docs", top_k=4, user_name=fin_user)
                    else:
                        from graph.finance_graph import finance_graph
                        r   = finance_graph.invoke({"action":"query","question":fin_q,"context":fin_ctx,"user_name":fin_user})
                        ans = r.get("output","")
                    st.markdown(f'<div class="resp-box resp-green">{ans}</div>', unsafe_allow_html=True)
                    from database.sqlite_db import log_finance
                    log_finance(fin_user,"qa",fin_q,ans[:500])
                except Exception as e:
                    st.error(f"Error: {e}")

    elif fin_action.startswith("📊"):
        fin_data = st.text_area("Paste Expense Data (CSV or text)",
            placeholder="Date, Description, Amount, Category\n2024-01-05, Office Supplies, 2500, Operations",
            height=180, key="fin_exp")
        if st.button("📊 Analyze", key="fin_exp_btn", use_container_width=True):
            with st.spinner("Analyzing expenses..."):
                try:
                    from graph.finance_graph import finance_graph
                    r = finance_graph.invoke({"action":"analyze_expenses","data":fin_data,"user_name":fin_user})
                    ans = r.get("output","")
                    st.markdown(f'<div class="resp-box resp-green">{ans}</div>', unsafe_allow_html=True)
                    # Chart
                    try:
                        import pandas as pd, io
                        df = pd.read_csv(io.StringIO(fin_data))
                        if df.shape[1] >= 3:
                            amt_col = df.columns[2]
                            cat_col = df.columns[3] if df.shape[1] > 3 else df.columns[1]
                            chart_df = df.groupby(cat_col)[amt_col].sum().reset_index()
                            st.bar_chart(chart_df.set_index(cat_col))
                    except Exception:
                        pass
                    from database.sqlite_db import log_finance
                    log_finance(fin_user,"analyze_expenses",fin_data[:500],ans[:500])
                except Exception as e:
                    st.error(f"Error: {e}")

    elif fin_action.startswith("🧾"):
        inv_text = st.text_area("Paste Invoice Text", height=200, key="inv_txt")
        if st.button("🧾 Summarize", key="inv_btn", use_container_width=True):
            with st.spinner("Processing invoice..."):
                try:
                    from graph.finance_graph import finance_graph
                    r = finance_graph.invoke({"action":"summarize_invoice","data":inv_text})
                    st.markdown(f'<div class="resp-box resp-green">{r.get("output","")}</div>', unsafe_allow_html=True)
                    from database.sqlite_db import log_finance
                    log_finance(fin_user,"summarize_invoice",inv_text[:300],r.get("output","")[:500])
                except Exception as e:
                    st.error(f"Error: {e}")

    elif fin_action.startswith("📈"):
        rep_data = st.text_area("Financial Data", height=160, key="rep_data")
        rep_type = st.selectbox("Report Type", ["general","budget","expense","invoice"], key="rep_type")
        if st.button("📈 Generate Report", key="rep_btn", use_container_width=True):
            with st.spinner("Generating report..."):
                try:
                    from graph.finance_graph import finance_graph
                    r = finance_graph.invoke({"action":"report","data":rep_data,"report_type":rep_type})
                    st.markdown(f'<div class="resp-box resp-green">{r.get("output","")}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    elif fin_action.startswith("⚖️"):
        bc1, bc2 = st.columns(2)
        with bc1: bdata = st.text_area("Budget Data", placeholder="IT, 500000\nMarketing, 200000", height=140, key="bdata")
        with bc2: adata = st.text_area("Actual Data", placeholder="IT, 485000\nMarketing, 267000", height=140, key="adata")
        if st.button("⚖️ Analyze", key="bva_btn", use_container_width=True):
            with st.spinner("Analyzing..."):
                try:
                    from graph.finance_graph import finance_graph
                    r = finance_graph.invoke({"action":"budget_vs_actual","data":f"{bdata}|||{adata}"})
                    ans = r.get("output","")
                    st.markdown(f'<div class="resp-box resp-green">{ans}</div>', unsafe_allow_html=True)
                    # Chart
                    try:
                        import pandas as pd, io
                        bdf = pd.read_csv(io.StringIO(bdata), header=None, names=["Category","Budget"])
                        adf = pd.read_csv(io.StringIO(adata), header=None, names=["Category","Actual"])
                        merged = bdf.merge(adf, on="Category").set_index("Category")
                        st.bar_chart(merged)
                    except Exception:
                        pass
                except Exception as e:
                    st.error(f"Error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — DOCUMENTS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="sec-hdr sec-teal">📂 Documents Agent <span class="badge badge-mcp">MCP</span> <span class="badge badge-purple">ChromaDB</span></div>', unsafe_allow_html=True)
    docs_user = st.text_input("Your Name", value=st.session_state.user_name, key="docs_user")

    lc1, lc2 = st.columns(2)
    with lc1:
        if st.button("☁️ Load from Google Drive", key="load_drive", use_container_width=True):
            with st.spinner("📂 Loading and reading Drive files..."):
                try:
                    from tools.mcp_drive_client import DriveClient
                    client = DriveClient()
                    docs   = client.load_documents(max_results=50)
                    if docs:
                        st.session_state.drive_documents = docs
                        # Embed into ChromaDB
                        from database.vector_db import embed_documents
                        with st.spinner("🧠 Embedding into ChromaDB..."):
                            res = embed_documents(docs, "documents")
                        st.success(f"✅ Loaded {len(docs)} docs · Embedded {res.get('embedded',0)} into ChromaDB")
                        # Save metadata to SQLite
                        try:
                            from database.sqlite_db import get_session, DocumentMeta
                            s = get_session()
                            for d in docs:
                                s.add(DocumentMeta(file_name=d.get("file",""), content_len=len(d.get("content","")), source="drive", embedded=True))
                            s.commit(); s.close()
                        except Exception:
                            pass
                    else:
                        files = client.list_files(max_results=50)
                        if files:
                            st.session_state.drive_documents = [{"file":f.get("name",""), "id":f.get("id",""), "content":""} for f in files]
                            st.warning(f"⚠️ Listed {len(files)} files but could not read content.")
                        else:
                            st.warning("No files found in Google Drive.")
                except Exception as e:
                    st.error(f"Drive error: {e}")

    with lc2:
        up_docs = st.file_uploader("📁 Upload Files", accept_multiple_files=True, type=["pdf","txt","docx"], key="doc_up")
        if up_docs:
            for f in up_docs:
                if not any(d["file"]==f.name for d in st.session_state.drive_documents):
                    try:
                        if f.name.endswith(".pdf"):
                            import io, pdfplumber
                            with pdfplumber.open(io.BytesIO(f.read())) as pdf:
                                content = "\n".join(p.extract_text() or "" for p in pdf.pages)
                        else:
                            content = f.read().decode("utf-8","ignore")
                        st.session_state.drive_documents.append({"file":f.name,"content":content})
                    except Exception:
                        st.session_state.drive_documents.append({"file":f.name,"content":f.read().decode("utf-8","ignore")})
            # Auto-embed
            if st.session_state.drive_documents:
                from database.vector_db import embed_documents
                embed_documents([d for d in st.session_state.drive_documents if d.get("content")], "documents")
            st.success(f"✅ {len(st.session_state.drive_documents)} documents ready & embedded")

    if st.session_state.drive_documents:
        names = " · ".join(d["file"] for d in st.session_state.drive_documents[:5])
        extra = f" ···+{len(st.session_state.drive_documents)-5} more" if len(st.session_state.drive_documents)>5 else ""
        st.markdown(f"**{len(st.session_state.drive_documents)} documents** · {names}{extra}")
        if st.button("🗑️ Clear", key="clr_docs"): st.session_state.drive_documents=[]; st.rerun()

    st.divider()
    docs_action = st.selectbox("Document Action", [
        "💬 Q&A (RAG via ChromaDB)","🔍 Search","📝 Summarize",
        "🔎 Extract Data","⚖️ Compare Two Docs","📊 Batch Analyze","📋 List All"
    ], key="docs_action")

    if docs_action.startswith("💬"):
        for entry in st.session_state.docs_chat:
            if entry["role"]=="user":
                st.markdown(f'<div class="chat-wrap"><div class="chat-user">👤 {entry["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-wrap"><div class="chat-agent">📂 {entry["content"]}</div></div>', unsafe_allow_html=True)
        with st.form("docs_qa", clear_on_submit=True):
            dq  = st.text_area("Question", placeholder="Ask anything about your documents...", height=80)
            dsb = st.form_submit_button("💬 Ask (RAG)", use_container_width=True)
        if dsb and dq.strip():
            st.session_state.docs_chat.append({"role":"user","content":dq.strip()})
            with st.spinner("🧠 Searching ChromaDB..."):
                try:
                    from agents.documents_agent import answer_question_from_documents
                    ans = answer_question_from_documents(dq.strip(), st.session_state.drive_documents, docs_user)
                    st.session_state.docs_chat.append({"role":"agent","content":ans})
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    elif docs_action.startswith("🔍"):
        sq = st.text_input("Search query", key="doc_sq")
        if st.button("🔍 Search", key="doc_srch", use_container_width=True) and sq.strip():
            with st.spinner("Searching..."):
                try:
                    from agents.documents_agent import search_documents
                    ans = search_documents(sq, st.session_state.drive_documents, docs_user)
                    st.markdown(f'<div class="resp-box resp-teal">{ans}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    elif docs_action.startswith("📝"):
        if st.session_state.drive_documents:
            sel = st.selectbox("Select Document", [d["file"] for d in st.session_state.drive_documents], key="sum_sel")
            if st.button("📝 Summarize", key="sum_btn", use_container_width=True):
                doc = next((d for d in st.session_state.drive_documents if d["file"]==sel), None)
                if doc:
                    with st.spinner("Summarizing..."):
                        try:
                            from agents.documents_agent import summarize_document
                            ans = summarize_document(doc["content"], doc["file"], docs_user)
                            st.markdown(f'<div class="resp-box resp-teal">{ans}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error: {e}")
        else:
            st.info("Load documents first.")

    elif docs_action.startswith("🔎"):
        ext_type = st.selectbox("Extract Type", ["all","dates","amounts","parties","clauses","contacts"], key="ext_t")
        if st.session_state.drive_documents:
            sel = st.selectbox("Select Document", [d["file"] for d in st.session_state.drive_documents], key="ext_sel")
            if st.button("🔎 Extract", key="ext_btn", use_container_width=True):
                doc = next((d for d in st.session_state.drive_documents if d["file"]==sel), None)
                if doc:
                    with st.spinner("Extracting..."):
                        try:
                            from agents.documents_agent import extract_data_from_document
                            ans = extract_data_from_document(doc["content"], ext_type, doc["file"])
                            st.markdown(f'<div class="resp-box resp-teal">{ans}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error: {e}")

    elif docs_action.startswith("⚖️"):
        if len(st.session_state.drive_documents) >= 2:
            names = [d["file"] for d in st.session_state.drive_documents]
            cc1, cc2 = st.columns(2)
            with cc1: d1n = st.selectbox("Document 1", names, key="cmp1")
            with cc2: d2n = st.selectbox("Document 2", names, index=1, key="cmp2")
            if st.button("⚖️ Compare", key="cmp_btn", use_container_width=True):
                d1 = next((d for d in st.session_state.drive_documents if d["file"]==d1n), {})
                d2 = next((d for d in st.session_state.drive_documents if d["file"]==d2n), {})
                with st.spinner("Comparing..."):
                    try:
                        from agents.documents_agent import compare_documents
                        ans = compare_documents(d1.get("content",""), d2.get("content",""), d1n, d2n)
                        st.markdown(f'<div class="resp-box resp-teal">{ans}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("Load at least 2 documents.")

    elif docs_action.startswith("📊"):
        bat = st.selectbox("Analysis Type", ["overview","financial","contracts","policies","compliance"], key="bat_t")
        if st.button("📊 Batch Analyze", key="bat_btn", use_container_width=True):
            with st.spinner(f"Analyzing {len(st.session_state.drive_documents)} documents..."):
                try:
                    from agents.documents_agent import batch_analyze_documents
                    ans = batch_analyze_documents(st.session_state.drive_documents, bat)
                    st.markdown(f'<div class="resp-box resp-teal">{ans}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

    elif docs_action.startswith("📋"):
        if st.button("📋 List All", key="lst_btn", use_container_width=True):
            from agents.documents_agent import list_documents_summary
            st.markdown(f'<div class="resp-box resp-teal">{list_documents_summary(st.session_state.drive_documents)}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — WHATSAPP
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="sec-hdr sec-wa">💬 WhatsApp Integration <span class="badge badge-wa">Twilio</span></div>', unsafe_allow_html=True)

    # Twilio status
    wc1, wc2 = st.columns([2,1])
    with wc1:
        st.info("💡 **How it works:** Type a task → Orchestrator processes it → Response sent to WhatsApp number + optionally Email. To receive WhatsApp messages automatically, run `python whatsapp/webhook.py` and expose via ngrok.")
    with wc2:
        if st.button("🔌 Test Twilio Connection", use_container_width=True, key="test_twilio"):
            with st.spinner("Testing..."):
                try:
                    from whatsapp.bot import test_connection
                    res = test_connection()
                    if res.get("success"):
                        st.success(f"✅ Connected: {res.get('account','')}")
                    else:
                        st.error(f"❌ {res.get('error','Failed')}")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.divider()

    # WhatsApp chat UI
    st.markdown('<div class="sec-hdr sec-wa" style="font-size:13px">📱 Send via WhatsApp</div>', unsafe_allow_html=True)

    wa_num = st.text_input("WhatsApp Number", value="+923462792937", placeholder="+923XXXXXXXXX", key="wa_num")
    wa_email = st.text_input("Also send to Email (optional)", placeholder="ahmed@example.com", key="wa_email")

    # Chat display
    for entry in st.session_state.wa_chat:
        if entry["role"] == "user":
            st.markdown(f'<div class="chat-wrap"><div class="wa-bubble-out">👤 {entry["content"]}</div></div>', unsafe_allow_html=True)
        else:
            agents_b = " ".join([f'<span class="badge badge-green">{a}</span>' for a in entry.get("agents",[])])
            wa_stat  = entry.get("wa_status","")
            em_stat  = entry.get("email_status","")
            stat_row = ""
            if wa_stat: stat_row += f'<br><small>📱 WhatsApp: {wa_stat}</small>'
            if em_stat: stat_row += f'<small> · 📧 Email: {em_stat}</small>'
            st.markdown(f'<div class="chat-wrap"><div class="wa-bubble-in">{agents_b}<br><br>{entry["content"]}{stat_row}</div></div>', unsafe_allow_html=True)

    with st.form("wa_form", clear_on_submit=True):
        wa_inp = st.text_area("Your message / task",
            placeholder="e.g. 'My laptop won't start, please resolve this issue and send to Ahmed'\nor 'Analyze our IT expenses and notify finance team'",
            height=100)
        wc_a, wc_b = st.columns([4,1])
        with wc_a: wa_sub = st.form_submit_button("📤 Send via Orchestrator + WhatsApp", use_container_width=True)
        with wc_b: also_email = st.checkbox("+ Email", value=bool(wa_email), key="wa_also_email")

    if wa_sub and wa_inp.strip():
        st.session_state.wa_chat.append({"role":"user","content":wa_inp.strip()})
        with st.spinner("🔄 Orchestrator processing + sending WhatsApp..."):
            try:
                from whatsapp.bot import send_agent_response_to_whatsapp
                result = send_agent_response_to_whatsapp(
                    user_input      = wa_inp.strip(),
                    recipient_number= wa_num,
                    also_email      = also_email and bool(wa_email),
                    email_address   = wa_email,
                    user_name       = st.session_state.user_name,
                )
                wa_r = result.get("whatsapp", {})
                em_r = result.get("email", "")

                wa_status = f"✅ Sent (SID: {wa_r.get('sid','')[:12]})" if wa_r and wa_r.get("success") else f"❌ {wa_r.get('error','Failed') if wa_r else 'Not sent'}"
                em_status = f"✅ {em_r}" if em_r and "✅" in str(em_r) else (f"❌ {em_r}" if em_r else "")

                st.session_state.wa_chat.append({
                    "role":         "agent",
                    "content":      result.get("agent_response",""),
                    "agents":       result.get("agents_used",[]),
                    "wa_status":    wa_status,
                    "email_status": em_status,
                })

                try:
                    from database.sqlite_db import add_notification
                    add_notification("WhatsApp message sent", f"To: {wa_num}", "success", "WhatsApp Agent")
                except Exception:
                    pass
                st.rerun()
            except Exception as e:
                st.error(f"WhatsApp error: {e}")

    st.divider()

    # WhatsApp logs
    st.markdown('<div class="sec-hdr sec-wa" style="font-size:13px">📋 WhatsApp Logs</div>', unsafe_allow_html=True)
    try:
        from database.sqlite_db import get_session, WhatsAppLog
        s    = get_session()
        wlogs = s.query(WhatsAppLog).order_by(WhatsAppLog.timestamp.desc()).limit(10).all()
        s.close()
        if wlogs:
            for wl in wlogs:
                dir_icon = "📤" if wl.direction=="outbound" else "📥"
                st.markdown(f"""<div class="hist-row">
                {dir_icon} <b>{wl.direction.upper()}</b> &nbsp;
                <b>To:</b> {wl.to_number} &nbsp;
                <span class="badge badge-{'green' if wl.status=='sent' else 'red'}">{wl.status}</span><br>
                <small style="color:#64748b">{wl.timestamp.strftime('%Y-%m-%d %H:%M')} · {wl.agents_used}</small><br>
                {wl.message[:100]}
                </div>""", unsafe_allow_html=True)
        else:
            st.caption("No WhatsApp messages yet.")
    except Exception:
        st.caption("WhatsApp logs unavailable.")

    # Webhook instructions
    with st.expander("📖 Setup Incoming WhatsApp (Webhook)"):
        st.markdown("""
**To receive WhatsApp messages and auto-reply:**

**Step 1** — Install ngrok: [ngrok.com/download](https://ngrok.com/download)

**Step 2** — Open terminal and run:
```bash
python whatsapp/webhook.py
```

**Step 3** — Open another terminal:
```bash
ngrok http 5000
```
Copy the `https://xxxx.ngrok.io` URL.

**Step 4** — Go to [twilio.com/console/sms/whatsapp/sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)

**Step 5** — Set webhook URL to:
```
https://xxxx.ngrok.io/whatsapp
```

**Step 6** — Send `join <your-sandbox-word>` from WhatsApp to +14155238886

Done! Any message sent to that number will be processed by your agents and replied automatically.
        """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 9 — HISTORY
# ══════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown('<div class="sec-hdr">📋 Task History</div>', unsafe_allow_html=True)

    hist_filter = st.selectbox("Filter by source", ["All","ui","whatsapp","api"], key="hist_filter")
    try:
        from database.sqlite_db import get_task_history
        history = get_task_history(limit=50)
        if hist_filter != "All":
            history = [h for h in history if h.get("source") == hist_filter]

        if history:
            st.caption(f"Showing {len(history)} tasks")
            for h in history:
                src_badge = {"ui":"badge-blue","whatsapp":"badge-wa","api":"badge-purple"}.get(h.get("source","ui"),"badge-blue")
                with st.expander(f"#{h['id']} · {h['time']} · {h.get('user','')} · {h.get('agents','')}", expanded=False):
                    st.markdown(f"""<div class="hist-row">
                    <span class="badge {src_badge}">{h.get('source','ui').upper()}</span>
                    <span class="badge badge-green">{h.get('role','')}</span>
                    <span style="font-size:12px;color:#64748b"> {h.get('elapsed',0)}ms</span><br><br>
                    <b>Input:</b> {h.get('input','')}<br><br>
                    <b>Agents:</b> {h.get('agents','')}<br><br>
                    <b>Response:</b><br>{h.get('response','')[:500]}{'...' if len(h.get('response',''))>500 else ''}
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("No task history yet. Use the Orchestrator tab to send tasks.")
    except Exception as e:
        st.error(f"History error: {e}")

