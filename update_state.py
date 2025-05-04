import json
from datetime import datetime, timezone
import os

LOG_FILE = "log.json"
README_FILE = "README.md"
START_TAG = "<!-- ACTION_LOG_START -->"
END_TAG = "<!-- ACTION_LOG_END -->"

ACTION_EMOJI_MAP = {
    "FEED_PET": "🍎",
    "TAKE_ON_ADVENTURE": "🗺️",
    "GIVE_TREAT": "🍦",
    "IDLE": "🛋️",
    # Add emojis for other potential actions if you add them
}

def load_log():
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def time_ago(iso_timestamp):
    past = datetime.fromisoformat(iso_timestamp.replace("Z", "")).replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = now - past
    seconds = int(diff.total_seconds())
    if seconds < 60:
        return f"{seconds} seconds ago"
    elif seconds < 3600:
        return f"{seconds // 60} minutes ago"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 2592000:
        days = seconds // 86400
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return past.strftime('%Y-%m-%d')

def describe_action(entry):
    action = entry["action"]
    user = entry["user"]
    emoji = ACTION_EMOJI_MAP.get(action, "✨")
    if action == "FEED_PET":
        description = f"fed me {emoji}"
    elif action == "TAKE_ON_ADVENTURE":
        description = f"took me on an adventure {emoji}"
    elif action == "GIVE_TREAT":
        description = f"gave me a treat {emoji}"
    elif action == "IDLE":
        return None  # Skip from log display
    else:
        description = f"did something strange... 🤔"

    return f"<b>{user}</b> {description}"


def format_entries(log):
    lines = []
    count = 0
    for entry in reversed(log):
        desc = describe_action(entry)
        if desc is None:
            continue  # skip IDLE actions
        ago = time_ago(entry["timestamp"])
        lines.append(f"<div>{desc} — {ago}</div>")
        count += 1
        if count == 5:
            break
    return "\n".join(lines)


def update_readme(formatted_html):
    collapsible = f"<details>\n<summary> Recent Pet Interactions </summary>\n\n{formatted_html}\n\n</details>"

    with open(README_FILE, "r") as f:
        content = f.read()

    if START_TAG in content and END_TAG in content:
        start = content.index(START_TAG) + len(START_TAG)
        end = content.index(END_TAG)
        updated = content[:start] + "\n\n" + collapsible + "\n\n" + content[end:]
    else:
        updated = content + f"\n\n{START_TAG}\n\n{collapsible}\n\n{END_TAG}"

    with open(README_FILE, "w") as f:
        f.write(updated)

if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        raise FileNotFoundError(f"{LOG_FILE} not found.")
    log = load_log()
    html_log = format_entries(log)
    update_readme(html_log)
