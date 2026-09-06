from langchain_chroma import Chroma

CHROMA_DIR = "chroma_db"


def create_vector_store(chunks, embedding_model):
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_DIR,
    )

    return vector_store