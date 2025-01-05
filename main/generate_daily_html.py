import os
import csv
import json
from jinja2 import Environment, FileSystemLoader

# Path to your templates folder
template_path = "."
env = Environment(loader=FileSystemLoader(template_path))

# Function to generate individual game HTML files (normal)
def generate_game_pages(csv_folder, output_folder, mode="normal"):
    os.makedirs(output_folder, exist_ok=True)
    game_template = env.get_template("template.html")
    games = []

    # Determine the correct folder based on the mode
    data_folder = f"{csv_folder}_{mode}" if mode == "daily" else csv_folder

    # Preload both datasets for normal and daily
    normal_data = {}
    daily_data = {}

    # Read data for both normal and daily modes
    for file in os.listdir(csv_folder):
        if file.endswith(".csv"):
            universe_id = file.replace(".csv", "")
            normal_csv_path = os.path.join(csv_folder, file)
            daily_csv_path = os.path.join(f"{csv_folder}_daily", file)

            # Read the CSV files
            with open(normal_csv_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                normal_data[universe_id] = list(reader)

            with open(daily_csv_path, mode="r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                daily_data[universe_id] = list(reader)

            # Extract game details and other necessary data
            game_name = normal_data[universe_id][-1]["name"]  # Game name from the last row
            games.append({"universe_id": universe_id, "name": game_name, "mode": mode})

    # Now we will pass both datasets to the HTML template for the selected mode
    for universe_id, data in (normal_data if mode == 'normal' else daily_data).items():
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

        # Render game page for the selected mode
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

        # Save the game page with a mode-specific filename
        output_file = os.path.join(output_folder, f"{universe_id}.html" if mode == 'normal' else f"daily_{universe_id}.html")
        with open(output_file, mode="w", encoding="utf-8") as htmlfile:
            htmlfile.write(output_html)

    return games

# Function to generate the home page
def generate_home_page(output_folder, games, mode="normal"):
    home_template = env.get_template("home_template.html")

    # Render home page
    output_html = home_template.render(games=games, mode=mode)

    # Save home page
    output_file = os.path.join(output_folder, "index.html")
    with open(output_file, mode="w", encoding="utf-8") as htmlfile:
        htmlfile.write(output_html)

# Paths
csv_folder = "./game_data"  # Folder where your CSV files are stored
output_folder = "./html_pages"  # Folder to store the generated HTML files

# Generate pages
mode = "normal"  # Change to "daily" to use daily data
games = generate_game_pages(csv_folder, output_folder, mode)
generate_home_page(output_folder, games, mode)

# For daily mode generation
daily_mode = "daily"
games_daily = generate_game_pages(csv_folder, output_folder, daily_mode)
generate_home_page(output_folder, games_daily, daily_mode)

print(f"HTML pages and home page generated in: {output_folder}")
