from langchain_chroma import Chroma
from src.embeddings import get_embedding_model

CHROMA_DIR = "chroma_db"


def get_retriever():
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedding_model
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 6}
    )

    return retriever


if __name__ == "__main__":
    retriever = get_retriever()

    question = "What AI chatbot services, packages, pricing, and timelines does ctrlaltcrew offer?"

    documents = retriever.invoke(question)

    print(f"Retrieved {len(documents)} documents\n")

    for i, doc in enumerate(documents, start=1):
        print(f"--- Result {i} ---")
        print(doc.page_content)
        print("\nMetadata:")
        print(doc.metadata)
        print()