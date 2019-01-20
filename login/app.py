import os
from flask import Flask, render_template, redirect, url_for, request, Response
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from multiprocessing import Queue
import requests
from genkey import *

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class MessageForm(FlaskForm):
    recipient = StringField('recipient', validators=[InputRequired(), Length(max=10)])
    message = StringField('message', validators=[InputRequired(), Length(max=15)])


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = request.form
    return render_template('index.html')


@app.route('/get_users', methods=['POST'])
@login_required
def get_users():
    users = User.query.filter_by(username != name)
    
    filter_users = {}
    for user in users:
        filter_users['username'] = user['username']
        filter_users['status'] = user['status']
        
    return filter_users

@app.route('/login', methods=['GET', 'POST'])
def login():
    global prikey, name
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        if user:
            if check_password_hash(user.password, data['password']):
                login_user(user, remember=data['remember'])

                # update database
                user.status = True
                user.ipAddress = request.remote_addr
                db.session.commit()

                # get name
                name = data['username']
                # get private key
                prikey, _ = load_keys(name)
                return redirect(url_for('index'))

            return '<h1>Invalid username or password</h1>'
            #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global name

    if request.method == 'POST':
        data = request.form

        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        # get public key
        _, pubkey = save_keys(data['username'])
        # put sender name as global
        name = data['username']

        new_user = User(username=data['username'],
                        email=data['number'], password=hashed_password,
                        status=False, pubkey=RSA2str(pubkey))
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

    return render_template('signup.html')

@app.route('/send_msg', methods=['POST'])
@login_required
def send_msg():
    print('sad')
    data = request.form
    recipient = User.query.filter_by(username=data['recipient']).first()
    recipient = User.query.filter_by(username='pakzan').first()
    if recipient:
        rec_pubkey = recipient.pubkey
        rec_ipAddress = recipient.ipAddress
        print('asd')
        JSON = {
            'sender': name,
            'recipient': rec_pubkey,
            'msg': encrypt_msg(data['message'], str2RSA(rec_pubkey))
        }
        sendJSON(rec_ipAddress, JSON)
    return render_template('message.html')


@app.route('/inter_msg', methods=['POST'])
# @login_required
def inter_msg():
    msg = decrypt_msg(request.form['msg'], prikey)
    print(msg)
    qMsg.put(msg)
    return render_template('message.html')

@app.route('/get_msg')
@login_required
def get_msg():
    def gen():
        while True:
            yield 'data: {}\n\n'.format(qMsg.get())
    return Response(gen(), mimetype='text/event-stream')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    prikey, pubkey = None, None
    return redirect(url_for('index'))

if __name__ == '__main__':
    qMsg = Queue()
    app.run(debug=True)
