#! /bin/bash
source ../.venv/bin/activate
# edit this for however many workers you want:
gunicorn -w 10 "app:app"
