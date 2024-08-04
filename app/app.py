from flask import render_template, Flask, redirect, url_for, request, make_response, jsonify
from datetime import datetime, timedelta
from colorama import Fore, init
from jinja2 import TemplateNotFound
import json
import os

init(autoreset=True)
app = Flask(__name__)

# Loading configuration from the config => server.conf
defaultConfigPath = os.path.join('config', 'server.conf')
if os.path.exists(defaultConfigPath):
    with open(defaultConfigPath, 'r') as file:
        config = json.load(file)
    # Check if the required keys are in the config file
    if not all(key in config for key in ("host", "port", "debug")):
        config = {"host": "localhost", "port": 5000, "debug": "True"}
else:
    print(Fore.YELLOW + '[WARNING] No Configuration file - config/server.conf not Found, using default values!')
    config = {"host": "localhost", "port": 5000, "debug": "True"}

# defining routes
@app.route('/')
def index():
    return redirect(url_for('home')), 301

@app.route('/home') # Main Route
def home():
    try:
        username = request.cookies.get('username', 'You')
        return render_template('index.html', title='Home Page', username=username), 200
    except TemplateNotFound:
        return render_template('pageNotFound.html'), 404

@app.route('/test', methods=["GET", "POST"])
def test():
    if request.method == "POST":
        try:
            name = request.form.get('usrname')
            resp = make_response(redirect(url_for('home')))
            expiry = datetime.utcnow() + timedelta(days=1)  # Setting expiry to 1 day
            resp.set_cookie("username", name, expires=expiry)
            return resp
        except Exception as e:
            print(e)
            return jsonify({"msg": "You are using an external way to send a POST request, kinda breaching something? I have reported you!"}), 402
    try:
        return render_template('test.html', title='Test Area'), 200
    except TemplateNotFound:
        return render_template('pageNotFound.html'), 404

# Defining some error routes
@app.errorhandler(404)
def handle_template_not_found(error):
    return render_template('pageNotFound.html'), 404

if __name__ == "__main__":
    app.run(host=config["host"], port=int(config["port"]), debug=config["debug"].lower() == 'true')
