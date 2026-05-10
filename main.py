from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import time

app = FastAPI(title="Hack Club Member Directory", description="An API to share hacker profiles!")

# This is a "Schema" - it defines what a Profile should look like
class Profile(BaseModel):
    name: str
    skill: str
    github_username: str
    joined_at: float = time.time()

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

@app.post("/join")
def create_profile(profile: Profile):
    """Add your own profile to the directory!"""
    profiles.append(profile)
    return {"message": f"Welcome to the club, {profile.name}!"}
