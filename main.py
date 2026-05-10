import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional  # Add Optional here
import time

app = FastAPI(title="Hack Club Member Directory", description="An API to share hacker profiles!")

# This is a "Schema" - it defines what a Profile should look like
class Profile(BaseModel):
    name: str = "New Hacker"
    skill: str = "Learning"
    github_username: str = "pending"
    joined_at: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Orpheus",
                "skill": "Dinosaurs",
                "github_username": "orpheus-codes"
            }
        }


# Our "Database" (for now)
profiles = []

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Welcome to the Hacker Directory!"}

@app.get("/profiles", response_model=List[Profile])
def get_all_profiles():
    """Returns a list of every hacker who has joined."""
    return profiles

@app.get("/stats")
def get_stats():
    """Shows how many hackers are in our directory."""
    return {"total_hackers": len(profiles), "server_time": time.time()}

@app.get("/search/{name}")
def search_hacker(name: str):
    data = load_data()  # Make sure we are looking at the saved file!
    for p in data:
        # We check both ways just in case
        hacker_name = p.get("name", "") if isinstance(p, dict) else getattr(p, "name", "")
        if hacker_name.lower() == name.lower():
            return p
    return {"error": "Hacker not found"}

@app.post("/join")
def join(profile: Profile):
    current_data = load_data()
    # Use .dict() or .model_dump() to turn the object into a simple dictionary
    new_entry = profile.dict() 
    current_data.append(new_entry)
    save_data(current_data)
    return {"message": f"Saved {profile.name} to the database!"}



