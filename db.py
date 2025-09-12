# db.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL") or "https://thkmxwkyuhxlwsgxllyg.supabase.co"
key = os.getenv("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRoa214d2t5dWh4bHdzZ3hsbHlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc1NDM1MjgsImV4cCI6MjA3MzExOTUyOH0.HzlNg7YIrGWvpp2l5dQfRzExNS6rq0fDvj2IHFzbpVg"

if not url or not key:
    raise ValueError("❌ Missing SUPABASE_URL or SUPABASE_KEY in environment")

supabase: Client = create_client(url, key)
