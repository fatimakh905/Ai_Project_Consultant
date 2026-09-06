from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return embedding_model


if __name__ == "__main__":
    embedding_model = get_embedding_model()

    test_text = "RAG chatbot development takes 5–9 weeks."

    vector = embedding_model.embed_query(test_text)

    print(f"Embedding dimensions: {len(vector)}")
    print("\nFirst 10 values:")
    print(vector[:10])