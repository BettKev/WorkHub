import tkinter as tk
import random
from datetime import datetime

def dashboard_view(content_frame):
    # Clear old content
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
        "Active Projects": random.randint(1, 10),
        "Completed Tasks": random.randint(10, 50),
        "Earnings ($)": random.randint(200, 2000),
        "Pending Tasks": random.randint(1, 15),
        "Messages": random.randint(0, 10),
        "Rating": f"{round(random.uniform(3.5, 5.0), 1)} ⭐",
    }

    for idx, (key, value) in enumerate(stats.items()):
        stat_box = tk.Frame(stats_frame, bg="white", bd=2, relief="groove", padx=20, pady=15)
        stat_box.grid(row=0, column=idx, padx=10, sticky="nsew")

        tk.Label(stat_box, text=key, font=("Helvetica", 12, "bold"), fg="#34495e", bg="white").pack()
        tk.Label(stat_box, text=str(value), font=("Helvetica", 14), fg="#27ae60", bg="white").pack()

    # Make columns expand evenly
    for i in range(len(stats)):
        stats_frame.grid_columnconfigure(i, weight=1)

    # === RECENT ACTIVITY ===
    activity_frame = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
    activity_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    tk.Label(
        activity_frame, text="🕒 Recent Activity",
        font=("Helvetica", 14, "bold"),
        bg="white", fg="#2c3e50"
    ).pack(anchor="w", padx=15, pady=10)

    # Mock activity data
    activities = [
        f"Completed task 'UI Fix' in Project Alpha ({datetime.now().strftime('%H:%M')})",
        f"Received message from Client X ({datetime.now().strftime('%H:%M')})",
        f"Updated profile bio ({datetime.now().strftime('%H:%M')})",
        f"Added new skill: Python ({datetime.now().strftime('%H:%M')})",
    ]

    for act in activities:
        tk.Label(
            activity_frame, text="• " + act,
            font=("Helvetica", 11), bg="white", anchor="w", justify="left"
        ).pack(fill="x", padx=20, pady=2)

    # === QUICK ACTIONS ===
    actions_frame = tk.Frame(content_frame, bg="#ecf0f1")
    actions_frame.pack(fill="x", pady=(0, 20), padx=20)

    tk.Label(
        actions_frame, text="⚡ Quick Actions",
        font=("Helvetica", 14, "bold"),
        bg="#ecf0f1", fg="#2c3e50"
    ).pack(anchor="w", pady=(10, 5))

    buttons_frame = tk.Frame(actions_frame, bg="#ecf0f1")
    buttons_frame.pack(fill="x", padx=10)

    quick_actions = ["Create Project", "View Messages", "Update Profile", "Check Earnings"]
    for action in quick_actions:
        tk.Button(
            buttons_frame, text=action,
            bg="#2980b9", fg="white", font=("Helvetica", 11, "bold"),
            relief="flat", padx=15, pady=8
        ).pack(side="left", padx=10, pady=10)
import tkinter as tk
import random
from datetime import datetime

