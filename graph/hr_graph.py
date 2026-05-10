from langgraph.graph import StateGraph, END
from state.hr_state import HRState
from agents.hr_agent import (
    screen_candidates, generate_interview_questions,
    generate_onboarding_checklist, answer_hr_query, draft_job_description
)


def hr_router(state: HRState) -> HRState:
    action = state.get("action", "hr_query")

    if action == "screen_cvs":
        state["results"] = screen_candidates(
            job_description=state.get("job_description", ""),
            cvs=state.get("cvs", [])
        )
    elif action == "interview_questions":
        state["output"] = generate_interview_questions(
            job_description=state.get("job_description", ""),
            candidate_name=state.get("candidate_name", "Candidate"),
            cv_content=state.get("cv_content", "")
        )
    elif action == "onboarding":
        state["output"] = generate_onboarding_checklist(
            job_title=state.get("job_title", "Employee"),
            department=state.get("department", "General")
        )
    elif action == "job_description":
        state["output"] = draft_job_description(
            role=state.get("job_title", ""),
            department=state.get("department", ""),
            requirements=state.get("query", "")
        )
    else:  # hr_query default
        state["output"] = answer_hr_query(
            question=state.get("query", ""),
            user_name=state.get("user_name", "Employee"),
            policy_context=state.get("policy_context", "")
        )

    return state


builder = StateGraph(HRState)
builder.add_node("hr_agent", hr_router)
builder.set_entry_point("hr_agent")
builder.add_edge("hr_agent", END)
hr_graph = builder.compile()
