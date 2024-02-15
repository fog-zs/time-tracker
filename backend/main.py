from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from typing import List

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORSを許可するオリジンのリスト
origins = [
    "http://192.168.0.10:8080/",  
    "http://localhost:8080",  
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],  # すべてのオリジンを許可    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ActionRecord(BaseModel):
    action: str
    time: str

def read_json_file(file_path: str) -> List:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_json_file(file_path: str, data) -> None:
    with open(file_path, "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

@app.post("/api/save/")
async def save_action(record: ActionRecord):
    file_path = "actions.json"
    actions = read_json_file(file_path)
    actions.append(record.dict())
    write_json_file(file_path, actions)
    return {"message": "データを保存しました"}

@app.get("/api/actions/", response_model=List[ActionRecord])
async def get_actions():
    actions = read_json_file("actions.json")
    return actions[-10:]  # 最新の10件を返す


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)