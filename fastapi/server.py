from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Shot(BaseModel):
    number: int
    name: str
    sequence: str
    department: Optional[str] = None

shots = {
    1001: {"number": 1001,
        "name": "shot01",
        "sequence": "some seq",
        "department": "FX"},
    1002: {"number": 1002,
        "name": "shot02",
        "sequence": "some other seq",
        "department": "Animation"},
}

@app.get("/")
def index():
    return shots

@app.get("/get-shot/{shot_num}")
def get_shot_by_number(shot_num: int = Path(description="Input the shot number for the shot in the sequence")):
    return shots[shot_num]

@app.get("/get-shot-by-name/{shot_name}")
def get_shot_by_name(shot_name):
    for shot in shots:
        if shots[shot]["name"] == shot_name:
            return shots[shot]

@app.post("/create-shot/{shot_num}")
def create_shot(shot_num: int, shot: Shot):
    if shot_num in shots:
        return {"Error": "Shot already exists"}
    shots[shot_num] = shot
    return shots[shot_num]

@app.put("/update-shot/{shot_num}")
def update_shot(shot_num: int, shot: Shot):
    if shot_num not in shots:
        return {"Error": "That shot doesn't exists"}
    
    shots[shot_num] =  {"number": shot_num,
        "name": shot.name,
        "sequence": shot.sequence,
        "department": shot.department}

    return shots[shot_num]

@app.delete("/delete-shot/{shot_num}")
def delete_shot(shot_num: int):
    if shot_num not in shots:
        return {"Error": "Shot not found"}

    del shots[shot_num]
    return {"Message" : "Shot deleted"}
