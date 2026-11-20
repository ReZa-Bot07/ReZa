from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# دیتابیس موقت در حافظه
users_db = {"Javad": "123456"}
bot_status = {"is_running": False, "reply_text": "", "target_group": ""}

class LoginData(BaseModel):
    username: str
    password: str

class BotConfig(BaseModel):
    reply_text: str
    target_group: str
    speed: int
    count: int

@app.post("/api/app/login")
async def login(data: LoginData):
    if data.username in users_db and users_db[data.username] == data.password:
        return {"status": "success", "message": "خوش آمدید", "token": "test_token_123"}
    raise HTTPException(status_code=401, detail="نام کاربری یا رمز عبور اشتباه است")

@app.post("/api/app/start_reply")
async def start_reply(config: BotConfig):
    bot_status["is_running"] = True
    bot_status["reply_text"] = config.reply_text
    bot_status["target_group"] = config.target_group
    return {"status": "success", "message": "ربات با موفقیت روشن شد"}

@app.get("/api/app/status")
async def get_status():
    return bot_status

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
