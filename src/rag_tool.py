from langchain_core.tools import tool

from src.retriever import get_retriever
from src.llm import get_llm
from src.rag_chain import prompt, format_docs


retriever = get_retriever()
llm = get_llm()


@tool
def company_knowledge(question: str) -> str:
    """Answer questions about ctrlaltcrew's services, pricing, process,
    AI solutions, requirements, FAQs, and support using the company
    knowledge base.
    """

    documents = retriever.invoke(question)

    context = format_docs(documents)

    response = (prompt | llm).invoke({
        "context": context,
        "question": question
    })

    return response.content