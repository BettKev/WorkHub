# windows/signup.py
import tkinter as tk
from tkinter import messagebox
import logging
from db import supabase

def signup_window(root):
    root.withdraw()  # hide root

    win = tk.Toplevel(root)
    win.title("Sign Up")
    win.geometry("400x300")
    win.grab_set()

    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Name:").pack(anchor="w")
    entry_name = tk.Entry(frame, width=40)
    entry_name.pack(pady=5)

    tk.Label(frame, text="Email:").pack(anchor="w")
    entry_email = tk.Entry(frame, width=40)
    entry_email.pack(pady=5)

    tk.Label(frame, text="Password:").pack(anchor="w")
    entry_password = tk.Entry(frame, show="*", width=40)
    entry_password.pack(pady=5)

    def handle_signup():
        email = entry_email.get()
        password = entry_password.get()
        name = entry_name.get()

        try:
            logging.info(f"Attempting signup for {email}")
            user = supabase.auth.sign_up({"email": email, "password": password})
            logging.debug(f"Signup response: {user}")

            if user and user.user:
                try:
                    supabase.table("profiles").insert({
                        "id": user.user.id,
                        "name": name,
                        "skills": []
                    }).execute()
                except Exception as db_err:
                    logging.warning(f"Profile insert failed: {db_err}")
                messagebox.showinfo("Signup", "Account created successfully!")
                win.destroy()
                root.deiconify()
            else:
                messagebox.showerror("Signup", "Signup failed.")
        except Exception as e:
            logging.exception("Signup error")
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Sign Up", command=handle_signup).pack(pady=10)

    def on_close():
        win.destroy()
        root.deiconify()

    win.protocol("WM_DELETE_WINDOW", on_close)
