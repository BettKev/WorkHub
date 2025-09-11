import tkinter as tk
import logging

def projects_view(content_frame, supabase):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="📂 Projects", font=("Helvetica", 16, "bold"), bg="#ecf0f1").pack(pady=20)

    try:
        logging.info("Fetching projects from Supabase...")
        response = supabase.table("projects").select("*").execute()
        projects = response.data if response.data else []

        if not projects:
            tk.Label(content_frame, text="No projects found.", font=("Helvetica", 12), bg="#ecf0f1").pack(pady=10)
            return

        listbox = tk.Listbox(content_frame, height=12, font=("Helvetica", 12))
        listbox.pack(fill="both", expand=True, padx=20, pady=10)

        for proj in projects:
            name = proj.get("name", "Untitled Project")
            status = proj.get("status", "Unknown")
            listbox.insert("end", f"• {name}  [{status}]")

    except Exception as e:
        logging.exception("Error fetching projects")
        tk.Label(
            content_frame,
            text=f"Error fetching projects: {e}",
            font=("Helvetica", 12),
            fg="red",
            bg="#ecf0f1"
        ).pack(pady=10)
