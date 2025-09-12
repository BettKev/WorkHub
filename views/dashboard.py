# views/dashboard.py
import tkinter as tk
import logging
import threading
from db import supabase
from ai.agent import AIAgent
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    logging.warning("GOOGLE_API_KEY not set in .env, using stub responses for AI agent.")
    api_key = None

# Initialize AI agent
agent = AIAgent(api_key)


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
        # Step 1: Projects user is accepted in
        resp = supabase.table("applications") \
            .select("project_id") \
            .eq("freelancer_id", user_id) \
            .eq("status", "accepted") \
            .execute()

        accepted_project_ids = [app["project_id"] for app in resp.data or []]

        # Step 2: Active projects
        if accepted_project_ids:
            resp = supabase.table("projects") \
                .select("id") \
                .in_("id", accepted_project_ids) \
                .eq("status", "In Progress") \
                .execute()
            stats["Active Projects"] = len(resp.data or [])

        # Completed tasks
        if accepted_project_ids:
            tasks_resp = (
                supabase.table("tasks")
                .select("id")
                .in_("project_id", accepted_project_ids)
                .eq("status", "done")
                .execute()
            )
            stats["Completed Tasks"] = len(tasks_resp.data or [])

        # Earnings
        if accepted_project_ids:
            tx_resp = (
                supabase.table("transactions")
                .select("amount, type, project_id")
                .in_("project_id", accepted_project_ids)
                .eq("type", "credit")
                .execute()
            )
            stats["Earnings ($)"] = sum(
                t.get("amount", 0) for t in (tx_resp.data or []) if t.get("amount")
            )

        # Unread messages
        resp = supabase.table("messages").select("id") \
            .eq("receiver_id", user_id).eq("is_read", False).execute()
        stats["Unread Messages"] = len(resp.data or [])

        # Rating
        resp = supabase.table("profiles").select("rating") \
            .eq("id", user_id).single().execute()
        if resp.data and resp.data.get("rating"):
            stats["Rating"] = f"{resp.data['rating']} ⭐"

    except Exception:
        logging.exception("Error fetching stats")

    # Render stats
    for idx, (key, value) in enumerate(stats.items()):
        stat_box = tk.Frame(stats_frame, bg="white", bd=2, relief="groove", padx=20, pady=15)
        stat_box.grid(row=0, column=idx, padx=10, sticky="nsew")

        tk.Label(stat_box, text=key, font=("Helvetica", 12, "bold"),
                 fg="#34495e", bg="white").pack()
        tk.Label(stat_box, text=str(value), font=("Helvetica", 14),
                 fg="#27ae60", bg="white").pack()

    for i in range(len(stats)):
        stats_frame.grid_columnconfigure(i, weight=1)

    # === MAIN BOTTOM SPLIT ===
    bottom_frame = tk.Frame(content_frame, bg="#ecf0f1")
    bottom_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    bottom_frame.grid_rowconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(1, weight=1)

    def make_scrollable_section(parent, title, height=300):
        outer = tk.Frame(parent, bg="white", bd=2, relief="groove", height=height)
        outer.grid_propagate(False)
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

    # === RECENT ACTIVITY ===
    activity_frame, activity_scroll = make_scrollable_section(bottom_frame, "🕒 Recent Activity")
    activity_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)

    # === ADVERTISED PROJECTS ===
    projects_frame, projects_scroll = make_scrollable_section(bottom_frame, "📢 Advertised Projects")
    projects_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)

    # === FLOATING AI ASSISTANT (Chat with bubbles) ===
    def open_ai_popup():
        popup = tk.Toplevel(content_frame)
        popup.title("🤖 AI Assistant")
        popup.geometry("400x500")
        popup.configure(bg="white")

        tk.Label(
            popup, text="🤖 AI Assistant",
            font=("Helvetica", 14, "bold"),
            bg="white", fg="#2c3e50"
        ).pack(anchor="w", padx=15, pady=10)

        # Scrollable chat area
        chat_frame = tk.Frame(popup, bg="white")
        chat_frame.pack(fill="both", expand=True, padx=10, pady=5)

        canvas = tk.Canvas(chat_frame, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
        messages_frame = tk.Frame(canvas, bg="white")

        messages_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=messages_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Input area
        input_frame = tk.Frame(popup, bg="white")
        input_frame.pack(fill="x", side="bottom", pady=5)

        user_input = tk.Entry(input_frame, font=("Helvetica", 10))
        user_input.pack(side="left", fill="x", expand=True, padx=(0, 5))

        def add_message(text, role="user"):
            bubble = tk.Frame(messages_frame, bg="white")
            bubble.pack(anchor="e" if role == "user" else "w", pady=4, padx=5, fill="x")

            if role == "user":
                lbl = tk.Label(
                    bubble, text=f"👤 {text}",
                    bg="#d0e6ff", fg="#2c3e50",
                    font=("Helvetica", 10), wraplength=250,
                    justify="left", padx=10, pady=5, bd=0,
                    relief="solid"
                )
                lbl.pack(anchor="e")
            elif role == "ai":
                lbl = tk.Label(
                    bubble, text=f"🤖 {text}",
                    bg="#e8f5e9", fg="#2c3e50",
                    font=("Helvetica", 10, "italic"), wraplength=250,
                    justify="left", padx=10, pady=5, bd=0,
                    relief="solid"
                )
                lbl.pack(anchor="w")
            elif role == "system":
                lbl = tk.Label(
                    bubble, text=text,
                    bg="#f0f0f0", fg="#7f8c8d",
                    font=("Helvetica", 9, "italic"),
                    wraplength=250, padx=10, pady=5
                )
                lbl.pack(anchor="c")

            canvas.update_idletasks()
            canvas.yview_moveto(1.0)

            return bubble

        def send_message(event=None):
            msg = user_input.get().strip()
            if not msg:
                return
            user_input.delete(0, tk.END)

            add_message(msg, role="user")
            thinking_bubble = add_message("thinking...", role="system")

            def fetch_response():
                reply = agent.query_gemini(msg)
                thinking_bubble.destroy()
                add_message(reply, role="ai")

            threading.Thread(target=fetch_response, daemon=True).start()

        tk.Button(
            input_frame, text="Send", command=send_message,
            bg="#2980b9", fg="white",
            font=("Helvetica", 10, "bold"),
            relief="flat", padx=12, pady=5
        ).pack(side="right")

        user_input.bind("<Return>", send_message)

    float_btn = tk.Button(
        content_frame, text="💬", command=open_ai_popup,
        bg="#2980b9", fg="white",
        font=("Helvetica", 16, "bold"),
        bd=0, relief="flat", width=3, height=1
    )
    float_btn.place(relx=0.95, rely=0.9, anchor="center")

    # === LOAD RECENT ACTIVITY ===
    def load_activity():
        try:
            if not accepted_project_ids:
                tk.Label(activity_scroll, text="No recent activity.",
                         font=("Helvetica", 11, "italic"),
                         bg="white", fg="#7f8c8d").pack(pady=10)
                return

            tasks_resp = (
                supabase.table("tasks")
                .select("id, title, status, project_id, created_at")
                .in_("project_id", accepted_project_ids)
                .order("created_at", desc=True)
                .limit(30)
                .execute()
            )
            tasks = tasks_resp.data or []

            if not tasks:
                tk.Label(activity_scroll, text="No recent tasks.",
                         font=("Helvetica", 11, "italic"),
                         bg="white", fg="#7f8c8d").pack(pady=10)
                return

            status_colors = {
                "done": "#27ae60",
                "in progress": "#e67e22",
                "not started": "#7f8c8d"
            }

            for t in tasks:
                task_box = tk.Frame(activity_scroll, bg="#f9f9f9", bd=1, relief="solid", padx=10, pady=5)
                task_box.pack(fill="x", padx=10, pady=4)

                title = t.get("title", "Untitled Task")
                status = (t.get("status") or "").lower()
                created = t.get("created_at", "")

                tk.Label(task_box,
                         text=f"📝 {title}",
                         font=("Helvetica", 10, "bold"),
                         bg="#f9f9f9", fg="#2c3e50",
                         wraplength=350, justify="left").pack(anchor="w")

                color = status_colors.get(status, "#34495e")
                tk.Label(task_box,
                         text=f"Status: {status.title()} | {created}",
                         font=("Helvetica", 9, "italic"),
                         bg="#f9f9f9", fg=color).pack(anchor="e")
        except Exception:
            logging.exception("Error loading recent activity")
            tk.Label(activity_scroll, text="❌ Error loading activity.",
                     font=("Helvetica", 11), fg="red", bg="white").pack(pady=10)

    # === LOAD ADVERTISED PROJECTS ===
    loading_label = tk.Label(
        projects_scroll, text="Loading available projects...",
        font=("Helvetica", 11, "italic"), bg="white", fg="#7f8c8d"
    )
    loading_label.pack(pady=10)

    def load_projects():
        try:
            response = supabase.table("projects") \
                .select("*") \
                .eq("status", "Not Started") \
                .order("created_at", desc=True) \
                .execute()
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
                         font=("Helvetica", 10), bg="#ecf0f1", fg="#34495e",
                         wraplength=350, justify="left").pack(anchor="w", pady=2)

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

    # Schedule loaders
    content_frame.after(500, load_activity)
    content_frame.after(500, load_projects)
