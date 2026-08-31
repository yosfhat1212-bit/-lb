from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

BALANCE_FILE = "balances.json"
TOKEN = "8680499622:AAHTpgQXyGKyFATDolT6tmBH4USgct1HU4A" # تۆکنا بۆتێ تە

def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f)

class BalanceRequest(BaseModel):
    user_id: str
    amount: int

@app.post("/api/add_balance")
async def add_balance(req: BalanceRequest):
    balances = load_data(BALANCE_FILE)
    current_bal = balances.get(req.user_id, 5)
    balances[req.user_id] = current_bal + req.amount
    save_data(BALANCE_FILE, balances)
    return {"status": "success", "new_balance": balances[req.user_id]}
