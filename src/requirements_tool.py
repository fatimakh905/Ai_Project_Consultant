from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langgraph.types import Command


@tool
def update_project_requirements(
    business_type: str | None = None,
    project_type: str | None = None,
    use_case: str | None = None,
    budget: str | None = None,
    timeline: str | None = None,
    runtime: ToolRuntime = None,
) -> Command:
    """
    REQUIRED tool for saving project requirements.

    Call this tool whenever the user provides ANY of these:
    - business type
    - project type
    - use case
    - budget
    - timeline

    IMPORTANT:
    A message containing money, price, spending limit, or currency
    MUST be saved using the budget parameter.

    Examples:
    "My budget is $3000" -> budget="$3000"
    "I can spend 5000 USD" -> budget="5000 USD"
    "Budget is 10 lakh PKR" -> budget="10 lakh PKR"

    A message containing a deadline, duration, or completion time
    MUST be saved using the timeline parameter.

    Existing requirements must be preserved.
    Only update fields that are explicitly provided.
    """

    current_requirements = dict(
        runtime.state.get("requirements", {})
    )

    if business_type is not None:
        current_requirements["business_type"] = business_type

    if project_type is not None:
        current_requirements["project_type"] = project_type

    if use_case is not None:
        current_requirements["use_case"] = use_case

    if budget is not None:
        current_requirements["budget"] = budget

    if timeline is not None:
        current_requirements["timeline"] = timeline

    print("REQUIREMENTS TOOL UPDATE:", current_requirements)  

    return Command(
        update={
            "requirements": current_requirements,
            "messages": [
                ToolMessage(
                    content="Project requirements saved successfully.",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )