# views/dashboard.py
import tkinter as tk
import logging
from db import supabase

def dashboard_view(content_frame, user_id, user_email=None):
    for widget in content_frame.winfo_children():
        widget.destroy()

    # === HEADER ===
    header = tk.Frame(content_frame, bg="#2980b9", height=80)
    header.pack(fill="x")
    tk.Label(
        header, text="📊 Dashboard Overview",
        font=("Helvetica", 18, "bold"),
        fg="white", bg="#2980b9"
    ).pack(pady=20, padx=20, anchor="w")

    # === STATS GRID ===
    stats_frame = tk.Frame(content_frame, bg="#ecf0f1")
    stats_frame.pack(fill="x", pady=15, padx=20)

    stats = {
        "Active Projects": 0,
        "Completed Tasks": 0,
        "Earnings ($)": 0,
        "Unread Messages": 0,
        "Rating": "N/A",
    }

    try:
        # Step 1: Get project IDs where user has an accepted application
        resp = supabase.table("applications") \
            .select("project_id") \
            .eq("freelancer_id", user_id) \
            .eq("status", "accepted") \
            .execute()

        accepted_project_ids = [app["project_id"] for app in resp.data or []]

        # Step 2: Count only projects that are still active
        if accepted_project_ids:
            resp = supabase.table("projects") \
                .select("id") \
                .in_("id", accepted_project_ids) \
                .eq("status", "In Progress") \
                .execute()
            stats["Active Projects"] = len(resp.data or [])
        else:
            stats["Active Projects"] = 0


        # Completed tasks
        try:
            # Step 1: get all project_ids where freelancer has an accepted application
            apps_resp = (
                supabase.table("applications")
                .select("project_id")
                .eq("freelancer_id", user_id)
                .eq("status", "accepted")
                .execute()
            )
            project_ids = [app["project_id"] for app in (apps_resp.data or [])]

            completed_count = 0
            if project_ids:
                # Step 2: get completed tasks for those projects
                tasks_resp = (
                    supabase.table("tasks")
                    .select("id")
                    .in_("project_id", project_ids)
                    .eq("status", "done")
                    .execute()
                )
                completed_count = len(tasks_resp.data or [])

            stats["Completed Tasks"] = completed_count

        except Exception:
            logging.exception("Error fetching completed tasks")


        # Earnings
        try:
            # Step 1: get all project_ids where freelancer has an accepted application
            apps_resp = (
                supabase.table("applications")
                .select("project_id")
                .eq("freelancer_id", user_id)
                .eq("status", "accepted")
                .execute()
            )
            project_ids = [str(app["project_id"]) for app in (apps_resp.data or [])]

            total_earnings = 0
            if project_ids:
                # Step 2: sum earnings from transactions/payments for those projects
                tx_resp = (
                    supabase.table("transactions")
                    .select("amount, type, project_id")
                    .in_("project_id", project_ids)
                    .eq("type", "credit")   # ✅ only credits count as earnings
                    .execute()
                )

                total_earnings = sum(
                    t.get("amount", 0) for t in (tx_resp.data or []) if t.get("amount")
                )

            stats["Earnings ($)"] = total_earnings

        except Exception:
            logging.exception("Error fetching earnings")


        # Unread messages
        resp = supabase.table("messages").select("id").eq("receiver_id", user_id).eq("is_read", False).execute()
        stats["Unread Messages"] = len(resp.data or [])

        # Rating
        resp = supabase.table("profiles").select("rating").eq("id", user_id).single().execute()
        if resp.data and resp.data.get("rating"):
            stats["Rating"] = f"{resp.data['rating']} ⭐"

    except Exception:
        logging.exception("Error fetching stats")

    for idx, (key, value) in enumerate(stats.items()):
        stat_box = tk.Frame(stats_frame, bg="white", bd=2, relief="groove", padx=20, pady=15)
        stat_box.grid(row=0, column=idx, padx=10, sticky="nsew")

        tk.Label(stat_box, text=key, font=("Helvetica", 12, "bold"),
                 fg="#34495e", bg="white").pack()
        tk.Label(stat_box, text=str(value), font=("Helvetica", 14),
                 fg="#27ae60", bg="white").pack()

    for i in range(len(stats)):
        stats_frame.grid_columnconfigure(i, weight=1)

    # === MAIN BOTTOM SPLIT (Recent Activity | Advertised Projects) ===
    bottom_frame = tk.Frame(content_frame, bg="#ecf0f1")
    bottom_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    bottom_frame.grid_rowconfigure(0, weight=1)   # ✅ allow row to expand
    bottom_frame.grid_columnconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(1, weight=1)

    # --- Scrollable Section Factory ---
    def make_scrollable_section(parent, title, height=300):
        outer = tk.Frame(parent, bg="white", bd=2, relief="groove", height=height)
        outer.grid_propagate(False)  # ✅ allow fixed height
        outer.pack_propagate(False)

        tk.Label(
            outer, text=title,
            font=("Helvetica", 14, "bold"),
            bg="white", fg="#2c3e50"
        ).pack(anchor="w", padx=15, pady=10)

        container = tk.Frame(outer, bg="white")
        container.pack(fill="both", expand=True, padx=10, pady=5)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="white")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return outer, scroll_frame

    # === RECENT ACTIVITY (left) ===
    activity_frame, activity_scroll = make_scrollable_section(bottom_frame, "🕒 Recent Activity")
    activity_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)

    # === ADVERTISED PROJECTS (right) ===
    projects_frame, projects_scroll = make_scrollable_section(bottom_frame, "📢 Advertised Projects")
    projects_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)


    loading_label = tk.Label(
        projects_scroll, text="Loading available projects...",
        font=("Helvetica", 11, "italic"), bg="white", fg="#7f8c8d"
    )
    loading_label.pack(pady=10)

    def load_projects():
        try:
            response = supabase.table("projects").select("*").eq("status", "Not Started").order("created_at", desc=True).execute()
            projects = response.data or []

            if not projects:
                loading_label.config(text="No advertised projects right now.")
                return

            loading_label.destroy()

            for proj in projects:
                proj_box = tk.Frame(projects_scroll, bg="#ecf0f1", bd=1, relief="solid", padx=15, pady=10)
                proj_box.pack(fill="x", padx=15, pady=5)

                tk.Label(proj_box, text=proj.get("name", "Untitled"),
                         font=("Helvetica", 12, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(anchor="w")
                tk.Label(proj_box, text=f"Budget: ${proj.get('budget', 'N/A')}",
                         font=("Helvetica", 10), bg="#ecf0f1", fg="#27ae60").pack(anchor="w", pady=2)
                tk.Label(proj_box, text=f"Description: {proj.get('description', 'No description')}",
                         font=("Helvetica", 10), bg="#ecf0f1", fg="#34495e", wraplength=350, justify="left").pack(anchor="w", pady=2)

                tags = proj.get("tags", [])
                if tags:
                    tk.Label(proj_box, text="Tags: " + ", ".join(tags),
                             font=("Helvetica", 9), bg="#ecf0f1", fg="#7f8c8d").pack(anchor="w")

                def apply_to_project(project_id=proj["id"]):
                    try:
                        supabase.table("applications").insert({
                            "project_id": project_id,
                            "freelancer_id": user_id
                        }).execute()
                        logging.info(f"User {user_id} applied to project {project_id}")
                        tk.Label(proj_box, text="✅ Applied!",
                                 font=("Helvetica", 10, "bold"),
                                 bg="#ecf0f1", fg="green").pack(anchor="e")
                    except Exception as e:
                        logging.exception("Error applying to project")
                        tk.Label(proj_box, text=f"❌ Error: {e}",
                                 font=("Helvetica", 10),
                                 bg="#ecf0f1", fg="red").pack(anchor="e")

                tk.Button(proj_box, text="Apply",
                          bg="#2980b9", fg="white",
                          font=("Helvetica", 10, "bold"),
                          relief="flat", padx=10, pady=5,
                          command=apply_to_project).pack(anchor="e", pady=5)

        except Exception as e:
            logging.exception("Error loading advertised projects")
            loading_label.config(text=f"❌ Error loading projects: {e}", fg="red")

    content_frame.after(500, load_projects)
