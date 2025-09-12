# views/projects.py
import tkinter as tk
import logging
from db import supabase  # global client

def projects_view(content_frame, user_id):
    # Clear frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="📂 My Projects", font=("Helvetica", 16, "bold"), bg="#ecf0f1").pack(pady=20)

    projects_frame = tk.Frame(content_frame, bg="#ecf0f1")
    projects_frame.pack(fill="both", expand=True)

    try:
        logging.info("Fetching user projects from Supabase...")

        response = (
            supabase
            .table("projects")
            .select(
                "id, title, status, "
                "applications!inner(freelancer_id), "
                "tasks(id, status)"
            )
            .in_("status", ["in_progress", "completed"])
            .execute()
        )

        projects = []
        if response.data:
            for proj in response.data:
                applied = any(app["freelancer_id"] == user_id for app in proj.get("applications", []))
                has_tasks = bool(proj.get("tasks"))

                if applied or has_tasks:
                    projects.append(proj)

        if not projects:
            tk.Label(
                projects_frame,
                text="No active or completed projects.",
                font=("Helvetica", 12),
                bg="#ecf0f1"
            ).pack(pady=10)
            return

        listbox = tk.Listbox(projects_frame, height=12, font=("Helvetica", 12))
        listbox.pack(fill="both", expand=True, padx=20, pady=10)

        for proj in projects:
            title = proj.get("title", "Untitled Project")
            status = proj.get("status", "Unknown")
            listbox.insert("end", f"• {title}  [{status}]")

    except Exception as e:
        logging.exception("Error fetching projects")
        tk.Label(
            projects_frame,
            text=f"Error fetching projects: {e}",
            font=("Helvetica", 12),
            fg="red",
            bg="#ecf0f1"
        ).pack(pady=10)
