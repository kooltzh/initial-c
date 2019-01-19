import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from difflib import SequenceMatcher

from multiprocessing import Queue
import requests
from genkey import *

Sen_ipAddress = 'localhost:5010'

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'localChat.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

app.config['SECRET_KEY'] = 'thisismysecret'

db = SQLAlchemy(app)


def sendJSON(ipAddress, path, JSON):
    r = False
    URL = 'http://' + ipAddress + path
    try:
        r = requests.post(url=URL, data=JSON)
    except Exception as e:
        print(e)
        print("failed to connect to {}".format(URL))
    return r

    

# define class for user database
class chatdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(15))
    sender = db.Column(db.String(15))
    msg = db.Column(db.String(300))
    time = db.Column(db.String(50))


@app.route('/msg/load')
def loading_msg():
    data = {
        'sender': '',
        'msg': '',
        'time': ''
    }
    full_list = {}
    # try:
    current_user = db.session.query(chatdata.id, chatdata.target).order_by(chatdata.id.desc()).first().target
    items = db.session.query(chatdata.target, chatdata.sender, chatdata.msg, chatdata.time).all()
    for item in items:
        data['sender'] = item.sender
        data['msg'] = item.msg
        data['time'] = item.time
        if item.target in full_list.keys():
            full_list[item.target].append(data.copy())
        else:
            full_list[item.target] = [data.copy()]

    return jsonify({'msgList': full_list, 'currentUser': current_user}), 200
    # except:
    #     data = {
    #         'message': 'Unable to read from localChat.db'
    #     }
    #     return jsonify(data), 201

# TODO adding sending message to /send_msg
@app.route('/msg/send', methods=['POST'])
def sending_msg():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['target', 'sender', 'msg', 'time']

    if not all(k in values for k in required):
        return 'Missing values', 400

    new_entry = {
        'target': values['target'],
        'sender': values['sender'],
        'msg': values['msg'],
        'time': values['time'],
    }

    db.session.add(new_entry)
    db.session.commit()


@app.route('/inter_msg', methods=['POST'])
def inter_msg():
    msg = decrypt_msg(request.form['msg'], prikey)
    print(msg)
    qMsg.put(msg)
    return render_template('index.html')


@app.route('/get_msg')
@login_required
def get_msg():
    def gen():
        while True:
            yield 'data: {}\n\n'.format(qMsg.get())
    return Response(gen(), mimetype='text/event-stream')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global prikey, name
    if request.method == 'POST':
        data = request.form
        data['password'] = generate_password_hash(data['password'], method='sha256')
        data['ipAddress'] = request.remote_addr

        if sendJSON(Sen_ipAddress, 'login', data):
            login_user(data, remember=data['remember'])
            return redirect(url_for('index'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form

        data['password'] = generate_password_hash(
            data['password'], method='sha256')
        # get public key
        _, pubkey = save_keys(data['username'])

        if sendJSON(Sen_ipAddress, 'signup', data):
            login_user(data, remember=data['remember'])
            return '<h1>New user has been created!</h1>'
        return '<h1>Invalid username or password</h1>'
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    if sendJSON(Sen_ipAddress, 'login', name):
        logout_user()
        prikey, pubkey = None, None
    return redirect(url_for('login'))

# TODO adding checking similarity
    data = {
        'message': 'Chat record had been added to the database'
    }
    return jsonify(data), 200

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='5000')
    app.run(port='5002', debug=True)


