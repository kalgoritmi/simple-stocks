#!/bin/bash 

if [ -d venv ]; then
  . venv/bin/activate
  echo "Activating virtual environment venv"
else
  echo "Creating virtual environment venv..."
  python -m venv venv
  if [ -f requirements.txt ]; then
    . venv/bin/activate && pip install -r requirements.txt
  else
    touch requirements.txt
  fi
fi
