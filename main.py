from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import random
import time

app = FastAPI(title="The Ultimate Hacker Directory")

# A simple list that stays in memory (no more 500 errors!)
profiles = []

class Profile(BaseModel):
    name: str
    skill: str
    github_username: str

@app.get("/")
def home():
    return {
        "title": "Welcome to My First API",
        "status": "Running on Render",
        "instructions": "Go to /docs to sign the guestbook and join the directory!"
    }

@app.post("/join")
def join(profile: Profile):
    """POST Endpoint: Join the club!"""
    profiles.append(profile.dict())
    return {"message": f"Welcome, {profile.name}!"}

@app.get("/profiles")
def get_all():
    return profiles

@app.get("/search/{name}")
def search_hacker(name: str):
    """GET Endpoint: Finds a specific hacker by name"""
    # 'p' is each individual profile in your list
    for p in profiles:
        if p["name"].lower() == name.lower():
            return p
    return {"error": "Hacker not found"}

@app.get("/random-hacker")
def get_random():
    """GET Endpoint 3: Picks a random person from the directory"""
    if not profiles:
        return {"message": "The directory is empty!"}
    return random.choice(profiles)

@app.get("/vibe")
def get_vibe():
    """GET Endpoint: Tells you the 'vibe' of the directory"""
    count = len(profiles)
    if count == 0:
        return {"vibe": "Ghost town... be the first to join!"}
    elif count < 5:
        return {"vibe": "Starting to buzz! A few hackers are here."}
    else:
        return {"vibe": "It's a party! The directory is full of talent."}

@app.get("/about")
def about_me():
    return {
        "developer": "Your Name Here", 
        "project_goal": "To earn my first Raspberry Pi", 
        "favorite_part": "Adding new components like vibe and the search function!", 
        "current_status": "Ready to submit!"
    }
