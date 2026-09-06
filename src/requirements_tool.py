from langchain_core.tools import tool
from langchain.tools import ToolRuntime
from langchain.messages import ToolMessage
from langgraph.types import Command


@tool
def update_project_requirements(
    business_type: str | None = None,
    project_type: str | None = None,
    use_case: str | None = None,
    budget: str | None = None,
    timeline: str | None = None,
    runtime: ToolRuntime = None
) -> Command:
    """
    Save and update the project requirements provided by the user.
    """

    # Get the current project state
    current_state = runtime.state

    # Start with the existing values
    updates = {
        "business_type": current_state.get("business_type"),
        "project_type": current_state.get("project_type"),
        "use_case": current_state.get("use_case"),
        "budget": current_state.get("budget"),
        "timeline": current_state.get("timeline"),
    }

    # Replace values only when the user provided new information
    if business_type is not None:
        updates["business_type"] = business_type

    if project_type is not None:
        updates["project_type"] = project_type

    if use_case is not None:
        updates["use_case"] = use_case

    if budget is not None:
        updates["budget"] = budget

    if timeline is not None:
        updates["timeline"] = timeline

    return Command(
        update={
            **updates,
            "messages": [
                ToolMessage(
                    content="Project requirements updated successfully.",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        }
    )


# For current state update extended AgentState which was not working correctly.