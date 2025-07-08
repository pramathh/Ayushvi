import json

# 🔁 Replace this path with your actual path
path = "D:/New folder (2)/ayushvi-whatsapp-firebase-adminsdk-fbsvc-0cb3ffdf85.json"

with open(path, "r") as f:
    data = json.load(f)

# Convert to one-liner with escaped newlines
env_ready = json.dumps(data)
print(env_ready)
