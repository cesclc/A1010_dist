# KPL Knowledge - Angular + FastAPI Application

A full-stack web application with an Angular frontend and FastAPI backend for collecting user contact information and displaying services.

## Project Structure

```
D04_AngularPlusFastAPI/
├── frontend/          # Angular application
├── backend/           # FastAPI application
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Features

### Frontend (Angular)
- User contact form with validation
- Services page with clickable service cards
- Responsive design with professional styling
- Navigation menu with KPL Knowledge branding
- Form submission to backend API

### Backend (FastAPI)
- RESTful API endpoints
- User data validation with Pydantic
- CORS enabled for frontend communication
- Email validation
- In-memory data storage (demo purposes)

## Quick Start

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.8 or higher)
- npm or yarn

### Running the Application

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd D04_AngularPlusFastAPI
   ```

2. **Start the Backend (FastAPI)**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip3 install -r requirements.txt
   python3 main.py
   ```
   The API will be available at `http://localhost:8080`

3. **Start the Frontend (Angular)**
   ```bash
   cd frontend
   npm install
   ng serve
   ```
   The application will be available at `http://localhost:4200`

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /users` - Create a new user
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get a specific user

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Services

The application includes the following services:
- Training
- Consultancy
- Authoring
- Mentoring
- Coaching

## Technologies Used

### Frontend
- Angular 17+
- TypeScript
- CSS3 with CSS Variables
- Angular Reactive Forms
- Angular Router
- Angular HttpClient

### Backend
- FastAPI
- Python 3.8+
- Pydantic for data validation
- Uvicorn ASGI server
- CORS middleware

## Development

### Frontend Development
```bash
cd frontend
ng serve --open
```

### Backend Development
```bash
cd backend
python3 main.py
```

## Production Deployment

### Frontend
```bash
cd frontend
ng build --prod
```

### Backend
```bash
cd backend
pip3 install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
