import os
import json
import logging
from typing import List, Dict

# LangChain imports
from langchain_community.chat_models import ChatOllama, ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

logger = logging.getLogger(__name__)

# Dynamic LLM Initialization 
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
LLM_MODEL = os.getenv("LLM_MODEL", "mistral") # Defaulting to mistral 

if LLM_PROVIDER == "localai":
    print(f"Initializing LocalAI with model: {LLM_MODEL}")
    llm = ChatOpenAI(
        openai_api_base=os.getenv("LOCALAI_URL", "http://localhost:8080/v1"),
        openai_api_key="dummy",
        model_name=LLM_MODEL,
        temperature=0.2
    )
else:
    print(f"Initializing Ollama with model: {LLM_MODEL}")
    llm = ChatOllama(
        base_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
        model=LLM_MODEL,
        temperature=0.2
    )

# -------------------------------------------------
# Translation Function
# -------------------------------------------------
async def translate(code: str, source: str, target: str, history: List[Dict]) -> Dict:
    """
    Translates pipeline code to a basic target format.
    """

    system_prompt = f"""
    You are an SDLC AI Assistant.
    Translate the CI/CD pipeline from {source} to {target}.
    
    INSTRUCTIONS:
    1. Translate the code.
    2. Provide a step-by-step checklist.
    3. Explain the rationale for security additions.
    
    You MUST output ONLY a valid JSON object.
    {{
        "translated_code": "<target code here>",
        "explanation": "<checklist and rationale here>"
    }}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Pipeline code to translate:\n\n{code}")
    ]

    try:
        response = llm.invoke(messages)
        raw_content = response.content.strip()
        
        # Directly attempt to parse whatever the LLM returns
        result = json.loads(raw_content)
        result["status"] = "success"
        return result
        
    except json.JSONDecodeError:
        logger.error(f"JSON Parsing failed. Raw output: {response.content}")
        return {
            "translated_code": "# Translation succeeded, but output formatting failed.\n# See explanation.",
            "explanation": f"The local model failed to return strict JSON. Here is its raw response:\n\n{response.content}",
            "status": "error"
        }
    except Exception as e:
        logger.error(f"LLM Invocation failed: {str(e)}")
        return {
            "translated_code": "",
            "explanation": f"An error occurred during translation: {str(e)}",
            "status": "error"
        }

# -------------------------------------------------
# General Chat Function
# -------------------------------------------------
async def chat(message: str, history: List[Dict]) -> str:
    """
    Handles general conversational queries about CI/CD.
    """
    system_prompt = """
    You are an SDLC Assistant. 
    Help engineers understand CI/CD concepts, troubleshoot pipelines.
    Keep answers developer-friendly and concise.
    """
    
    messages = [SystemMessage(content=system_prompt)]
    
    for msg in history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
            
    messages.append(HumanMessage(content=message))
    
    try:
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error connecting to the local AI service: {str(e)}"
