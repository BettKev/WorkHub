# views/settings.py
import tkinter as tk

def settings_view(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="⚙️ Settings", font=("Helvetica", 16, "bold"), bg="#ecf0f1").pack(pady=20)
    tk.Label(content_frame, text="(Settings page coming soon...)", font=("Helvetica", 12), bg="#ecf0f1").pack()
