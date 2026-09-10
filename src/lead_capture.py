import csv
from datetime import datetime
from pathlib import Path

from langchain.tools import tool, ToolRuntime


LEADS_FILE = Path("leads.csv")



@tool
def capture_lead(
    name: str,
    email: str,
    runtime: ToolRuntime,
) -> str:
    """
    REQUIRED tool for recording a lead.

    Call this tool ONLY when BOTH the user's name and email
    address have been explicitly provided.

    Do not call this tool with missing, guessed, or invented
    contact information.

    The tool saves the contact information together with the
    project requirements currently stored in agent state.
    """

    requirements = runtime.state.get("requirements", {})

    file_exists = LEADS_FILE.exists()

    lead = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "name": name,
        "email": email,
        "business_type": requirements.get("business_type", "Not specified"),
        "project_type": requirements.get("project_type", "Not specified"),
        "use_case": requirements.get("use_case", "Not specified"),
        "budget": requirements.get("budget", "Not specified"),
        "timeline": requirements.get("timeline", "Not specified"),
    }

    with LEADS_FILE.open(
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "timestamp",
            "name",
            "email",
            "business_type",
            "project_type",
            "use_case",
            "budget",
            "timeline",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(lead)

    return f"Lead captured successfully for {name}."