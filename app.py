from flask import Flask, jsonify, render_template, session, url_for, redirect, session, make_response
from flask_dance.contrib.discord import make_discord_blueprint, discord
from flask_login import login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from jinja2 import Environment
from sqlhelper import *
from api import *
import uuid
import yaml

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

if __name__ == '__main__':
    app.run(host=CONFIG['flask']['host'], port=CONFIG['flask']['port'])

