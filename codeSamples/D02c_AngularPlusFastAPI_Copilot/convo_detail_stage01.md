# Angular + FastAPI Application Development Log

## Initial Requirements
- Create an Angular app with a user form
- Input fields for name, address (2 lines + postcode), email and phone
- Left-aligned field titles
- Styling matching www.kplknowledge.co.uk
- Top menu bar with KPLKnowledge logo
- Submit button sending data to backend (POST to localhost:8080/users)
- Services page with clickable links (Training, Consultancy, Authoring, Mentoring, Coaching)
- FastAPI backend implementation
- Proper .gitignore setup

## Implementation Steps

### 1. Project Structure Setup
- Created frontend (Angular) and backend (FastAPI) directories
- Set up initial project files and configurations
- Implemented basic routing and component structure

### 2. Frontend Implementation
- Created components:
  - User form with left-aligned labels
  - Services page with clickable service links
  - Top menu bar with logo
- Added styling to match KPLKnowledge theme (navy blue/orange)
- Implemented form submission to backend

### 3. Backend Implementation
- Created FastAPI application with POST endpoint
- Added CORS configuration for frontend
- Implemented request validation using Pydantic

### 4. Project Configuration
- Added comprehensive .gitignore for both Python and Node.js
- Created README with setup instructions
- Set up development dependencies

## Technical Issues and Resolutions

### Angular Build Issue
Problem: Missing build dependencies
```
Error: Could not find the '@angular-devkit/build-angular:dev-server' builder's node package.
```
Solution: Added @angular-devkit/build-angular to devDependencies in package.json

## Project Structure
```
frontend/
  ├── src/
  │   ├── app/
  │   │   ├── user-form/
  │   │   ├── services/
  │   │   └── app.component.*
  │   └── assets/
  │       └── logo.svg
  └── package.json

backend/
  ├── main.py
  ├── requirements.txt
  └── venv/
```

## Running the Application

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

The application will be available at:
- Frontend: http://localhost:4200
- Backend API: http://localhost:8080/users

## Dependencies

### Frontend (Angular)
- @angular/core, common, forms, router: ^15.0.0
- @angular-devkit/build-angular: ^15.0.0
- Other standard Angular dependencies

### Backend (FastAPI)
- fastapi
- uvicorn[standard]
- pydantic
- python-multipart