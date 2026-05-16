from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
import random
import time
import hashlib
import secrets
import hmac

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

def hash_passkey(passkey: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        passkey.encode(),
        salt.encode(),
        100000
    ).hex()

def verify_passkey(passkey: str, salt: str, stored_hash: str) -> bool:
    attempted_hash = hash_passkey(passkey, salt)
    return hmac.compare_digest(attempted_hash, stored_hash)

def public_profile(profile):
    return {
        "name": profile["name"],
        "skill": profile["skill"],
        "github_username": profile["github_username"],
    }

@app.get("/")
def home():
    return {
        "title": "Welcome to My First API",
        "status": "Running on Render",
        "instructions": "Go to /docs to sign the guestbook and join the directory!"
    }

@app.post("/join")
def join(profile: Profile):
    salt = secrets.token_hex(16)

    profiles.append({
        "name": profile.name,
        "skill": profile.skill,
        "github_username": profile.github_username,
        "passkey_hash": hash_passkey(profile.passkey, salt),
        "passkey_salt": salt,
    })

    return {"message": f"Welcome, {profile.name}! Keep your passkey safe."}

@app.get("/profiles")
def get_all():
    return [public_profile(p) for p in profiles]

@app.get("/stats")
def get_stats():
    return {"total_hackers": len(profiles), "timestamp": time.time()}

@app.get("/search/{name}")
def search_hacker(name: str):
    for p in profiles:
        if p["name"].lower() == name.lower():
            return public_profile(p)
    return {"error": "Hacker not found"}

@app.get("/random-hacker")
def get_random():
    if not profiles:
        return {"message": "The directory is empty!"}
    return public_profile(random.choice(profiles))

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
        "favorite_part": "Adding new components such as the search function and the vibe check!",
    }

@app.delete("/delete/{name}/{user_key}")
def delete_hacker(name: str, user_key: str):
    global profiles

    MASTER_KEY = "ImTheAdmin"

    for p in profiles:
        if p["name"].lower() == name.lower():
            valid_user_key = verify_passkey(
                user_key,
                p["passkey_salt"],
                p["passkey_hash"]
            )

            if valid_user_key or user_key == MASTER_KEY:
                profiles = [h for h in profiles if h["name"].lower() != name.lower()]
                return {"message": "Success"}

            raise HTTPException(status_code=403, detail="Invalid passkey")

    raise HTTPException(status_code=404, detail="User not found")
