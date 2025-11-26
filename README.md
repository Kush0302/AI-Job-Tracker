# 📌 AI Job Tracker

An **AI-powered job tracking system** built with **Django**, **Django REST Framework**, and **React**.  
The project allows users to manage job applications and get AI-driven feedback on resumes.

---

##  Features

### ✅ Current Features
- **Job Tracking (Django)**
  - Add, view, and manage job applications
  - Store company, role, status, and notes
  - Django admin panel for management  

- **AI Resume Feedback (Django + React)**
  - Paste/upload resume text in React frontend
  - Sends request to Django REST API backend
  - AI model provides instant resume feedback

- **Architecture**
  - **Django:** Serves as the main backend, handling database models, authentication, and business logic.
  - **Django REST Framework (DRF):** Exposes API endpoints for the frontend to consume (Job CRUD, Auth, AI Feedback).
  - **React**: Provides the user interface for tracking jobs and viewing resume feedback.

---

## 🛠️ Tech Stack
- **Backend** → Django + Django REST Framework (Python) 
- **Frontend** → React (JavaScript/JSX)
- **Database** → PostgreSQL (Production) / SQLite (Development)
- **Deployment** → Render (Backend) + Vercel (Frontend) + Neon (Database)

---

## ⚙️ Installation & Setup

### 1. Clone the repo
```bash
git clone https://github.com/Kush0302/AI-Job-Tracker
cd AI-Job-Tracker 
```
### 2. Backend – Django
```bash
cd django_backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### 3. Frontend – React
```bash
cd react_frontend
npm install
npm run dev
```

# 🎯 Future Goals

- Automate Resume Parsing,

- Add Cloud Storage,

- Extend AI features:

  - Job description vs resume matching
  - Personalized career suggestions

# 📌 Project Status

✅ Core functionality complete: Job tracking + AI resume feedback

