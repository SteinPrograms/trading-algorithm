# Import the required libraries
import os
import uvicorn
from dotenv import load_dotenv
from routers import news
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.config import LOGGING_CONFIG

load_dotenv()
# Check if the API_KEY is set in env
try:
    SERVER_API_KEY = os.environ["STEINPROGRAMS_API_KEY"]
except KeyError:
    raise KeyError("STEINPROGRAMS_API_KEY is not set")

# Create the fastapi app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(news.router)

if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run("main:app", host="0.0.0.0", port=5050, log_level="info", reload=True)