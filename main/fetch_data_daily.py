import requests
import csv
import os
import time
import json
from datetime import datetime

# CONSOLE: this will let you modify some items but most of the options are in config.json
# NOTE: 0 is on for looping and 1 is off

SLEEP = 600  # Time to wait before fetching data again

# Function to fetch game data from the Roblox API
def fetch_game_data(universe_ids):
    base_url_games = "https://games.roblox.com/v1/games"
    base_url_votes = "https://games.roblox.com/v1/games/votes"

    universe_ids_str = ",".join(map(str, universe_ids))
    games_url = f"{base_url_games}?universeIds={universe_ids_str}"
    votes_url = f"{base_url_votes}?universeIds={universe_ids_str}"

    try:
        games_response = requests.get(games_url)
        votes_response = requests.get(votes_url)

        games_response.raise_for_status()
        votes_response.raise_for_status()

        games_data = games_response.json().get("data", [])
        votes_data = votes_response.json().get("data", [])

        votes_lookup = {item['id']: item for item in votes_data}
        combined_data = []

        for game in games_data:
            universe_id = game['id']
            combined_data.append({
                "universeId": universe_id,
                "name": game.get("name", ""),
                "playing": game.get("playing", 0),
                "visits": game.get("visits", 0),
                "favoritedCount": game.get("favoritedCount", 0),
                "upVotes": votes_lookup.get(universe_id, {}).get("upVotes", 0),
                "downVotes": votes_lookup.get(universe_id, {}).get("downVotes", 0),
            })

        return combined_data

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# Function to calculate changes based on the last CSV row
def calculate_changes(current, previous):
    if not previous:
        return {
            "visitschange": 0,
            "favoritedchange": 0,
            "upVoteschange": 0,
            "downVoteschange": 0,
            "upVotespercentage": 0.0
        }

    visitschange = current["visits"] - int(previous["visits"])
    favoritedchange = current["favoritedCount"] - int(previous["favoritedCount"])
    upVoteschange = current["upVotes"] - int(previous["upVotes"])
    downVoteschange = current["downVotes"] - int(previous["downVotes"])
    total_votes = current["upVotes"] + current["downVotes"]

    upVotespercentage = (current["upVotes"] / total_votes * 100) if total_votes > 0 else 0.0

    return {
        "visitschange": visitschange,
        "favoritedchange": favoritedchange,
        "upVoteschange": upVoteschange,
        "downVoteschange": downVoteschange,
        "upVotespercentage": upVotespercentage
    }

# Function to load the last row from a CSV file
def load_last_row(file_path):
    if not os.path.isfile(file_path):
        return None

    with open(file_path, mode="r", encoding="utf-8") as csvfile:
        reader = list(csv.DictReader(csvfile))
        if not reader:
            return None
        return reader[-1]

# Function to save game data to a CSV file
def save_to_csv(data, folder_path="game_data_daily"):  # Updated default folder name
    os.makedirs(folder_path, exist_ok=True)

    for game in data:
        universe_id = game["universeId"]
        file_path = os.path.join(folder_path, f"{universe_id}.csv")
        file_exists = os.path.isfile(file_path)

        previous_data = load_last_row(file_path)

        changes = calculate_changes(game, previous_data)

        with open(file_path, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                "timestamp", "name", "playing", "visits", "visitschange",
                "favoritedCount", "favoritedchange", "upVotes", "upVoteschange",
                "downVotes", "downVoteschange", "upVotespercentage"
            ])

            if not file_exists:
                writer.writeheader()

            game_to_write = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": game["name"],
                "playing": game["playing"],
                "visits": game["visits"],
                "visitschange": changes["visitschange"],
                "favoritedCount": game["favoritedCount"],
                "favoritedchange": changes["favoritedchange"],
                "upVotes": game["upVotes"],
                "upVoteschange": changes["upVoteschange"],
                "downVotes": game["downVotes"],
                "downVoteschange": changes["downVoteschange"],
                "upVotespercentage": changes["upVotespercentage"]
            }

            writer.writerow(game_to_write)

# Main script logic
def main():
    config_file = "config.json"
    folder_path = "game_data_daily"  # Updated folder path

    # Load config to check for loop control
    if not os.path.exists(config_file):
        print(f"Config file '{config_file}' not found. Please create one with a list of universe IDs and loop setting.")
        return

    with open(config_file, "r") as file:
        config = json.load(file)

    universe_ids = config.get("universeIds", [])
    loop_enabled = config.get("loopEnabled", 0)  # 0 to run in a loop, 1 to run once

    if not universe_ids:
        print("No universe IDs found in the config file.")
        return

    print("Starting data collection.")
    
    # If loop is enabled, keep fetching data
    if loop_enabled == 0:
        while True:
            print("Fetching game data...")
            data = fetch_game_data(universe_ids)
            if data:
                print("Saving data to CSV...")
                save_to_csv(data, folder_path)
                print("Data saved successfully.")
            else:
                print("No data fetched.")
            
            print(f"Waiting for {SLEEP} seconds...")
            time.sleep(SLEEP)  # Wait for the specified duration before fetching again
    else:
        # Fetch and save data once if loop is disabled
        print("Fetching game data...")
        data = fetch_game_data(universe_ids)
        if data:
            print("Saving data to CSV...")
            save_to_csv(data, folder_path)
            print("Data saved successfully.")
        else:
            print("No data fetched.")

if __name__ == "__main__":
    main()


