from flask import Flask, jsonify, render_template, session, url_for, redirect, make_response, request, send_file, abort
from flask_dance.contrib.discord import make_discord_blueprint, discord
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from jinja2 import Environment
from sqlhelper import *
from api import *
import uuid
import yaml
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import os
import io


with open('config.yml', 'r') as f:
    CONFIG  = yaml.safe_load(f)

discord_bp = make_discord_blueprint(client_id=CONFIG['discord']['id'],
                                    client_secret=CONFIG['discord']['secret'],
                                    redirect_url='/auth',
                                    scope=['identify'])

app = Flask(__name__)
app.secret_key = CONFIG['flask']['secret']
app.register_blueprint(discord_bp, url_prefix="/discord")
login_manager = LoginManager(app)


class User(UserMixin):

    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(id):
    return User(id)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/auth')
@discord_bp.session.authorization_required
def auth():
    resp = discord.get('/api/users/@me').json()
    user = User(resp['id'])
    session['user'] = resp['global_name']
    login_user(user)
    uu = str(uuid.uuid4())
    setSession(uu, resp['id'])
    response = make_response(redirect(url_for('mycards')))
    response.set_cookie('session_id', uu)
    return response


@app.route('/satchemon/mycards')
@login_required
def mycards():
    return render_template('userCards.j2', user=getUserName(current_user.id)[0], did=current_user.id, msets=getMonSets(), isets=getItemSets(), lsets=getLocSets(), exps=getExpansions())


@app.route('/discord')
def discord_login():
    try:
        did = getSession(request.cookies.get('session_id'))
        if did:
            user = User(did)
            session['user'] = resp['global_name']
            login_user(user)
            return redirect(url_for('mycards'))
        else:
            return redirect(url_for('discord.login'))
    except:
        return redirect(url_for('discord.login'))

@app.route("/api/getAll")
def getAll():
    return apiGetAll()

@app.route('/api/cs/<c>/<did>')
def getCs(did,c): 
    return apiGetCs(did,c)

@app.route('/api/set/<s>/<did>')
def getCards(did,s):
    return apiGetCards(did,s)

@app.route("/satchemon/search")
def search():
    return render_template('search.j2')

@app.route("/satchemon/user/<user>")
def users(user):

    did = str(user)
    return render_template('userCards.j2', user=getUserName(did)[0], did=did, msets=getMonSets(), isets=getItemSets(), lsets=getLocSets(), exps=getExpansions())

@app.route("/home")
def home():
    return render_template('home.j2')

@app.route("/satchemon/")
def index():
    users = getAllUsers()
    return render_template('users.j2', users=users)

# ── Configuration ────────────────────────────────────────────────────────────
SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "gc.json")
FOLDER_ID            = os.environ.get("GOOGLE_DRIVE_FOLDER_ID", "1GPKCdlyjwEqDpLsJ5XUV1ak1zr52HF_z")
SCOPES               = ["https://www.googleapis.com/auth/drive.readonly"]

# ── Google Drive client ──────────────────────────────────────────────────────
def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


def list_images(folder_id: str):
    """Return list of image file metadata from a Drive folder."""
    service = get_drive_service()
    query = (
        f"'{folder_id}' in parents "
        "and trashed = false"
    )
    results = (
        service.files()
        .list(
            q=query,
            fields="files(id, name, mimeType)",
            orderBy="name",
            pageSize=200,
        )
        .execute()
    )
    return results.get("files", [])


@app.route("/CS")
def cs_index():
    return render_template("cs.html")


@app.route("/api/cs/images")
def api_images():
    """Return JSON list of image ids and names."""
    try:
        print('test')
        files = list_images(FOLDER_ID)
        print(files)
        return jsonify([{"id": f["id"], "name": f["name"]} for f in files])
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/image/<file_id>")
def serve_image(file_id: str):
    """Proxy an image from Google Drive so the browser can display it."""
    try:
        service = get_drive_service()
        meta = service.files().get(fileId=file_id, fields="mimeType,name").execute()
        mime = meta.get("mimeType", "image/jpeg")

        request = service.files().get_media(fileId=file_id)
        buf = io.BytesIO()
        downloader = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        buf.seek(0)
        return send_file(buf, mimetype=mime)
    except Exception as exc:
        print(f"Error serving image {file_id}: {exc}")
        abort(404)

if __name__ == '__main__':
    app.run(host=CONFIG['flask']['host'], port=CONFIG['flask']['port'])

