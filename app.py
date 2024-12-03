from flask import Flask, request, render_template
import json
import pathlib
import os

app = Flask(__name__)
CONFIG_PATH = "config.json"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/fursona")
def fursona():
    return render_template("fursona.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/gaming")
def gaming():
    return render_template("gaming.html")


@app.route("/files")
def files():
    return render_template("files.html", files=os.listdir(FILE_SERVE_PATH))


@app.route("/files/<path:filename>")
def file_path(path):
    pass


with open(CONFIG_PATH, "r") as f:
    cfg = json.loads(f.read())
    FILE_SERVE_PATH = cfg.get("file_serve_path")
    app.run(host=cfg.get("host"), port=cfg.get("port"), debug=cfg.get("debug"))
