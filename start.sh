#!/bin/bash
echo "[INFO] Starting application..."
echo "Launching python environment"
source venv/bin/activate
sleep 5
python3 app.py
sleep 2

echo "[INFO] Application exited."
