#!/bin/bash
# Activate the virtual environment.
. $(poetry env info --path)/bin/activate

# Run telegram bot.
python /app/src/app.py
