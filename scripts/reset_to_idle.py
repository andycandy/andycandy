import json
import os
import random
import shutil
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LOG_FILE = os.path.join(BASE_DIR, "log.json")
CUR_GIF = os.path.join(BASE_DIR, "curState.gif")

IDLE_LIST = ["idle1.gif", "idle2.gif", "idle3.gif"]


def reset_to_idle():
    if not os.path.exists(LOG_FILE):
        print("No log file found. Skipping reset.")
        return

    with open(LOG_FILE, 'r') as f:
        entries = json.load(f)
    if not entries:
        print("Log is empty. Nothing to reset.")
        return

    last = entries[-1]
    last_time = datetime.fromisoformat(last['timestamp'].replace("Z", "")).replace(tzinfo=timezone.utc)
    timeout = last.get('timeout', 1800)
    now = datetime.now(timezone.utc)
    if (now - last_time).total_seconds() > timeout:
        idle_gif = random.choice(IDLE_LIST)
        shutil.copyfile(os.path.join(ASSETS_DIR, idle_gif), CUR_GIF)
        if last['action'] != "IDLE":
            idle_entry = {
                "user": "system",
                "action": "IDLE",
                "timestamp": now.isoformat() + "Z",
                "timeout": 1800
            }
            entries.append(idle_entry)
        with open(LOG_FILE, 'w') as f:
            json.dump(entries, f, indent=2)

if __name__ == '__main__':
    reset_to_idle()
