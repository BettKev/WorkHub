# views/projects.py
import tkinter as tk
import logging
from db import supabase  # global client


def projects_view(content_frame, user_id):
    # Clear frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # === HEADER ===
    header = tk.Label(
        content_frame,
        text="📂 My Projects",
        font=("Helvetica", 18, "bold"),
        bg="#ecf0f1",
        fg="#2c3e50"
    )
    header.pack(pady=20, anchor="w", padx=20)

    projects_frame = tk.Frame(content_frame, bg="#ecf0f1")
    projects_frame.pack(fill="both", expand=True, padx=20, pady=10)

    try:
        logging.info("Fetching projects linked to freelancer %s...", user_id)

        # Fetch projects where user has applied and been linked
        response = (
            supabase
            .table("projects")
            .select("id, name, description, status, created_at, applications!inner(freelancer_id)")
            .in_("status", ["Not Started", "In Progress", "Completed"])
            .eq("applications.freelancer_id", user_id)
            .execute()
        )

        projects = response.data or []

        if not projects:
            tk.Label(
                projects_frame,
                text="You have no linked projects yet.",
                font=("Helvetica", 12, "italic"),
                bg="#ecf0f1",
                fg="#7f8c8d"
            ).pack(pady=15)
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

        # --- Render projects ---
        for proj in projects:
            name = proj.get("name", "Untitled Project")
            status = proj.get("status", "Unknown")
            desc = proj.get("description", "No description provided.")
            created_at = proj.get("created_at", "")

            card = tk.Frame(
                scroll_frame,
                bg="white",
                bd=2,
                relief="groove",
                padx=15,
                pady=12
            )
            card.pack(fill="x", pady=8, padx=5)

            # Top row (name + status badge)
            top_row = tk.Frame(card, bg="white")
            top_row.pack(fill="x")

            tk.Label(
                top_row,
                text=name,
                font=("Helvetica", 13, "bold"),
                bg="white",
                fg="#2c3e50"
            ).pack(side="left", anchor="w")

            tk.Label(
                top_row,
                text=status,
                font=("Helvetica", 9, "bold"),
                bg=status_colors.get(status, "#bdc3c7"),
                fg="white",
                padx=10, pady=3
            ).pack(side="right", anchor="e")

            # Description
            tk.Label(
                card,
                text=desc,
                font=("Helvetica", 10),
                bg="white",
                fg="#34495e",
                wraplength=500,
                justify="left"
            ).pack(anchor="w", pady=(6, 4))

            # Metadata row
            meta = f"📅 Created: {created_at}   |   🆔 ID: {proj.get('id')}"
            tk.Label(
                card,
                text=meta,
                font=("Helvetica", 9, "italic"),
                bg="white",
                fg="#7f8c8d"
            ).pack(anchor="w", pady=(0, 6))

            # --- Button row ---
            btn_row = tk.Frame(card, bg="white")
            btn_row.pack(anchor="e", pady=(5, 0))

            def open_project(pid=proj["id"]):
                logging.info(f"Opening project {pid}")
                # TODO: integrate project detail view

            def view_tasks(pid=proj["id"]):
                logging.info(f"Viewing tasks for project {pid}")
                # TODO: integrate tasks view

            def mark_completed(pid=proj["id"]):
                try:
                    supabase.table("projects").update({"status": "Completed"}).eq("id", pid).execute()
                    logging.info(f"Marked project {pid} as Completed")
                    tk.Label(card, text="✅ Marked as Completed",
                             font=("Helvetica", 9, "bold"),
                             bg="white", fg="#27ae60").pack(anchor="e", pady=3)
                except Exception as e:
                    logging.exception("Error marking project completed")
                    tk.Label(card, text=f"❌ Error: {e}",
                             font=("Helvetica", 9),
                             bg="white", fg="red").pack(anchor="e", pady=3)

            for text, cmd, color in [
                ("Open", open_project, "#2980b9"),
                ("View Tasks", view_tasks, "#8e44ad"),
                ("Mark Completed", mark_completed, "#27ae60"),
            ]:
                tk.Button(
                    btn_row,
                    text=text,
                    command=cmd,
                    bg=color,
                    fg="white",
                    font=("Helvetica", 9, "bold"),
                    relief="flat",
                    padx=8, pady=4
                ).pack(side="right", padx=5)

    except Exception as e:
        logging.exception("Error fetching projects")
        tk.Label(
            projects_frame,
            text=f"❌ Error fetching projects: {e}",
            font=("Helvetica", 12),
            fg="red",
            bg="#ecf0f1"
        ).pack(pady=10)
