# Server: uvicorn test:app --reload
# LLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.prompts.chat import ChatPromptTemplate

mistral = Ollama(
    model="mistral",
    verbose=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

# -- API 

#!/usr/bin/env python

from fastapi import FastAPI
from langserve import add_routes

# 1. Chain definition

summarizer_template = """
Your are an helpful assistant producing a summary of an article
Make a 50 words summary covering the main points of the article
"""

summarizer_prompt = ChatPromptTemplate.from_messages([
    ("system", summarizer_template),
    ("human", "{text}"),
])
summarizer = summarizer_prompt | mistral 

redactor_template = """
Your are an helpful assistant redacting an article
which goes through different news about the crypto market
"""

redactor_prompt = ChatPromptTemplate.from_messages([
    ("system", redactor_template),
    ("human", "Here is a list of news {list}"),
])
redactor = redactor_prompt | mistral 

# 2. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 3. Adding summarizer route
add_routes(
    app,
    summarizer,
    path="/mistral_summarizer",
)

# 3. Adding chain route
add_routes(
    app,
    redactor,
    path="/mistral_redactor",
)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