def dashboard_view(content_frame):
    # Clear old content
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
        "Active Projects": random.randint(1, 10),
        "Completed Tasks": random.randint(10, 50),
        "Earnings ($)": random.randint(200, 2000),
        "Pending Tasks": random.randint(1, 15),
        "Messages": random.randint(0, 10),
        "Rating": f"{round(random.uniform(3.5, 5.0), 1)} ⭐",
    }

    for idx, (key, value) in enumerate(stats.items()):
        stat_box = tk.Frame(stats_frame, bg="white", bd=2, relief="groove", padx=20, pady=15)
        stat_box.grid(row=0, column=idx, padx=10, sticky="nsew")

        tk.Label(stat_box, text=key, font=("Helvetica", 12, "bold"), fg="#34495e", bg="white").pack()
        tk.Label(stat_box, text=str(value), font=("Helvetica", 14), fg="#27ae60", bg="white").pack()

    # Make columns expand evenly
    for i in range(len(stats)):
        stats_frame.grid_columnconfigure(i, weight=1)

    # === RECENT ACTIVITY ===
    activity_frame = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
    activity_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    tk.Label(
        activity_frame, text="🕒 Recent Activity",
        font=("Helvetica", 14, "bold"),
        bg="white", fg="#2c3e50"
    ).pack(anchor="w", padx=15, pady=10)

    # Mock activity data
    activities = [
        f"Completed task 'UI Fix' in Project Alpha ({datetime.now().strftime('%H:%M')})",
        f"Received message from Client X ({datetime.now().strftime('%H:%M')})",
        f"Updated profile bio ({datetime.now().strftime('%H:%M')})",
        f"Added new skill: Python ({datetime.now().strftime('%H:%M')})",
    ]

    for act in activities:
        tk.Label(
            activity_frame, text="• " + act,
            font=("Helvetica", 11), bg="white", anchor="w", justify="left"
        ).pack(fill="x", padx=20, pady=2)

    # === QUICK ACTIONS ===
    actions_frame = tk.Frame(content_frame, bg="#ecf0f1")
    actions_frame.pack(fill="x", pady=(0, 20), padx=20)

    tk.Label(
        actions_frame, text="⚡ Quick Actions",
        font=("Helvetica", 14, "bold"),
        bg="#ecf0f1", fg="#2c3e50"
    ).pack(anchor="w", pady=(10, 5))

    buttons_frame = tk.Frame(actions_frame, bg="#ecf0f1")
    buttons_frame.pack(fill="x", padx=10)

    quick_actions = ["Create Project", "View Messages", "Update Profile", "Check Earnings"]
    for action in quick_actions:
        tk.Button(
            buttons_frame, text=action,
            bg="#2980b9", fg="white", font=("Helvetica", 11, "bold"),
            relief="flat", padx=15, pady=8
        ).pack(side="left", padx=10, pady=10)

    # === SUGGESTED PROJECTS (AI Filtered) ===
    projects_frame = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
    projects_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    tk.Label(
        projects_frame, text="🤖 Suggested Projects for You",
        font=("Helvetica", 14, "bold"),
        bg="white", fg="#2c3e50"
    ).pack(anchor="w", padx=15, pady=10)

    # Loading text first
    loading_label = tk.Label(
        projects_frame, text="Loading AI suggestions...",
        font=("Helvetica", 11, "italic"), bg="white", fg="#7f8c8d"
    )
    loading_label.pack(pady=10)

    def load_projects():
        loading_label.destroy()

        # Mock project advertisements
        all_projects = [
            {"title": "Build a Django REST API", "budget": "$500", "tags": ["Python", "API"]},
            {"title": "Design a Portfolio Website", "budget": "$300", "tags": ["HTML", "CSS", "UI"]},
            {"title": "Machine Learning Model for Sales Prediction", "budget": "$800", "tags": ["AI", "ML", "Python"]},
            {"title": "React Dashboard for Analytics", "budget": "$600", "tags": ["React", "Frontend"]},
        ]

        # Mock AI filter (e.g., user is strong in Python/AI)
        suggested = [p for p in all_projects if "Python" in p["tags"] or "AI" in p["tags"]]

        for proj in suggested:
            proj_box = tk.Frame(projects_frame, bg="#ecf0f1", bd=1, relief="solid", padx=15, pady=10)
            proj_box.pack(fill="x", padx=15, pady=5)

            tk.Label(proj_box, text=proj["title"], font=("Helvetica", 12, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(anchor="w")
            tk.Label(proj_box, text=f"Budget: {proj['budget']}", font=("Helvetica", 10), bg="#ecf0f1", fg="#27ae60").pack(anchor="w", pady=2)
            tk.Label(proj_box, text="Tags: " + ", ".join(proj["tags"]), font=("Helvetica", 9), bg="#ecf0f1", fg="#7f8c8d").pack(anchor="w")

            tk.Button(
                proj_box, text="Apply",
                bg="#2980b9", fg="white", font=("Helvetica", 10, "bold"),
                relief="flat", padx=10, pady=5
            ).pack(anchor="e", pady=5)

    # Simulate async loading with after()
    content_frame.after(1500, load_projects)
