from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# ڤەکری بۆ هندێ ماڵپەڕ شیێت داخوازێ بینێرێت
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOT_TOKEN = "8680499622:AAHTpgQXyGKyFATDolT6tmBH4USgct1HU4A"

class BalanceRequest(BaseModel):
    user_id: str
    amount: int

@app.post("/api/add_balance")
async def add_balance(data: BalanceRequest):
    try:
        msg = f"🎉 پیرۆزە! {data.amount} کلیل ژ لایێ ڕێڤەبەری ڤە هاتنە زێدەکرن بۆ پڕۆفایلا تە."
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        response = requests.post(url, json={
            "chat_id": data.user_id,
            "text": msg
        })
        
        res_data = response.json()
        if res_data.get("ok"):
            return {"status": "success", "new_balance": data.amount}
        else:
            raise HTTPException(status_code=400, detail="Telegram failed to send message.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
