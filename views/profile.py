# views/profile.py
import tkinter as tk
import logging
import json
from db import supabase


def profile_view(content_frame, user_email, user_id):
    # Clear frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Header bar
    header = tk.Frame(content_frame, bg="#2980b9", height=70)
    header.pack(fill="x")
    tk.Label(
        header, text="👤 Profile",
        font=("Helvetica", 18, "bold"),
        fg="white", bg="#2980b9"
    ).pack(pady=20, padx=20, anchor="w")

    # Loading placeholder
    loading_label = tk.Label(
        content_frame,
        text="⏳ Loading profile...",
        font=("Helvetica", 12, "italic"),
        bg="#ecf0f1", fg="#7f8c8d"
    )
    loading_label.pack(pady=40)

    def fetch_profile():
        try:
            response = (
                supabase.table("profiles")
                .select("*")
                .eq("id", user_id)
                .single()
                .execute()
            )
            profile = response.data or {}
            loading_label.destroy()

            # --- Profile Card (main container) ---
            card = tk.Frame(content_frame, bg="white", bd=0, highlightthickness=0)
            card.pack(padx=30, pady=30, fill="both", expand=True)

            # --- 2-column layout ---
            columns = tk.Frame(card, bg="white")
            columns.pack(fill="both", expand=True, padx=20, pady=20)

            left_col = tk.Frame(columns, bg="white")
            left_col.pack(side="left", fill="both", expand=True, padx=(0, 20))

            right_col = tk.Frame(columns, bg="white")
            right_col.pack(side="right", fill="both", expand=True)

            # --- Left column content ---
            # Avatar + name
            top = tk.Frame(left_col, bg="white")
            top.pack(fill="x", pady=10)

            avatar = profile.get("profile_image")
            avatar_label = tk.Label(
                top,
                text="👤" if not avatar else "",
                font=("Helvetica", 40),
                bg="#3498db", fg="white",
                width=4, height=2
            )
            avatar_label.pack(side="left", padx=15)

            name_area = tk.Frame(top, bg="white")
            name_area.pack(side="left", anchor="w", padx=10)
            tk.Label(
                name_area,
                text=profile.get("name", "Freelancer"),
                font=("Helvetica", 16, "bold"),
                bg="white", fg="#2c3e50"
            ).pack(anchor="w")
            tk.Label(
                name_area,
                text=profile.get("specialization", "No specialization"),
                font=("Helvetica", 12, "italic"),
                bg="white", fg="#7f8c8d"
            ).pack(anchor="w")

            # Info rows
            def info_row(label, value):
                row = tk.Frame(left_col, bg="white")
                row.pack(fill="x", pady=5)
                tk.Label(row, text=f"{label}:", font=("Helvetica", 12, "bold"),
                         bg="white", fg="#34495e", width=18, anchor="w").pack(side="left")
                tk.Label(row, text=value, font=("Helvetica", 12),
                         bg="white", fg="#2c3e50", anchor="w", wraplength=250, justify="left").pack(side="left")

            info_row("Email", user_email)
            info_row("Hourly Rate", f"${profile.get('hourly_rate', 'N/A')}")
            info_row("Availability", profile.get("availability", "N/A"))
            info_row("Completed Projects", profile.get("completed_projects", 0))
            info_row("Location", profile.get("location", "N/A"))
            info_row("Rating", f"{profile.get('rating', 'N/A')} ⭐")

            # Bio
            tk.Label(left_col, text="Bio", font=("Helvetica", 13, "bold"),
                     bg="white", fg="#34495e").pack(anchor="w", pady=(15, 5))
            tk.Message(left_col, text=profile.get("bio", "N/A"),
                       font=("Helvetica", 12), bg="white",
                       fg="#2c3e50", width=300).pack(anchor="w")

            # Skills
            tk.Label(left_col, text="Skills", font=("Helvetica", 13, "bold"),
                     bg="white", fg="#34495e").pack(anchor="w", pady=(15, 5))
            skills = profile.get("skills", [])
            if skills:
                skills_frame = tk.Frame(left_col, bg="white")
                skills_frame.pack(anchor="w", pady=5)
                for skill in skills:
                    tk.Label(
                        skills_frame, text=skill,
                        font=("Helvetica", 11),
                        bg="#ecf0f1", fg="#2c3e50",
                        padx=8, pady=4, relief="ridge", bd=1
                    ).pack(side="left", padx=4, pady=2)
            else:
                tk.Label(left_col, text="No skills listed",
                         font=("Helvetica", 11, "italic"), bg="white", fg="#7f8c8d").pack(anchor="w")

            # --- Right column content ---
            # Education
            tk.Label(right_col, text="Education", font=("Helvetica", 13, "bold"),
                     bg="white", fg="#34495e").pack(anchor="w", pady=(10, 5))
            education = profile.get("education") or []
            if isinstance(education, str):
                try:
                    education = json.loads(education)
                except Exception:
                    education = []
            if education:
                for edu in education:
                    tk.Label(
                        right_col,
                        text=f"🎓 {edu.get('degree')} at {edu.get('institution')} ({edu.get('year')})",
                        font=("Helvetica", 11), bg="white", fg="#2c3e50", wraplength=300, justify="left"
                    ).pack(anchor="w", pady=2)
            else:
                tk.Label(right_col, text="No education details", bg="white",
                         font=("Helvetica", 11, "italic")).pack(anchor="w")

            # Work history
            tk.Label(right_col, text="Work History", font=("Helvetica", 13, "bold"),
                     bg="white", fg="#34495e").pack(anchor="w", pady=(15, 5))
            work = profile.get("work_history") or []
            if isinstance(work, str):
                try:
                    work = json.loads(work)
                except Exception:
                    work = []
            if work:
                for job in work:
                    tk.Label(
                        right_col,
                        text=f"💼 {job.get('role')} at {job.get('company')} ({job.get('years')})",
                        font=("Helvetica", 11), bg="white", fg="#2c3e50", wraplength=300, justify="left"
                    ).pack(anchor="w", pady=2)
            else:
                tk.Label(right_col, text="No work history", bg="white",
                         font=("Helvetica", 11, "italic")).pack(anchor="w")

            # Edit button
            tk.Button(
                right_col, text="✏️ Edit Profile",
                command=lambda: open_edit_profile(profile),
                bg="#2980b9", fg="white",
                font=("Helvetica", 12, "bold"),
                relief="flat", padx=10, pady=6
            ).pack(pady=20, anchor="w")

            # --- Edit window ---
            def open_edit_profile(profile):
                edit_win = tk.Toplevel(content_frame)
                edit_win.title("Edit Profile")
                edit_win.geometry("500x700")
                edit_win.configure(bg="white")

                entries = {}
                form_fields = {
                    "Name": profile.get("name", ""),
                    "Specialization": profile.get("specialization", ""),
                    "Hourly Rate": profile.get("hourly_rate", ""),
                    "Availability": profile.get("availability", ""),
                    "Location": profile.get("location", ""),
                    "Bio": profile.get("bio", ""),
                }

                for field, value in form_fields.items():
                    tk.Label(edit_win, text=field, font=("Helvetica", 11, "bold"),
                             bg="white").pack(pady=(10, 0), anchor="w", padx=20)
                    entry = tk.Entry(edit_win, width=40)
                    entry.insert(0, str(value))
                    entry.pack(pady=2, padx=20)
                    entries[field] = entry

                # Skills multi-select
                tk.Label(edit_win, text="Skills", font=("Helvetica", 11, "bold"),
                         bg="white").pack(pady=(10, 0), anchor="w", padx=20)
                skills_list = ["Python", "JavaScript", "UI/UX", "API Integration", "SQL",
                               "Django", "Flask", "React", "DevOps", "Machine Learning"]
                skills_box = tk.Listbox(edit_win, selectmode="multiple", height=6, exportselection=0)
                skills_box.pack(padx=20, pady=5, fill="x")
                user_skills = set(profile.get("skills", []))
                for i, skill in enumerate(skills_list):
                    skills_box.insert("end", skill)
                    if skill in user_skills:
                        skills_box.selection_set(i)

                status_label = tk.Label(edit_win, text="", font=("Helvetica", 11), bg="white")
                status_label.pack(pady=(10, 0))

                def save_profile():
                    try:
                        selected_skills = [skills_box.get(i) for i in skills_box.curselection()]
                        updated_data = {
                            "name": entries["Name"].get(),
                            "specialization": entries["Specialization"].get(),
                            "hourly_rate": entries["Hourly Rate"].get(),
                            "availability": entries["Availability"].get(),
                            "location": entries["Location"].get(),
                            "bio": entries["Bio"].get(),
                            "skills": selected_skills,
                        }
                        supabase.table("profiles").update(updated_data).eq("id", user_id).execute()
                        logging.info("Profile updated successfully")
                        status_label.config(text="✅ Profile updated successfully!", fg="green")
                        profile_view(content_frame, user_email, user_id)
                    except Exception as e:
                        logging.exception("Error updating profile")
                        status_label.config(text=f"❌ Error: {e}", fg="red")

                tk.Button(edit_win, text="Save",
                          command=save_profile,
                          bg="#27ae60", fg="white",
                          font=("Helvetica", 12, "bold"),
                          relief="flat", padx=10, pady=5).pack(pady=20)

        except Exception as e:
            logging.exception("Error fetching profile")
            loading_label.config(text=f"❌ Error fetching profile: {e}", fg="red")

    content_frame.after(200, fetch_profile)
