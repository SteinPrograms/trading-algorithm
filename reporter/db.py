from dotenv import load_dotenv
from supabase import create_client, Client

# Load the environment variables
load_dotenv()
try:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    assert type(url) == str, "UNABLE TO LOAD SUPABASE_URL"
    assert type(key) == str, "UNABLE TO LOAD SUPABASE_KEY"
except Exception as e:
    logger.error("Error while loading environment variables")
    logger.error(e)
    raise e

# Create the supabase client
supabase: Client = create_client(url, key)

def insert_database(article):
    data, count = supabase.table("coindesk").insert(article).execute()
    print(count)
    return data
