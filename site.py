from flask import Flask, jsonify, render_template
from jinja2 import Environment
from sqlhelper import *
from api import *
import yaml

with open('config.yml', 'r') as f:
    CONFIG  = yaml.safe_load(f)

app = Flask(__name__)

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
    return render_template('userCards.j2', user=getUserName(did)[0], did=did, msets=getMonSets(), isets=getItemSets())

@app.route("/")
def home():
    return render_template('home.j2')

@app.route("/satchemon/")
def index():
    users = getAllUsers()
    return render_template('users.j2', users=users)

if __name__ == '__main__':
    app.run(host=CONFIG['flask']['host'], port=CONFIG['flask']['port'])
