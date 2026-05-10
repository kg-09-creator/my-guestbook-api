import os
# This finds the exact folder your code is sitting in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "hackers.json")
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
def create_profile(profile: Profile):
    data = load_data()
    # model_dump() is the modern way to turn your profile into data
    new_entry = profile.model_dump() 
    data.append(new_entry)
    save_data(data)
    return {"message": f"Successfully saved {profile.name}!"}
