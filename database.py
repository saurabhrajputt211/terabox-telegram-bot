import json
import os
from datetime import datetime

DB_FILE = "users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user(user_id):
    users = load_users()
    user_id = str(user_id)
    if user_id not in users:
        users[user_id] = {
            "downloads_today": 0,
            "is_premium": False,
            "last_reset": datetime.now().strftime("%Y-%m-%d")
        }
        save_users(users)
    return users[user_id]

def update_user(user_id, key, value):
    users = load_users()
    user_id = str(user_id)
    users[user_id][key] = value
    save_users(users)

def reset_daily_limits():
    users = load_users()
    today = datetime.now().strftime("%Y-%m-%d")
    for user_id in users:
        if users[user_id]["last_reset"] != today:
            users[user_id]["downloads_today"] = 0
            users[user_id]["last_reset"] = today
    save_users(users)
