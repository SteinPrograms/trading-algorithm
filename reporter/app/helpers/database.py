import os
from dotenv import load_dotenv
from supabase import create_client, Client

class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.supabase: Client = create_client(
            os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
        )

    def get_api_keys(self):
        response = self.supabase.table("users").select("*").execute()
        return [user["api_key"] for user in response.data]
