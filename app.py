from flask import Flask, request, render_template, send_file, abort
from werkzeug.exceptions import HTTPException
import json
from pathlib import Path
import re
import hashlib
import secrets
import logging

app = Flask(__name__)
CONFIG_PATH = Path(__file__).parent.resolve()/Path("config.json")


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


logging.basicConfig(filename=Path(__file__)/Path("app.log"),
                    filemode='w')
logger = logging.getLogger()


@app.before_request
def log_request():
    request_data = {
        "remote_addr": request.remote_addr,
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "json": request.json,
        "data": request.data.decode("utf-8"),
    }
    logger.info(request_data)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ip")
def ip():
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


@app.route("/files")
def files():
    files = generate_dir(Path(FILE_SERVE_PATH))
    preview = True if request.values.get("preview") == "true" else False
    return render_template("files.html", files=files, preview=preview)


@app.route("/files/<path:filename>")
def file_path(filename):
    path = Path(FILE_SERVE_PATH)/Path(filename)
    if check_path(path):
        return send_file(path, as_attachment=False)
    else:
        abort(404)


@app.route("/admin/files/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        password = request.values.get("password")
        if password and hashlib.sha256(password.encode("utf-8")).hexdigest() == UPLOAD_PASS_HASH:
            files = request.files.getlist("files")
            for file in files:
                while (Path(FILE_SERVE_PATH)/Path(file.filename)).exists():
                    file.filename=re.sub(r"(?=\.\w+$)|$", "-"+secrets.token_hex(4), file.filename, count=1)
                save_path = Path(FILE_SERVE_PATH)/Path(file.filename)
                assert save_path.resolve().is_relative_to(Path(FILE_SERVE_PATH))
                if check_path(save_path):
                    file.save(save_path)
                else:
                    abort(400)
        else:
            return render_template("message.html", message="401: UwU, who's this, you aren't supposed to be here", title="401 Unauthorized"), 401
    else:
        return render_template("upload.html", form_path="/admin/files/upload", upload_path="/")
    return render_template("message.html", message="File(s) uploaded succesfully!", title="TheTridentGuy - Upload Successful")


@app.route("/admin/files/upload/<path:uploadpath>", methods=["POST", "GET"])
def upload_to(uploadpath):
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
        return render_template("upload.html", form_path="/admin/files/upload/"+uploadpath, upload_path=uploadpath)
    return render_template("message.html", message="File(s) uploaded succesfully!", title="TheTridentGuy - Upload Successful")


@app.errorhandler(HTTPException)
def handle_exception(e):
    if e.code == 500:
        return render_template("message.html", message="500: OwOopsie, something went wrong!", title="500 Internal Server Error")
    elif e.code == 404:
        return render_template("message.html", message="404: TwT, we couldn't find this page!", title="404 Not Found")
    elif e.code == 400:
        return render_template("message.html", message="400: OwOah there, stop trying to hack me!", title="400 Bad Request")
    else:
        return render_template("message.html", message=f"{e.code}: {e.name}", title=f"{e.code}: {e.name}")


with open(CONFIG_PATH, "r") as f:
    cfg = json.loads(f.read())
    FILE_SERVE_PATH = cfg.get("file_serve_path")
    UPLOAD_PASS_HASH = cfg.get("upload_pass_hash")
    app.run(host=cfg.get("host"), port=cfg.get("port"), debug=cfg.get("debug"))

