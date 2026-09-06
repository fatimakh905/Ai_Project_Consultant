from langchain.agents import create_agent

from src.llm import get_llm
from src.tools import calculator
from src.rag_tool import company_knowledge


def get_agent():

    llm = get_llm()

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

Choose the appropriate tool based on the user's question.
Do not invent company information.
"""
    )

    return agent


if __name__ == "__main__":

    agent = get_agent()

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": "How much does a RAG-based knowledge assistant cost?"
            }
        ]
    })

    print(response["messages"][-1].content)