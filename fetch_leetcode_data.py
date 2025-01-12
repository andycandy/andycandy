import requests
import json
import time

def fetch_calendar(username):
    """Fetch the user's submission calendar from LeetCode."""
    url = "https://leetcode.com/graphql"
    query = """
    {
      userCalendar(userSlug: "%s") {
        submissionCalendar
      }
    }
    """ % username

    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json={"query": query}, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if "errors" in data:
            print(f"Error in GraphQL response: {data['errors']}")
            return {}

        calendar = json.loads(data['data']['userCalendar']['submissionCalendar'])
        return calendar
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {}

def save_calendar(calendar, file_path="leetcode_calendar.json"):
    """Save the formatted calendar to a JSON file."""
    try:
        formatted = [
            {"date": time.strftime('%Y-%m-%d', time.gmtime(int(ts))),
             "count": int(count)} for ts, count in calendar.items()
        ]
        with open(file_path, "w") as file:
            json.dump(formatted, file, indent=2)
        print(f"Calendar saved to {file_path}")
    except Exception as e:
        print(f"Error saving calendar: {e}")

if __name__ == "__main__":
    username = "your-username"  # Replace with your LeetCode username
    calendar_data = fetch_calendar(username)
    if calendar_data:
        save_calendar(calendar_data)
    else:
        print("No calendar data fetched.")
