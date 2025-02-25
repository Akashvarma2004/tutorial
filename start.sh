#!/bin/bash

# Define environment variables
echo "Setting up environment variables..."
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create one with the required Twitter API credentials."
    exit 1
fi
source .env

# Check for Python and required packages
echo "Checking for Python and required packages..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed. Please install it and try again."
    exit 1
fi

if ! python3 -m pip &> /dev/null; then
    echo "Error: pip is not installed. Installing pip..."
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3
fi

# Install necessary Python dependencies
echo "Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install flask flask-cors tweepy transformers

# Verify Flask installation
if ! python3 -m flask --version &> /dev/null; then
    echo "Error: Flask installation failed. Exiting."
    exit 1
fi

# Start the Flask server
echo "Starting Flask server..."
export FLASK_APP=server.py
python3 -m flask run --host=127.0.0.1 --port=5000 &
FLASK_PID=$!

# Open the web application
echo "Opening the web application in the default browser..."
sleep 5  # Give Flask server some time to start
if command -v xdg-open &> /dev/null; then
    xdg-open "http://127.0.0.1:5000"
elif command -v open &> /dev/null; then
    open "http://127.0.0.1:5000"
else
    echo "Warning: Could not detect a command to open the browser. Please manually visit http://127.0.0.1:5000."
fi

# Wait for the Flask server to stop
wait $FLASK_PID
