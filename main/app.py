import os
import time
import subprocess
from datetime import datetime

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_daily_script():
    # This function will run the daily script
    daily_script_path = os.path.join(SCRIPT_DIR, "app_daily.sh")
    print("Running daily script...")
    subprocess.run(["/bin/bash", daily_script_path])

def run_regular_scripts():
    # This function runs the fetch and generate scripts
    fetch_data_path = os.path.join(SCRIPT_DIR, "fetch_data.py")
    generate_html_path = os.path.join(SCRIPT_DIR, "generate_html.py")
    
    print("Running fetch_data.py...")
    subprocess.run(["python3", fetch_data_path])
    
    print("Running generate_html.py...")
    subprocess.run(["python3", generate_html_path])

def main():
    while True:
        current_time = datetime.now()
        
        # Run the daily script at noon
        if current_time.hour == 12 and current_time.minute == 0:
            run_daily_script()
            # Wait for 5 seconds to ensure it doesn't run multiple times in the same minute
            time.sleep(5)
        
        # Run the regular scripts every 10 minutes
        if current_time.minute % 10 == 0 and current_time.second == 0:
            run_regular_scripts()
            # Wait for 5 seconds to avoid multiple executions in the same minute
            time.sleep(5)
        
        # Sleep for a short time to avoid high CPU usage
        time.sleep(1)

if __name__ == "__main__":
    main()
