from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from src.retriever import get_retriever
from src.llm import get_llm


prompt = ChatPromptTemplate.from_template("""
You are the AI Project Consultant for ctrlaltcrew.

Answer the user's question using ONLY the context provided below.

If the answer is not present in the context, say:
"I don't have that information in my knowledge base."

Do not make up facts.

Context:
{context}

Question:
{question}
""")


def format_docs(documents):
    return "\n\n".join(
        document.page_content
        for document in documents
    )


def get_rag_chain():

    retriever = get_retriever()
    llm = get_llm()

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    return rag_chain


if __name__ == "__main__":

    rag_chain = get_rag_chain()

    question = "Who is the founder of ctrlaltcrew?"

    response = rag_chain.invoke(question)

    print("\nAnswer:")
    print(response.content)