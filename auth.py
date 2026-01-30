users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
}


def login(username, password):
    if username in users and users[username]["password"] == password:
        return users[username]["role"]
    return None
