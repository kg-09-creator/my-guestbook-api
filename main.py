from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import random
import time

app = FastAPI(title="The Ultimate Hacker Directory")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Profile(BaseModel):
    name: str
    skill: str
    github_username: str
    passkey: str  

profiles = []

@app.get("/")
def home():
    return {
        "title": "Welcome to My First API",
        "status": "Running on Render",
        "instructions": "Go to /docs to sign the guestbook and join the directory!"
    }

@app.post("/join")
def join(profile: Profile):
    profiles.append(profile.dict())
    return {"message": f"Welcome, {profile.name}! Keep your passkey safe."}

@app.get("/profiles")
def get_all():
    return profiles

@app.get("/stats")
def get_stats():
    return {"total_hackers": len(profiles), "timestamp": time.time()}

@app.get("/search/{name}")
def search_hacker(name: str):
    for p in profiles:
        if p["name"].lower() == name.lower():
            return p
    return {"error": "Hacker not found"}

@app.get("/random-hacker")
def get_random():
    if not profiles:
        return {"message": "The directory is empty!"}
    return random.choice(profiles)

@app.get("/vibe")
def get_vibe():
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
        "developer": "Kavya",
        "project_goal": "To earn my first Raspberry Pi",
        "favorite_part": "Adding new components like vibe and the search function!",
    }

@app.delete("/delete/{name}/{passkey}")
def delete_hacker(name: str, passkey: str):
    global profiles
    for p in profiles:
        if p["name"].lower() == name.lower():
            if p["passkey"] == passkey:
                profiles = [h for h in profiles if h["name"].lower() != name.lower()]
                return {"message": f"Profile for {name} deleted successfully."}
            else:
                return {"error": "Invalid passkey for this user."}, 403
    
    return {"error": "User not found."}, 404
