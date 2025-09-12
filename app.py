# app.py
import tkinter as tk
import logging

# Import Supabase client
from db import supabase  

# Import windows
from windows.login import login_window
from windows.signup import signup_window

# --- Setup Logging ---
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

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

# Pass only root (supabase is global now)
tk.Button(
    frame,
    text="Login",
    width=20,
    font=("Gothic", 12),
    command=lambda: login_window(root)
).pack(pady=5)

tk.Button(
    frame,
    text="Sign Up",
    width=20,
    font=("Gothic", 12),
    command=lambda: signup_window(root)
).pack(pady=5)

root.mainloop()
