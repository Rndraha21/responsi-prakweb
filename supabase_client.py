import os
from dotenv import load_dotenv
from supabase import create_client, ClientOptions
import httpx

load_dotenv()

transport = httpx.HTTPTransport(http2=False)

httpx_client = httpx.Client(transport=transport, timeout=10.0)
options = ClientOptions(httpx_client=httpx_client)

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

supabase = create_client(url, key, options)
