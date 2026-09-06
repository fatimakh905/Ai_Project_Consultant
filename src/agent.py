from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver

from src.llm import get_llm
from src.tools import calculator
from src.rag_tool import company_knowledge
from src.requirements_tool import update_project_requirements


class ProjectState(AgentState):
    business_type: str | None
    project_type: str | None
    use_case: str | None
    budget: str | None
    timeline: str | None

def get_agent():

    llm = get_llm()

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=llm,

        tools=[
            calculator,
            company_knowledge,
            update_project_requirements
        ],

        state_schema=ProjectState,

        system_prompt="""
You are an AI Project Consultant for ctrlaltcrew.

Your job is to understand a client's project requirements.

Track these requirements:

- business_type
- project_type
- use_case
- budget
- timeline

IMPORTANT:

Whenever the user provides information about any of these
requirements, ALWAYS call the update_project_requirements tool
to save that information into the project state.

For example:

User: My business is an e-commerce store.

Call:
update_project_requirements(
    business_type="e-commerce store"
)

User: I need an AI chatbot.

Call:
update_project_requirements(
    project_type="AI chatbot"
)

User: It should handle customer support.

Call:
update_project_requirements(
    use_case="customer support"
)

Remember information the user has already provided.

Do not ask for information that the user has already given.

Ask only ONE relevant follow-up question at a time.

Do not immediately recommend a package or give pricing unless
the user asks for it or enough requirements have been collected.

Use company_knowledge for questions about:

- services
- pricing
- AI solutions
- project requirements
- development process
- FAQs
- support and maintenance

Use calculator whenever mathematical calculation is required.

Never invent company information.

If the user asks what you remember about their project,
summarize the requirements currently stored in the project state.
"""
    )

    return agent


if __name__ == "__main__":

    agent = get_agent()

    config = {
        "configurable": {
            "thread_id": "demo_user_1"
        }
    }

    messages = [
        "My business is an e-commerce store.",
        "I need an AI chatbot.",
        "It should handle customer support.",
        "My budget is around $3000.",
        "The project should be completed within 4 weeks.",
    ]

    for message in messages:

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            },
            config=config
        )

        print("\nUser:")
        print(message)

        print("\nAgent:")
        print(response["messages"][-1].content)

        print("\nCurrent state:")
        print({
            "business_type": response.get("business_type"),
            "project_type": response.get("project_type"),
            "use_case": response.get("use_case"),
            "budget": response.get("budget"),
            "timeline": response.get("timeline")
        })

        print("-" * 60)