from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow CORS for Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    name: str
    address1: str
    address2: str
    postcode: str
    email: str
    phone: str

@app.post("/users")
async def create_user(user: User):
    # In a real app, save to database here
    print(f"Received user data: {user}")
    return {"status": "success"}