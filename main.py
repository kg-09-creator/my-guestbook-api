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
    return {"message": "API is Live! Visit /docs to join the club."}

@app.get("/profiles")
def get_all():
    return profiles

@app.get("/random-hacker")
def get_random():
    """GET Endpoint 3: Picks a random person from the directory"""
    if not profiles:
        return {"message": "The directory is empty!"}
    return random.choice(profiles)

@app.get("/vibe")
def get_vibe():
    """GET Endpoint 4: Checks the vibe of the directory"""
    count = len(profiles)
    if count == 0:
        return {"vibe": "Quiet... maybe too quiet. Add someone!"}
    elif count < 5:
        # This will be your vibe since you have 3 profiles now!
        return {"vibe": "Starting to buzz! The club is growing."}
    else:
        return {"vibe": "It's a party in here! We've got a full house."}

@app.get("/about")
def about_me():
    return {
        "developer": "Your Name/Username",
        "project": "RaspAPI Member Directory",
        "fun_fact": "I built this entire API in one sitting!"
    }

@app.post("/join")
def join(profile: Profile):
    """POST Endpoint: Join the club!"""
    profiles.append(profile.dict())
    return {"message": f"Welcome, {profile.name}!"}
