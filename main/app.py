import time
import subprocess
from datetime import datetime

def run_daily_script():
    # This function will run the daily script
    print("Running daily script...")
    subprocess.run(["/bin/bash", "/home/server/tracker/app_daily.sh"])

def run_regular_scripts():
    # This function runs the fetch and generate scripts
    print("Running fetch_data.py...")
    subprocess.run(["python3", "/home/server/tracker/fetch_data.py"])
    
    print("Running generate_html.py...")
    subprocess.run(["python3", "/home/server/tracker/generate_html.py"])

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
