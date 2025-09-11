import tkinter as tk
import logging
from dotenv import load_dotenv
from supabase import create_client, Client
import os

# Import windows
from windows.login import login_window
from windows.signup import signup_window

# --- Setup Logging ---
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

# --- Load environment ---
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    logging.error("Missing SUPABASE_URL or SUPABASE_KEY in environment!")

supabase: Client = create_client(url, key)

# --- Global Tkinter Root ---
root = tk.Tk()
root.title("WorkHub")
root.geometry("600x300")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True, fill="both")

tk.Label(
    frame,
    text="WorkHub",
    font=("Helvetica", 50, "bold"),
    wraplength=350,
    justify="center"
).pack(pady=20)

# Pass root + supabase client to windows
tk.Button(
    frame,
    text="Login",
    width=20,
    font=("Gothic", 12),
    command=lambda: login_window(root, supabase)
).pack(pady=5)

tk.Button(frame,
          text="Sign Up",
          width=20,
          font=("Gothic", 12),
          command=lambda: signup_window(root, supabase)
).pack(pady=5)

root.mainloop()
