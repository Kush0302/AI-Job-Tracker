# 📌 AI Job Tracker

An **AI-powered job tracking system** built with **Django**, **FastAPI**, and **React**.  
The project allows users to manage job applications and get AI-driven feedback on resumes.

---

## 🚀 Features

### ✅ Current Features
- **Job Tracking (Django)**
  - Add, view, and manage job applications
  - Store company, role, status, and notes
  - Django admin panel for management  

- **AI Resume Feedback (FastAPI + React)**
  - Paste/upload resume text in React frontend
  - Sends request to FastAPI backend
  - AI model provides instant resume feedback

- **Separation of Concerns**
  - Django handles job applications
  - FastAPI handles AI services
  - React handles resume feedback display

---

## 🛠️ Tech Stack
- **Backend 1 (Django)** → Job application management  
- **Backend 2 (FastAPI)** → AI resume feedback service (using Z.AI Dolphin model)  
- **Frontend (React)** → User interface for resume feedback  

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
### 3. Backend – FastAPI
```bash
cd fastapi_backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```
### 4. Frontend – React
```bash
cd react_frontend
npm install
npm run dev
```

# 🎯 Future Goals

Convert the entire job tracker frontend into React:

Replace Django templates/admin with React UI consuming Django REST API (via Django REST Framework).

Add authentication for multiple users.

Extend AI features:

Job description vs resume matching

Personalized career suggestions

# 📌 Project Status

✅ Core functionality complete: Job tracking + AI resume feedback

