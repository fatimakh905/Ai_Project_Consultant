from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


from src.llm import get_llm
from src.tools import calculator
from src.rag_tool import company_knowledge


def get_agent():

    llm = get_llm()

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=llm,
        tools=[
            calculator,
            company_knowledge
        ],
        system_prompt="""
You are an AI Project Consultant for ctrlaltcrew.

Use the company_knowledge tool for questions about:
- services
- pricing
- AI solutions
- project requirements
- development process
- FAQs
- support and maintenance

Use the calculator tool whenever mathematical calculation is required.

Remember information the user provides during the conversation.

Choose the appropriate tool based on the user's question.
Do not invent company information.
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

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "My business is an e-commerce store."
                }
            ]
        },
        config=config
    )

    print("\nAgent:")
    print(response["messages"][-1].content)

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "I want an AI chatbot for customer support."
                }
            ]
        },
        config=config
    )

    print("\nAgent:")
    print(response["messages"][-1].content)

    response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What type of business did I say I have?"
            }
        ]
    },
    config=config
)

print("\nAgent:")
print(response["messages"][-1].content)