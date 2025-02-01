import requests
import json
import time

def fetch_calendar(username):
  url = "https://leetcode.com/graphql"
  query = """
  query userProfileCalendar($username: String!, $year: Int) {
    matchedUser(username: $username) {
    userCalendar(year: $year) {
      activeYears
      streak
      totalActiveDays
      dccBadges {
      timestamp
      badge {
        name
        icon
      }
      }
      submissionCalendar
    }
    }
  }
  """

  variables = {
    "username": username
  }

  payload = {
    "query": query,
    "variables": variables,
    "operationName": "userProfileCalendar"
  }

  headers = {"Content-Type": "application/json"}
  try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    if "errors" in data:
      print(f"Error in GraphQL response: {data['errors']}")
      return {}

    calendar = json.loads(data['data']['matchedUser']['userCalendar']['submissionCalendar'])
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
    username = "kasyapanand7"
    calendar_data = fetch_calendar(username)
    if calendar_data:
        save_calendar(calendar_data)
    else:
        print("No calendar data fetched.")
