import os
from flask import Flask, render_template, redirect, url_for, request, Response
from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'

# database location
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def sendJSON(ipAddress, JSON):
    URL = 'http://' + ipAddress + ':5000/inter_msg'
    try:
        r = requests.post(url=URL, data=JSON)
    except Exception as e:
        print(e)
        print("failed to connect to {}".format(URL))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    status = db.Column(db.Boolean)
    ipAddress = db.Column(db.String(15))
    pubkey = db.Column(db.String(128))


@app.route('/login', methods=['POST'])
def verf_login():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['username', 'password', 'ipAddress']
    if values is None:
        return 'Values is None', 400
    if not all(k in values for k in required):
        return 'Missing values', 400

    data = request.form
    user = User.query.filter_by(username=data['username']).first()
    if user:
        if user.password == data['password']:
            # update database
            user.status = True
            user.ipAddress = data['ipAddress']
            db.session.commit()
            return True

    return False


@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    new_user = User(username=data['username'],
                    email=data['number'], password=data['password'],
                    status=False, pubkey=data['pubkey'])
    db.session.add(new_user)
    db.session.commit()

    return True


@app.route('/get_rec_pub', methods=['POST'])
def get_rec_pub():
    data = request.form
    # get pubkey
    recipient = User.query.filter_by(username=data['recipient']).first()
    if recipient:
        rec_pubkey = recipient.pubkey
        return rec_pubkey
    else:
        return 'pubkey not found'


@app.route('/send_msg', methods=['POST'])
def send_msg():
    data = request.form
    # get ip address
    recipient = User.query.filter_by(username=data['recipient']).first()
    if recipient:
        rec_ipAddress = recipient.ipAddress
        JSON = {
            'sender': data['sender'],
            'msg': data['message']
        }
        sendJSON(rec_ipAddress, JSON)
        return True
    return False


@app.route('/logout')
def logout():
    data = request.form
    user = User.query.filter_by(username=data['username']).first()
    if user:
        # update database
        user.status = False
        db.session.commit()
        return True
    return False


if __name__ == '__main__':
    app.run(port=5010, debug=True)
