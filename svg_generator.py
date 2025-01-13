import json
from datetime import datetime, timedelta
from svgwrite import Drawing

def generate_calendar_svg(data_file="leetcode_calendar.json", output_file="leetcode_calendar.svg"):
    with open(data_file, "r") as f:
        data = json.load(f)

    activity = {}
    for entry in data:
        date = datetime.strptime(entry["date"], "%Y-%m-%d")
        activity[date] = entry["count"]

    height = 150
    box_size = 12
    box_spacing = 2
    colors = {
        0: "#353839",
        1: "#fdecc8",
        2: "#fbc98a",
        3: "#FFA116",
    }

    days_in_year = 366 if datetime.now().year % 4 == 0 else 365
    width = (days_in_year // 7 + 18) * (box_size + box_spacing)

    dwg = Drawing(output_file, size=(f"{width}px", f"{height}px"))
    start_x, start_y = 20, 20
    x_offset, y_offset = start_x, start_y
    start_date = datetime(datetime.now().year - 1, datetime.now().month, datetime.now().day)
    current_date = start_date
    end_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    
    if current_date.weekday() != 6:
        y_offset = start_y + (current_date.weekday() + 1) * (box_size + box_spacing)

    while current_date < end_date:
        if current_date.day == 1:
            x_offset += (box_size + box_spacing)
        if(current_date.weekday() == 6):
            y_offset = start_y
            x_offset += (box_size + box_spacing)
        count = activity.get(current_date, 0)
        if count == 0:
            color = colors[0]
        elif count <= 5:
            color = colors[1]
        elif count <= 15:
            color = colors[2]
        else:
            color = colors[3]

        x, y= x_offset, y_offset
        dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), fill=color, rx=2, ry=2))
        y_offset += (box_size + box_spacing)
        current_date += timedelta(days=1)

    dwg.save()
    print(f"SVG generated: {output_file}")

if __name__ == "__main__":
    generate_calendar_svg()
