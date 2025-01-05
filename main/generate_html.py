import os
import csv
import json
from jinja2 import Environment, FileSystemLoader

# Path to your templates folder
template_path = "."
env = Environment(loader=FileSystemLoader(template_path))

# Function to generate individual game HTML files
def generate_game_pages(csv_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    game_template = env.get_template("template.html")
    games = []

    for file in os.listdir(csv_folder):
        if file.endswith(".csv"):
            universe_id = file.replace(".csv", "")
            csv_path = os.path.join(csv_folder, file)

            # Read CSV data
            with open(csv_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)

            # Extract game details - game name from the last row
            if data:
                game_name = data[-1]["name"]
                games.append({"universe_id": universe_id, "name": game_name})

                # Extract data for Highcharts
                timestamps = [row["timestamp"] for row in data] if data else []
                playing = [int(row["playing"]) for row in data] if data else []
                visits = [int(row["visits"]) for row in data] if data else []
                favoritedCount = [int(row["favoritedCount"]) for row in data] if data else []
                upVotes = [int(row["upVotes"]) for row in data] if data else []
                downVotes = [int(row["downVotes"]) for row in data] if data else []

                # Calculate change fields
                visitschange = [int(data[i]["visits"]) - int(data[i-1]["visits"]) if i > 0 else 0 for i in range(len(data))]
                favoritedchange = [int(data[i]["favoritedCount"]) - int(data[i-1]["favoritedCount"]) if i > 0 else 0 for i in range(len(data))]
                upVoteschange = [int(data[i]["upVotes"]) - int(data[i-1]["upVotes"]) if i > 0 else 0 for i in range(len(data))]
                downVoteschange = [int(data[i]["downVotes"]) - int(data[i-1]["downVotes"]) if i > 0 else 0 for i in range(len(data))]
                upVotespercentage = [(int(data[i]["upVotes"]) / (int(data[i]["upVotes"]) + int(data[i]["downVotes"]))) * 100 if int(data[i]["upVotes"]) + int(data[i]["downVotes"]) > 0 else 0 for i in range(len(data))]

                # Render game page
                output_html = game_template.render(
                    game_name=game_name,
                    timestamps=json.dumps(timestamps),
                    playing=json.dumps(playing),
                    visits=json.dumps(visits),
                    visitschange=json.dumps(visitschange),
                    favoritedCount=json.dumps(favoritedCount),
                    favoritedchange=json.dumps(favoritedchange),
                    upVotes=json.dumps(upVotes),
                    downVotes=json.dumps(downVotes),
                    upVoteschange=json.dumps(upVoteschange),
                    downVoteschange=json.dumps(downVoteschange),
                    upVotespercentage=json.dumps(upVotespercentage),
                )

                # Save game page
                output_file = os.path.join(output_folder, f"{universe_id}.html")
                with open(output_file, mode="w", encoding="utf-8") as htmlfile:
                    htmlfile.write(output_html)

    return games

# Function to generate the home page
def generate_home_page(output_folder, games):
    home_template = env.get_template("home_template.html")

    # Render home page
    output_html = home_template.render(games=games)

    # Save home page
    output_file = os.path.join(output_folder, "index.html")
    with open(output_file, mode="w", encoding="utf-8") as htmlfile:
        htmlfile.write(output_html)

# Paths
csv_folder = "./game_data"  # Folder where your CSV files are stored
output_folder = "./html_pages"  # Folder to store the generated HTML files

# Generate pages
games = generate_game_pages(csv_folder, output_folder)
generate_home_page(output_folder, games)

print(f"HTML pages and home page generated in: {output_folder}")

