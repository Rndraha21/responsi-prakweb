import os
from dotenv import load_dotenv
from supabase import create_client
from httpx import Client

load_dotenv()

custom_http = Client(http2=False)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key, http_client=custom_http)
