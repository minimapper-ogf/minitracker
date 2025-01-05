#!/bin/bash

# Run fetch_data.py
echo "Running fetch_data.py..."
python3 fetch_data.py
echo "Completed fetch_data.py."

# Wait for 5 seconds before running generate_html.py
echo "Waiting for 5 seconds..."
sleep 5

# Run generate_html.py
echo "Running generate_html.py..."
python3 generate_html.py
echo "Completed generate_html.py."

