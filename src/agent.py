from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from typing_extensions import NotRequired

from src.llm import get_llm
from src.tools import calculator
from src.rag_tool import company_knowledge


class ProjectState(AgentState):
    business_type: NotRequired[str]
    project_type: NotRequired[str]
    use_case: NotRequired[str]
    budget: NotRequired[str]
    timeline: NotRequired[str]


def get_agent():

    llm = get_llm()

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=llm,

        tools=[
            calculator,
            company_knowledge
        ],

        state_schema=ProjectState,

        system_prompt="""
You are an AI Project Consultant for ctrlaltcrew.

Your job is to understand a client's project requirements.

Track these requirements in your state when the user provides them:

- business_type
- project_type
- use_case
- budget
- timeline

Important rules:

1. Remember information the user has already provided.
2. Do not ask for information that the user has already given.
3. Ask only ONE relevant follow-up question at a time.
4. Do not immediately recommend a package or give pricing unless the
   user asks for it or enough requirements have been collected.
5. Use company_knowledge for questions about:
   - services
   - pricing
   - AI solutions
   - project requirements
   - development process
   - FAQs
   - support and maintenance
6. Use calculator whenever mathematical calculation is required.
7. Never invent company information.
8. If the user asks what information you remember about their project,
   summarize the requirements currently known.
""",

        checkpointer=checkpointer
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
        "What do you know about my project so far?"
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