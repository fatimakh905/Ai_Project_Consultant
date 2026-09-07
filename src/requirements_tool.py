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
    Save any project requirements provided by the user.
    Existing requirements are preserved.
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