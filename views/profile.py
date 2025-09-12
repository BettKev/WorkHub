# views/profile.py
import tkinter as tk
import logging
from db import supabase  # ✅ use global client

def profile_view(content_frame, user_email, user_id):
    # Clear content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Page header
    header = tk.Frame(content_frame, bg="#2980b9", height=80)
    header.pack(fill="x")
    tk.Label(
        header, text="👤 Profile",
        font=("Helvetica", 18, "bold"),
        fg="white", bg="#2980b9"
    ).pack(pady=20, padx=20, anchor="w")

    # Loading message
    loading_label = tk.Label(
        content_frame,
        text="⏳ Loading profile...",
        font=("Helvetica", 12, "italic"),
        bg="#ecf0f1",
        fg="#7f8c8d"
    )
    loading_label.pack(pady=40)

    def fetch_profile():
        try:
            logging.info(f"Fetching profile for {user_email}...")

            response = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
            profile = response.data if response.data else None

            # Clear loading state
            loading_label.destroy()

            if not profile:
                tk.Label(
                    content_frame,
                    text="No profile found. Please complete your profile.",
                    font=("Helvetica", 12),
                    bg="#ecf0f1"
                ).pack(pady=20)
                return

            # === Profile Card ===
            card = tk.Frame(content_frame, bg="white", bd=2, relief="groove")
            card.pack(padx=30, pady=30, fill="x")

            # Avatar + name
            top_section = tk.Frame(card, bg="white")
            top_section.pack(fill="x", pady=10)
            tk.Label(top_section, text="👤", font=("Helvetica", 40), bg="white").pack(side="left", padx=15)
            tk.Label(
                top_section,
                text=profile.get("name", "Freelancer"),
                font=("Helvetica", 16, "bold"),
                bg="white", fg="#2c3e50"
            ).pack(anchor="w", padx=10)

            # Information section
            info_frame = tk.Frame(card, bg="white")
            info_frame.pack(fill="x", pady=10, padx=15)

            fields = {
                "Email": user_email,
                "Specialization": profile.get("specialization", "N/A"),
                "Hourly Rate": f"${profile.get('hourly_rate', 'N/A')}",
                "Location": profile.get("location", "N/A"),
                "Bio": profile.get("bio", "N/A"),
                "Rating": f"{profile.get('rating', 'N/A')} ⭐",
            }

            for key, value in fields.items():
                row = tk.Frame(info_frame, bg="white")
                row.pack(fill="x", pady=3)
                tk.Label(row, text=f"{key}:", font=("Helvetica", 12, "bold"), bg="white", width=15, anchor="w").pack(side="left")
                tk.Label(row, text=value, font=("Helvetica", 12), bg="white", anchor="w", wraplength=400, justify="left").pack(side="left", fill="x")

            # Skills section
            skills = profile.get("skills", [])
            skills_str = ", ".join(skills) if skills else "No skills listed"

            tk.Label(
                card, text="Skills", font=("Helvetica", 12, "bold"),
                bg="white", fg="#34495e"
            ).pack(anchor="w", padx=15, pady=(15, 5))
            tk.Label(
                card, text=skills_str, font=("Helvetica", 12),
                bg="white", wraplength=500, justify="left"
            ).pack(anchor="w", padx=15)

            # --- Edit Profile Button ---
            def open_edit_profile():
                edit_win = tk.Toplevel(content_frame)
                edit_win.title("Edit Profile")
                edit_win.geometry("450x600")
                edit_win.configure(bg="white")

                entries = {}
                form_fields = {
                    "Name": profile.get("name", ""),
                    "Specialization": profile.get("specialization", ""),
                    "Hourly Rate": profile.get("hourly_rate", ""),
                    "Location": profile.get("location", ""),
                    "Bio": profile.get("bio", ""),
                }

                for field, value in form_fields.items():
                    tk.Label(edit_win, text=field, font=("Helvetica", 11), bg="white").pack(pady=(10, 0), anchor="w", padx=20)
                    entry = tk.Entry(edit_win, width=40)
                    entry.insert(0, str(value) if value is not None else "")
                    entry.pack(pady=2, padx=20)
                    entries[field] = entry

                # Skills with multi-select listbox
                tk.Label(edit_win, text="Skills", font=("Helvetica", 11), bg="white").pack(pady=(10, 0), anchor="w", padx=20)
                skills_list = ["Python", "JavaScript", "UI/UX", "API Integration", "SQL", "Django", "Flask", "React", "DevOps", "Machine Learning"]
                skills_box = tk.Listbox(edit_win, selectmode="multiple", height=6, exportselection=0)
                skills_box.pack(padx=20, pady=5, fill="x")

                user_skills = set(profile.get("skills", []))
                for i, skill in enumerate(skills_list):
                    skills_box.insert("end", skill)
                    if skill in user_skills:
                        skills_box.selection_set(i)

                # Status label for save
                status_label = tk.Label(edit_win, text="", font=("Helvetica", 11), bg="white")
                status_label.pack(pady=(10, 0))

                def save_profile():
                    try:
                        selected_skills = [skills_box.get(i) for i in skills_box.curselection()]
                        updated_data = {
                            "name": entries["Name"].get(),
                            "specialization": entries["Specialization"].get(),
                            "hourly_rate": entries["Hourly Rate"].get(),
                            "location": entries["Location"].get(),
                            "bio": entries["Bio"].get(),
                            "skills": selected_skills,
                        }
                        supabase.table("profiles").update(updated_data).eq("id", user_id).execute()
                        logging.info("Profile updated successfully")
                        status_label.config(text="✅ Profile updated successfully!", fg="green")
                        profile_view(content_frame, user_email, user_id)  # ✅ removed supabase arg
                    except Exception as e:
                        logging.exception("Error updating profile")
                        status_label.config(text=f"❌ Error: {e}", fg="red")

                tk.Button(edit_win, text="Save", command=save_profile, bg="#27ae60", fg="white", font=("Helvetica", 12)).pack(pady=20)

            tk.Button(card, text="✏️ Edit Profile", command=open_edit_profile, bg="#2980b9", fg="white", font=("Helvetica", 12, "bold")).pack(pady=15)

        except Exception as e:
            logging.exception("Error fetching profile")
            loading_label.config(
                text=f"❌ Error fetching profile: {e}",
                fg="red"
            )

    # Fetch after short delay so "Loading profile..." shows
    content_frame.after(200, fetch_profile)
