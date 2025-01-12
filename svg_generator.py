import json
from datetime import datetime
from svgwrite import Drawing

def generate_calendar_svg(data_file="leetcode_calendar.json", output_file="leetcode_calendar.svg"):
    with open(data_file, "r") as f:
        data = json.load(f)

    width = 800
    height = 120
    box_size = 12
    box_spacing = 2
    colors = {
        0: "#ebedf0", 
        1: "#fce2b3", 
        2: "#fcc78d", 
        3: "#FFA116",
    }

    dwg = Drawing(output_file, size=(f"{width}px", f"{height}px"))
    start_x, start_y = 20, 20

    max_count = max(entry["count"] for entry in data) if data else 1

    for i, entry in enumerate(data):
        date = datetime.strptime(entry["date"], "%Y-%m-%d")
        count = entry["count"]

        intensity = min((count * 3) // max_count, 3)
        color = colors[intensity]

        week = (date - datetime(date.year, 1, 1)).days // 7
        day = date.weekday()

        x = start_x + (week * (box_size + box_spacing))
        y = start_y + (day * (box_size + box_spacing))

        dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), fill=color))
      
    dwg.save()
    print(f"SVG generated: {output_file}")

if __name__ == "__main__":
    generate_calendar_svg()
