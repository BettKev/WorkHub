# WorkHub

WorkHub is a freelancer platform desktop application built with Python, Tkinter, and Supabase. It provides a modern interface for freelancers to manage projects, profiles, and settings, with persistent data storage via Supabase.

---

## 📁 Project Structure

```
.
├── .env                  # Environment variables (Supabase credentials)
├── .gitignore            # Git ignore file
├── app.py                # Main application entry point
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── start.sh              # Shell script to launch the app
├── views/                # UI views for dashboard, profile, projects, settings
│   ├── dashboard.py
│   ├── profile.py
│   ├── projects.py
│   ├── settings.py
│   └── __pycache__/
├── windows/              # Tkinter windows for login, signup, dashboard
│   ├── __init__.py
│   ├── dashboard.py
│   ├── login.py
│   ├── signup.py
│   └── __pycache__/
```

- **app.py**: Initializes the Tkinter root window, loads environment variables, and launches the login/signup windows.
- **views/**: Contains the main content views for dashboard, projects, profile, and settings.
- **windows/**: Contains window logic for login, signup, and dashboard navigation.
- **requirements.txt**: Lists all required Python packages.
- **start.sh**: Bash script to activate the virtual environment and start the app.
- **.env**: Stores Supabase URL and API key (not committed to version control).

---

## 🚀 Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/BettKev/WorkHub
cd workhub
```

### 2. Set Up Python Environment

It is recommended to use a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with your Supabase credentials:

```
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-supabase-api-key"
```

> **Note:** Never share your Supabase key publicly.

### 5. Run the Application

You can start the app using the provided shell script:

```sh
bash start.sh
```

Or run directly with Python:

```sh
python3 app.py
```

---

## 🖥️ Features

- **User Authentication:** Sign up and log in with Supabase Auth.
- **Dashboard:** Overview of projects, tasks, earnings, and recent activity.
- **Projects:** View all projects from Supabase.
- **Profile:** View and edit freelancer profile, including skills and bio.
- **Settings:** (Coming soon)

- Note: Use the following test credentials to test the application (email: testuser1@gmail.com, password: 123456). The backend is deployed in supabase and after sometime the project is paused which may cause the application to delay for up to 50 seconds when you first try to call the backend resources.

---

## 🛠️ Tech Stack

- **Python 3**
- **Tkinter** (GUI)
- **Supabase** (Backend: Auth & Database)
- **dotenv** (Environment management)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

---
