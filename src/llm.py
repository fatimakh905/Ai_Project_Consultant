from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm():
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0
    )

    return llm


if __name__ == "__main__":
    llm = get_llm()

    response = llm.invoke(
        "Explain RAG in one simple paragraph."
    )

    print(response.content)