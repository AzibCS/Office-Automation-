from typing import TypedDict, Optional

class FinanceState(TypedDict, total=False):
    action:      str    # query | analyze_expenses | summarize_invoice | report | budget_vs_actual
    question:    str
    context:     str
    data:        str
    report_type: str
    user_name:   str
    output:      str
