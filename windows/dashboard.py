# windows/dashboard.py
import tkinter as tk
import platform
from views.dashboard import dashboard_view
from views.projects import projects_view
from views.profile import profile_view
from views.settings import settings_view
from db import supabase

def open_dashboard(root, user_email, user_id):
    root.withdraw()

    dash = tk.Toplevel(root)
    dash.title("Dashboard")
    dash.configure(bg="#ecf0f1")
    dash.grab_set()

     # === Fullscreen / Maximize ===
    system_platform = platform.system()
    if system_platform == "Windows":
        dash.state("zoomed")
    else:
        try:
            dash.attributes("-zoomed", True)  # Works on Linux (e.g., Ubuntu/Gnome)
        except tk.TclError:
            dash.attributes("-fullscreen", True)  # Fallback

    # Sidebar
    sidebar = tk.Frame(dash, bg="#2c3e50", width=200)
    sidebar.pack(side="left", fill="y")

    tk.Label(
        sidebar, text="Freelancer\nPlatform",
        font=("Helvetica", 14, "bold"), fg="white",
        bg="#2c3e50", pady=20
    ).pack()

    profile_frame = tk.Frame(sidebar, bg="#2c3e50")
    profile_frame.pack(pady=20)
    tk.Label(profile_frame, text="👤", font=("Helvetica", 30), bg="#2c3e50", fg="white").pack()
    tk.Label(
        profile_frame, text=user_email,
        font=("Helvetica", 10), bg="#2c3e50", fg="white",
        wraplength=180, justify="center"
    ).pack(pady=5)

    # Content area
    content_frame = tk.Frame(dash, bg="#ecf0f1")
    content_frame.pack(side="right", fill="both", expand=True)

    # Navigation
    nav_items = [
        ("🏠 Dashboard", lambda: dashboard_view(content_frame, user_id, user_email)),
        ("📂 Projects", lambda: projects_view(content_frame, user_id)),
        ("👤 Profile", lambda: profile_view(content_frame, user_email, user_id)),
        ("⚙️ Settings", lambda: settings_view(content_frame)),
    ]
    for text, command in nav_items:
        tk.Button(
            sidebar, text=text,
            font=("Helvetica", 12),
            fg="white", bg="#34495e",
            relief="flat", anchor="w", padx=20, pady=10,
            command=command
        ).pack(fill="x", pady=2)

    # Logout
    def logout():
        dash.destroy()
        root.deiconify()

    tk.Button(
        sidebar, text="🚪 Logout",
        font=("Helvetica", 12, "bold"),
        fg="white", bg="#e74c3c",
        relief="flat", anchor="w", padx=20, pady=10,
        command=logout
    ).pack(side="bottom", fill="x")

    # Default view
    dashboard_view(content_frame, user_id, user_email)

    dash.protocol("WM_DELETE_WINDOW", logout)
