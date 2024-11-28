from doctest import debug
from fileinput import filename
from typing import override

import flask
from flask import Flask, request, render_template
from werkzeug.utils import redirect

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


app.run(host="localhost", port=8080, debug=True)
