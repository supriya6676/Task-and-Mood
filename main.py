from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
app = FastAPI(title= "Task & Mood Tracker")


# 1. In-Memory Database
entries = [
    {"id": 0, "task": "Clean room", "status": "pending", "mood": "neutral", "date": "2026-08-28T09:00:00"},
    {"id": 1, "task": "Finish assignment", "status": "done", "mood": "happy", "date": "2026-08-29T15:30:00"},
    {"id": 2, "task": "Go for a walk", "status": "pending", "mood": "sad", "date": "2026-08-30T07:45:00"},
]
# Data validation
class Entry(BaseModel):
    task: str
    status: str  # "done" or "pending"
    mood: str    # "happy", "neutral", "sad"


# ==========================================
# 1. READ (GET) - View All 
# ==========================================
@app.get("/details")
def get_entries(task: str = None):
    if task:
        # filter entries where task matches
        return [e for e in entries if e["task"] == task]
    return entries

@app.get("/details/{id}")
def get_entry_by_id(id: int):
    for e in entries:
        if e["id"] == id:
            return e
    return {"error": "entry not found"}

@app.get("/stats/mood-by-status")
def mood_by_status():
    result = {}
    for e in entries:
        status = e["status"]
        mood = e["mood"]
        result.setdefault(status, {}).setdefault(mood, 0)
        result[status][mood] += 1
    return result
@app.get("/details/by-mood")
def get_entries_by_mood(mood: str):
    # your logic here
    if mood:
            # filter entries where task matches
            return [e for e in entries if e["mood"] == mood]
    return entries
# ==========================================
# 2. CREATE (POST) - Add New Student
# ==========================================
@app.post("/send_data")
def create_entry(entry:Entry):
    entry_dict = entry.model_dump()
    new_id= len(entries)
    entry_dict["id"] =new_id
    entry_dict["date"] = datetime.now().isoformat()
    entries.append(entry_dict)
    return entry_dict

# ==========================================
# 3. UPDATE (PUT) - Update Existing Student
# ==========================================


@app.put("/details/{id}")
def update_entry(id:int,updated_entry:Entry):
    for e in entries:
        if e["id"] == id:
            e.update(updated_entry.dict())
            return { "message": "Student updated successfully"} 
    return {"error": "entry not found"}

# ==========================================
# 4. DELETE (DELETE) - Remove Student
# ==========================================


@app.delete("/delete/{id}")
def delete_entry(id:int):
    for e in entries:
        if e["id"] == id:
            deleted = entries.remove(e)
            return {"message":"deleted successfully"}
    return {"error": "id not found"}