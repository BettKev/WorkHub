import tkinter as tk
from tkinter import messagebox
import logging
from .dashboard import open_dashboard

def login_window(root, supabase):
    # Close root when opening login
    root.withdraw()  

    win = tk.Toplevel(root)
    win.title("Login")
    win.geometry("400x250")
    win.grab_set()

    frame = tk.Frame(win, padx=20, pady=20)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Email:").pack(anchor="w")
    entry_email = tk.Entry(frame, width=40)
    entry_email.pack(pady=5)

    tk.Label(frame, text="Password:").pack(anchor="w")
    entry_password = tk.Entry(frame, show="*", width=40)
    entry_password.pack(pady=5)

    def handle_login():
        email = entry_email.get()
        password = entry_password.get()

        try:
            logging.info(f"Attempting login for {email}")
            user = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            logging.debug(f"Login response: {user}")

            if user and user.user:
                # messagebox.showinfo("Login", "Login successful!")
                win.destroy()
                open_dashboard(root, user.user.email, supabase, user.user.id)  # go to dashboard
            else:
                messagebox.showerror("Login", "Login failed.")
        except Exception as e:
            logging.exception("Login error")
            messagebox.showerror("Error", str(e))

    tk.Button(frame, text="Login", command=handle_login).pack(pady=10)

    # If login window is closed without logging in → show root again
    def on_close():
        win.destroy()
        root.deiconify()

    win.protocol("WM_DELETE_WINDOW", on_close)
