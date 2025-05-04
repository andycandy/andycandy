import random
import shutil
import os
import sys
import json
from datetime import datetime
from pathlib import Path

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../assets")

food = ["food1.gif", "food2.gif", "food3.gif"]
adventure = ["advent1.gif", "advent2.gif"]
treat = ["treat.gif"]
idle = ["idle1.gif", "idle2.gif", "idle3.gif"]

def copy_gif(filename: str, target: str = "curState.gif"):
    src = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(src):
        shutil.copyfile(src, target)
    else:
        print(f"File not found: {src}")

def log_action(user, action, file_path="log.json"):
    log_entry = {
        "user": user,
        "action": action,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "timeout": 1800 if action == "FEED_PET" else 7200
    }

    path = Path(file_path)
    if path.exists():
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No action provided.")
        sys.exit(1)

    action = sys.argv[1]
    log_action(sys.argv[2], action)

    if action == "FEED_PET":
        copy_gif(random.choice(food))
    elif action == "TAKE_ON_ADVENTURE":
        copy_gif(random.choice(adventure))
    elif action == "GIVE_TREAT":
        copy_gif(random.choice(treat))
    elif action == "IDLE":
        copy_gif(random.choice(idle))
    else:
        print(f"Invalid action: {action}")
