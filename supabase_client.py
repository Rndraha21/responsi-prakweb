import os
from dotenv import load_dotenv
from supabase import create_client
import httpx

load_dotenv()

transport = httpx.HTTPTransport(http2=False)

http_client = httpx.Client(transport=transport, timeout=10.0)


url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")
supabase = create_client(url, key, options={"http_client": http_client})
