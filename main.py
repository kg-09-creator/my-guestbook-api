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

@app.post("/join")
def join(profile: Profile):
    """POST Endpoint: Join the club!"""
    profiles.append(profile.dict())
    return {"message": f"Welcome, {profile.name}!"}
