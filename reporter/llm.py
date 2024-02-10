import requests
from log import logger
from fastapi import HTTPException

def summarizer(content: str) -> str:
    # Create a summary of the article using mistral
    try:
        response = requests.post(
            "http://localhost:8000/summarizer/invoke", json={"input": {"text": content}}
        )
    except Exception:
        logger.error("UNABLE TO CONNECT TO SUMMARIZER API")
        raise HTTPException(
            status_code=404, detail="UNABLE TO CONNECT TO SUMMARIZER API"
        )
    json_response = response.json()
    summary = json_response.get("output")
    return summary



