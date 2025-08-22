import hashlib
import logging
import re
import secrets
from pathlib import Path

from flask import Flask, request, render_template, send_file, abort
from werkzeug.exceptions import HTTPException

from config import HOST, PORT, FILE_SERVE_PATH, UPLOAD_PASS_HASH, NEKO_API_ENDPOINTS, BLAHAJ_IMG_DATA, DEBUG

app = Flask(__name__)
logging.basicConfig(filename=Path(__file__).parent.resolve() / Path("app.log"), filemode="a")
logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@app.after_request
def log_request(response):
    request_data = {
        "user_agent": request.user_agent.string,
        "x-real-ip": request.headers.get("X-Real-IP"),
        "x-forwarded-for": request.headers.get("X-Forwarded-For"),
        "remote_addr": request.remote_addr,
        "method": request.method,
        "url": request.url,
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "data": request.data.decode("utf-8"), }
    logger.info(request_data)
    return response


# Static routes

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ip")
def ip():
    if request.headers.get("X-Real-IP"):
        return request.headers.get("X-Real-IP")
    elif request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0]
    return request.remote_addr


@app.route("/fursona")
def fursona():
    return render_template("fursona.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/gaming")
def gaming():
    return render_template("gaming.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/card")
def card():
    return render_template("card.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/music")
def music():
    id_ = request.args.get("id_")
    return render_template("music.html", id=id_)


@app.route("/uwu")
def uwu():
    content_filter = request.values.get("filter")
    return render_template("uwu.html", api_url=NEKO_API_ENDPOINTS[content_filter if content_filter else ""])


@app.route("/blahaj")
def blahaj():
    return render_template("blahaj.html", img_data=[(caption, img_url) for caption, img_url in BLAHAJ_IMG_DATA])


@app.errorhandler(HTTPException)
def handle_exception(e):
    if e.code == 500:
        return render_template("message.html", message="500: OwOopsie, something went wrong!",
                               title="500 Internal Server Error"), e.code
    elif e.code == 404:
        return render_template("message.html", message="404: TwT, we couldn't find this page!",
                               title="404 Not Found"), e.code
    elif e.code == 400:
        return render_template("message.html", message="400: OwOah there, stop trying to hack me!",
                               title="400 Bad Request"), e.code
    else:
        return render_template("message.html", message=f"{e.code}: {e.name}", title=f"{e.code}: {e.name}"), e.code


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
