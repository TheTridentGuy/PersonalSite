from flask import Flask, request, render_template, send_file, abort, url_for
from werkzeug.exceptions import HTTPException
import flask_login
from pathlib import Path
import re
import hashlib
import secrets
import logging

from config import HOST, PORT, FILE_SERVE_PATH, UPLOAD_PASS_HASH, NEKO_API_ENDPOINTS, BLAHAJ_IMG_DATA, DEBUG

app = Flask(__name__)
logging.basicConfig(filename=Path(__file__).parent.resolve()/Path("app.log"), filemode="a")
logging.getLogger().addHandler(logging.StreamHandler())
logger = logging.getLogger()
logger.setLevel(logging.INFO)
app.secret_key = secrets.token_hex(16)
login_manager = flask_login.LoginManager()
# login_manager.init_app(app)


class File:
    def __init__(self, path, name):
        self.is_dir = False
        self.path = path
        self.name = name


class Directory:
    def __init__(self, path, name, subdirs=(), files=()):
        self.path = path
        self.is_dir = True
        self.name = name
        self.subdirs = subdirs
        self.files = files


def generate_dir(path: Path):
    files = []
    subdirs = []
    for file in sorted(path.iterdir()):
        if file.is_dir():
            subdirs.append(generate_dir(file))
        else:
            files.append(File(path=(path/file).relative_to(FILE_SERVE_PATH), name=file.name))
    return Directory(path=path.relative_to(FILE_SERVE_PATH), name=path.name, subdirs=subdirs, files=files)


def check_path(path):
    return path.resolve().is_relative_to(Path(FILE_SERVE_PATH))


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
        "data": request.data.decode("utf-8"),
    }
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


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/files")
def files():
    return render_template("files.html")

@app.route("/card")
def card():
    return render_template("card.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/music")
def music():
    id = request.args.get("id")
    return render_template("music.html", id=id)

@app.route("/f")
@app.route("/public/files")
def publicfiles():
    files = generate_dir(Path(FILE_SERVE_PATH))
    preview = True if request.values.get("preview") == "true" else False
    return render_template("publicfiles.html", files=files, preview=preview)


@app.route("/f/<path:filename>")
@app.route("/public/files/<path:filename>")
def file_path(filename):
    path = Path(FILE_SERVE_PATH)/Path(filename)
    if check_path(path) and path.exists():
        return send_file(path, as_attachment=False)
    else:
        abort(404)


@app.route("/admin/public/files/upload/<path:uploadpath>", methods=["POST", "GET"])
@app.route("/admin/public/files/upload", methods=["POST", "GET"])
def upload(uploadpath=""):
    if request.method == "POST":
        password = request.values.get("password")
        if password and hashlib.sha256(password.encode("utf-8")).hexdigest() == UPLOAD_PASS_HASH:
            files = request.files.getlist("files")
            for file in files:
                while (Path(FILE_SERVE_PATH)/Path(uploadpath)/Path(file.filename)).exists():
                    file.filename=re.sub(r"(?=\.\w+$)|$", "-"+secrets.token_hex(4), file.filename, count=1)
                save_path = Path(FILE_SERVE_PATH)/Path(uploadpath)/Path(file.filename)
                if check_path(save_path):
                    file.save(save_path)
                else:
                    abort(400)
        else:
            return render_template("message.html", message="401: UwU, who's this, you aren't supposed to be here", title="401 Unauthorized"), 401
    else:
        return render_template("upload.html", form_path="/admin/public/files/upload"+("/"+uploadpath) if uploadpath else "", upload_path=uploadpath if uploadpath else "/")
    return render_template("message.html", message="File(s) uploaded succesfully!", title="TheTridentGuy - Upload Successful")


@app.route("/uwu")
def uwu():
    content_filter = request.values.get("filter")
    return render_template("uwu.html", api_url=NEKO_API_ENDPOINTS[content_filter if content_filter else ""])

@app.route("/blahaj")
def blahaj():
    return render_template("blahaj.html", img_data=[(caption, img_url) for caption, img_url in BLAHAJ_IMG_DATA])


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        password = request.values.get("password")
        if password and hashlib.sha256(password.encode("utf-8")).hexdigest() == UPLOAD_PASS_HASH:
            user = flask_login.UserMixin()
            flask_login.login_user(user)
            return render_template("message.html", message="Logged in successfully!", title="TheTridentGuy - Login Successful")
        else:
            return render_template("message.html", message="401: UwU, who's this, you aren't supposed to be here", title="401 Unauthorized"), 401
    else:
        return render_template("login.html")


@app.route("/blog/<path:filepath>")
def blog_article(filepath):
    return render_template(f"blog/{filepath}.html")


@app.errorhandler(HTTPException)
def handle_exception(e):
    if e.code == 500:
        return render_template("message.html", message="500: OwOopsie, something went wrong!", title="500 Internal Server Error"), e.code
    elif e.code == 404:
        return render_template("message.html", message="404: TwT, we couldn't find this page!", title="404 Not Found"), e.code
    elif e.code == 400:
        return render_template("message.html", message="400: OwOah there, stop trying to hack me!", title="400 Bad Request"), e.code
    else:
        return render_template("message.html", message=f"{e.code}: {e.name}", title=f"{e.code}: {e.name}"), e.code


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
