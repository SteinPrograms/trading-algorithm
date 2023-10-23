from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler                                  
from langchain.prompts.chat import ChatPromptTemplate


llm = Ollama(model="mistral", 
             )

# First define model role and goal
template = (
    "Provided a list of news about the {symbol} crypto market."
    "Write a blog post about the news."
    "Make a general readable summary of around 500 characters about the news, make transition between news. It should be easy to read"
)
print(type(template))
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system",template),
    ("human",human_template),
])

chat = chat_prompt.format_messages(symbol="BTC",text="All time high for bitcoin")
print(chat)
# Second provide data that needs to be processed
print(llm(chat))
