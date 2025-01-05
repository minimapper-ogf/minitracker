#!/bin/bash
# Navigate to the directory containing the scripts
cd "$(dirname "$0")"

# Run fetch_data_daily.py
python3 fetch_data_daily.py

# Wait 1 minute to ensure data is fully fetched
sleep 60

# Run generate_daily_html.py
python3 generate_daily_html.py

#start with 'crontab -e'

#then add '0 12 * * * app_daily.sh'

#stop with 'crontab -e' then remove the line above
