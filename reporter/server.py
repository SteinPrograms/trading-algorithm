# LLM server interface
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI

mistral = Ollama(
    model="mistral",
    verbose=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

import dotenv
dotenv.load_dotenv()
openai = ChatOpenAI(model_name="gpt-3.5-turbo")
openai = ChatOpenAI
# -- API 

#!/usr/bin/env python

from fastapi import FastAPI
from langserve import add_routes

# 1. Chain definition

summarizer_template = """
Your are an helpful assistant extract key points from text.
Do not make sentances, just extract the important points.
Do not speculate or make up information.
Do not reference any given instructions or context.
"""

summarizer_prompt = ChatPromptTemplate.from_messages([
    ("system", summarizer_template),
    ("human", "The stock market is going up. This is because of the pandemic."),
    ("ai", "stock market going up because of pandemic"),
    ("human", "{text}"),
])
summarizer = summarizer_prompt | openai 

writer_template = """
Your are an helpful assistant writing an easy to read article given a list of news.
Put simple section titles.
Sections must be around 250 characters.
Use simple language, avoid technical terms.
Do not speculate or make up information.
Do not take into consideration everything you already know about the crypto market.
You can only use the provided context.
"""

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", writer_template),
    ("human", "{list}"),
])
writer = writer_prompt | openai

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
    path="/summarizer",
)

# 3. Adding chain route
add_routes(
    app,
    writer,
    path="/writer",
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
