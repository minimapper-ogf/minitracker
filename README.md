# minitracker
Minitracker: A roblox game stats tracker.


This 'thing' will go to the roblox api and grabb data stuff cuz I was bored and wanted something like Rolimons for smaller games.
This was generated with CHatGPT while fixes and other things less improtant I did

---

## How It Works

1. **Main Python Script (`app.py`)**
   - The script continuously monitors the system time.
   - It runs the following tasks:
     - **Daily Script (`app_daily.sh`)**: Executes at 12:00 PM every day.
     - **Regular Scripts (`fetch_data.py` and `generate_html.py`)**: Executes every 10 minutes.

2. **Daily Script (`app_daily.sh`)**
   - This Bash script runs `fetch_data_daily.py` to fetch daily data.
   - Waits for 1 minute to ensure data fetching is complete.
   - Runs `generate_daily_html.py` to generate the daily HTML file.
     - You can find the HTML files when you open any of the games folders and click the 'Daily' button. If nothing loads it may be because it only generates the page after 12:00 PM when all the daily data is gathered.

3. **Regular Scripts (`fetch_data.py` and `generate_html.py`)**
   - These Python scripts fetch and generate data/HTML files every 10 minutes.

4. **Logging**
   - Logs can be added to capture output and errors for debugging purposes.

---

## Setup Instructions

### Step 1: Configure `config.json` to the games you need
`config.json` is quite simple to manage as it only needs the universe id's of all games you want to track and as the script runs it will automatically add it in next update.
To get universe id's for the file you need to go to the play page of whatever game you want to track in your browser and view source of that page. In there look for 'data-universe-id'. Both results will have the same number to the right of them, copy that and paste it into your json.


### Step 2: Running
It should be quite simple to run if I have not messed up any of the scripts but you can use cd to where you put the repository and run ```python3 app.py```. If that fails I have no clue as of right now but I will try to fix it as soon as possible.

---

## Script Details

### `scheduled_tasks.py`
- **Triggers:**
  - **Daily at Noon:** Runs `app_daily.sh`.
  - **Every 10 Minutes:** Runs `fetch_data.py` and `generate_html.py`.
- **Core Logic:**
  - Checks the system time every second.
  - Ensures scripts don’t run multiple times within the same minute.

### `app_daily.sh`
- Fetches daily data and generates daily HTML files.
- Includes a 1-minute delay to ensure data fetching is complete.

### `fetch_data.py` and `generate_html.py`
- Fetch data and generate HTML files every 10 minutes.

---

After setup you should be all good to go! 
If there any problems place an issue and I will try my best to fix it!
