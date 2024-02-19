"""
API to fetch news from coindesk
"""

# Import the required libraries
import os
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException
from uvicorn.config import LOGGING_CONFIG
from fastapi.middleware.cors import CORSMiddleware
from app.app.helpers.log import logger
import asyncio
import time
import itertools
from dotenv import load_dotenv
from app.app.models.coindesk import Coindesk
from app.app.models.crypto import Crypto
from supabase import create_client, Client 

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

    


class MEMORY:
    API_KEYS = []

def get_supabase_client():
    return create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY")
    )
@app.post("/update_keys")
def update_keys(item: APIKEY):
    """
    REQUEST FROM WEB SERVER ONLY

    Update all api keys
    """
    global API_KEYS
    if item.api_key != os.getenv("STEINPROGRAMS_API_KEY"):
        logger.error(f"api_key: {item.api_key}")
        raise HTTPException(
            status_code=403, detail
            =f"API KEY {item.api_key} is not valid"
        )
    # Fetch API KEYS from the database
    # Update memory
    ### SUPABASE CLIENT
    supabase: Client = create_client(
        os.environ.get("SUPABASE_URL"),
        os.environ.get("SUPABASE_KEY")
    )
    # data = supabase.auth.sign_in_with_password({
    #     "email": os.environ.get("SUPABASE_EMAIL"),
    #     "password": os.environ.get("SUPABASE_PASSWORD")
    # })
    # rls = supabase.postgrest.auth(supabase.auth.get_session().access_token)
    try:
        data, count = supabase.table('users').select('*').execute()
        logger.info(data)
    except Exception as e:
        logger.error(e)
        logger.error("unable to fetch data")
        error =e
    finally:
        supabase.auth.sign_out()
        try:
            if (error):
                raise HTTPException(
                    status_code=500, detail
                    =f"UNABLE TO FETCH DATA"
                )
        except UnboundLocalError:
            # There is no error
            pass
        return {"message": "success"}



if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
    uvicorn.run(
        "interact:app", host="0.0.0.0", port=5050, log_level="info", reload=True
    )
