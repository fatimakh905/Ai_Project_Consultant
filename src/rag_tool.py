from langchain.tools import tool, ToolRuntime

from src.retriever import get_retriever
from src.llm import get_llm
from src.rag_chain import prompt, format_docs


retriever = get_retriever()
llm = get_llm()


@tool
def company_knowledge(
    question: str,
    runtime: ToolRuntime
) -> str:
    """
    Answer questions about ctrlaltcrew's services, pricing,
    project packages, AI solutions, development process,
    requirements, FAQs, and support using the company
    knowledge base.
    """

    # Get the project requirements currently stored in state
    requirements = runtime.state.get("requirements", {})

    # Convert the state into useful retrieval context
    requirement_context = " ".join(
        f"{key}: {value}"
        for key, value in requirements.items()
    )

    # Build a retrieval query using both:
    # 1. The client's actual project requirements
    # 2. The current question
    search_query = f"""
    ctrlaltcrew company services
    project packages pricing
    project timelines
    AI solutions
    development process

    Client project requirements:
    {requirement_context}

    User question:
    {question}
    """

    print("\nRAG SEARCH QUERY:")
    print(search_query)

    # Retrieve relevant knowledge-base chunks
    documents = retriever.invoke(search_query)

    print("\nRETRIEVED DOCUMENTS:")
    for i, document in enumerate(documents, start=1):
        print(f"\n--- Document {i} ---")
        print(document.page_content[:500])

    # Combine retrieved chunks
    context = format_docs(documents)

    # Ask the LLM to answer strictly from retrieved context
    response = (prompt | llm).invoke({
        "context": context,
        "question": question
    })

    return response.content