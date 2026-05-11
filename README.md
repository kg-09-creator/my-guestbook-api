# my-guestbook-api
# My Digital Guestbook API
Hi, this is my project for Hack Club's RaspAPI! It's a simple guestbook where you can add a profile, view others' profiles, or search for a specific user. It works similar to Instagram and Discord in the sense that users create profiles that you and others can view.

## Live Link
(https://kgs-guestbook-api.onrender.com)

## How to Use
- Visit `/docs` to see all the commands.
- Use `/join` to add your profile!
- Use `GET /search{name}` to search for other users.
- Use `GET /random-hacker` to find someone new!
- Visit `/profiles` to see others' profiles.
  - If you see [], it just means the directory is empty. Use the /join endpoint to add yourself!
- Try the /vibe endpoint to see how the club is doing!

## Process
Built using Python and FastAPI, it is hosted on Render.

## Some Issues I Faced and Troubleshooted
- Error 500
- Status 127
