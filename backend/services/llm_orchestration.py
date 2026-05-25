import json
import os
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage

localai_base_url = os.getenv("LOCALAI_URL", "http://127.0.0.1:8080").rstrip("/")
openai_api_base = (
    localai_base_url if localai_base_url.endswith("/v1") else f"{localai_base_url}/v1"
)

# ---- Initialize LLM ----
llm = ChatOpenAI(
    openai_api_base=openai_api_base,
    openai_api_key="dummy",
    model="mistral-7b-instruct-v0.3",
    temperature=0.2
)

# ---- Initialize RAG ----
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


def retrieve_context(query: str, k: int = 3):
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])


# -------------------------------------------------
# Translation Function
# -------------------------------------------------
async def translate(code, source, target, history):

    context = retrieve_context(f"{source} to {target}")

    prompt = f"""
You are an expert CI/CD pipeline translator.

Source Tool: {source}
Target Tool: {target}

Relevant documentation:
{context}

Pipeline Code:
{code}

Respond in JSON:
{{
  "translated_code": "...",
  "explanation": "..."
}}
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)
    except:
        return {
            "translated_code": response.content,
            "explanation": "Could not parse structured output."
        }


# -------------------------------------------------
# General Chat Function
# -------------------------------------------------
async def chat(message, history):

    formatted_history = ""
    for msg in history:
        formatted_history += f"{msg.get('role')}: {msg.get('content')}\n"

    prompt = f"""
You are a CI/CD assistant.

Conversation:
{formatted_history}

User: {message}
"""

    response = llm.invoke(prompt)
    return response.content
