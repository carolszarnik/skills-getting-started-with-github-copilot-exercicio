"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Practice tennis techniques, strategy, and competitive play",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Swimming Team": {
        "description": "Build swimming skills, endurance, and teamwork in the pool",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": []
    },
    "Soccer Team": {
        "description": "Practice teamwork and compete in soccer matches",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Basketball Team": {
        "description": "Develop shooting, passing, and defensive skills on the court",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Explore acting, stage performance, and theatrical storytelling",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Art Workshop": {
        "description": "Create paintings, sketches, and mixed media projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": []
    },
    "Creative Writing Club": {
        "description": "Develop storytelling skills through poetry, fiction, and creative writing",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    },
    "Music Ensemble": {
        "description": "Learn ensemble performance, musical expression, and collaboration",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants":  twenty,
        "participants": []
    },
    "Science Olympiad": {
        "description": "Solve STEM challenges and prepare for science competitions",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": []
    },
    "Book Club": {
        "description": "Read, discuss, and analyze literature from diverse perspectives",
        "schedule": "Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Computer Science Club": {
        "description": "Explore algorithms, coding projects, and computer science concepts",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Debate Club": {
        "description": "Practice argumentation, public speaking, and critical thinking",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 12,
        "participants": []
    },
    "Track and Field": {
        "description": "Train for sprinting, jumping, and distance events in a competitive environment",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": []
    },
    "Volleyball Team": {
        "description": "Develop serving, passing, and teamwork skills through practice and matches",
        "schedule": "Thursdays, 3:30 PM - 5:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Ceramics Club": {
        "description": "Explore clay sculpting, pottery techniques, and creative design",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": []
    },
    "Photography Club": {
        "description": "Learn camera techniques, composition, and digital editing skills",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Mathletes": {
        "description": "Solve challenging math problems and compete in academic contests",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Robotics Club": {
        "description": "Design, build, and program robots for STEM challenges and competitions",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
