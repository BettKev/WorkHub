# views/projects.py
import tkinter as tk
import logging
from db import supabase  # global client


def projects_view(content_frame, user_id):
    # Clear frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(
        content_frame,
        text="📂 My Projects",
        font=("Helvetica", 16, "bold"),
        bg="#ecf0f1"
    ).pack(pady=20)

    projects_frame = tk.Frame(content_frame, bg="#ecf0f1")
    projects_frame.pack(fill="both", expand=True, padx=20, pady=10)

    try:
        logging.info("Fetching projects linked to freelancer %s...", user_id)

        # Include Not Started, In Progress, and Completed
        response = (
            supabase
            .table("projects")
            .select("id, name, status, applications!inner(freelancer_id)")
            .in_("status", ["Not Started", "In Progress", "Completed"])
            .eq("applications.freelancer_id", user_id)
            .execute()
        )

        projects = response.data or []

        if not projects:
            tk.Label(
                projects_frame,
                text="You have no linked projects yet.",
                font=("Helvetica", 12),
                bg="#ecf0f1"
            ).pack(pady=10)
            return

        # --- Scrollable container ---
        canvas = tk.Canvas(projects_frame, bg="#ecf0f1", highlightthickness=0)
        scrollbar = tk.Scrollbar(projects_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#ecf0f1")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Status colors ---
        status_colors = {
            "Not Started": "#7f8c8d",   # gray
            "In Progress": "#e67e22",   # orange
            "Completed": "#27ae60",     # green
        }

        for proj in projects:
            name = proj.get("name", "Untitled Project")
            status = proj.get("status", "Unknown")

            item_frame = tk.Frame(scroll_frame, bg="white", bd=1, relief="solid", padx=10, pady=8)
            item_frame.pack(fill="x", pady=5)

            tk.Label(
                item_frame,
                text=name,
                font=("Helvetica", 12, "bold"),
                bg="white",
                fg="#2c3e50"
            ).pack(side="left", anchor="w")

            tk.Label(
                item_frame,
                text=status,
                font=("Helvetica", 10, "bold"),
                bg=status_colors.get(status, "#bdc3c7"),
                fg="white",
                padx=8, pady=2
            ).pack(side="right")

    except Exception as e:
        logging.exception("Error fetching projects")
        tk.Label(
            projects_frame,
            text=f"Error fetching projects: {e}",
            font=("Helvetica", 12),
            fg="red",
            bg="#ecf0f1"
        ).pack(pady=10)
