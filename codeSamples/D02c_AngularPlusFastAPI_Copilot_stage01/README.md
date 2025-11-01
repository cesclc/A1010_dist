# KPLKnowledge Sample App

A simple user form app with Angular frontend and FastAPI backend.

Written by Copilot.
Use as an exercise in fixing AI-produced code.

## Setup

### Frontend (Angular)

```bash
cd frontend
npm install
npm start
```

The frontend will be available at http://localhost:4200

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

The backend API will be available at http://localhost:8080

## Features

- User form with name, address, email and phone
- Services page with clickable service options
- Responsive layout that works well on all screen sizes
- Styling matches KPLKnowledge website theme
- Backend API to handle form submissions