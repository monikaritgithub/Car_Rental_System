#!/bin/bash

echo "========================================================"
echo "Starting Smriti Car Rental System"
echo "========================================================"
echo ""

# Check if Python virtual environment exists, if not, create it
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo ""
echo "Initializing database and seed data..."
python scripts/seed_data.py

echo ""
echo "Starting Customer Application (Port 5000)..."
# Start the customer server in the background
python customer_server.py &
CUSTOMER_PID=$!

echo "Starting Admin Application (Port 5001)..."
# Start the admin server in the background
python admin_server.py &
ADMIN_PID=$!

echo ""
echo "Servers are running in the background."
echo "- Customer Interface: http://127.0.0.1:5000"
echo "- Admin Interface:    http://127.0.0.1:5001"
echo ""
echo "Press Ctrl+C to stop both servers."

# Trap SIGINT (Ctrl+C) and kill both background processes
trap "kill $CUSTOMER_PID $ADMIN_PID; exit" INT

# Wait indefinitely until interrupted
wait
