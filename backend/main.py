from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import requests
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = "https://etpqutdudxszedkkrjam.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV0cHF1dGR1ZHhzemVka2tyamFtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NDE2OTQsImV4cCI6MjA2ODIxNzY5NH0.Nu9_ZKlGVX1Sub9A4AHbgyzAL3Pctn8_ClrtjkLjnT8"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

class User(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str
    updated_at: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "User CRUD API"}

@app.get("/users", response_model=List[UserResponse])
def get_users():
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/users",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
            headers=headers
        )
        response.raise_for_status()
        users = response.json()
        if not users:
            raise HTTPException(status_code=404, detail="User not found")
        return users[0]
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users", response_model=UserResponse)
def create_user(user: User):
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/users",
            headers=headers,
            json=user.dict()
        )
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        elif isinstance(result, dict):
            return result
        else:
            raise HTTPException(status_code=500, detail="Unexpected response format")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    try:
        update_data = {k: v for k, v in user.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No data to update")
        
        response = requests.patch(
            f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
            headers=headers,
            json=update_data
        )
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list):
            if not result:
                raise HTTPException(status_code=404, detail="User not found")
            return result[0]
        elif isinstance(result, dict):
            return result
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        response = requests.delete(
            f"{SUPABASE_URL}/rest/v1/users?id=eq.{user_id}",
            headers=headers
        )
        response.raise_for_status()
        return {"message": "User deleted successfully"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)