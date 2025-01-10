#! /bin/bash
cd ..
. .venv/bin/activate
# edit this for however many workers you want:
gunicorn -w 10 "PersonalSite.app:app"