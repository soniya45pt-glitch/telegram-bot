import time

users = {}

def add_user(user_id):
    users[user_id] = {"paid": False}

def set_paid(user_id):
    users[user_id]["paid"] = True

def is_paid(user_id):
    return users.get(user_id, {}).get("paid", False)
