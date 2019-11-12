from flask import Flask, render_template, flash, url_for, redirect, session, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail, Message

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class LogOnForm(FlaskForm):
    name = StringField('User name', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('log on')

class LogInForm(FlaskForm):
    name = StringField('User Name:', validators=[DataRequired()])
    password = StringField('password:', validators=[DataRequired()])
    email = StringField('email:', validators=[DataRequired()])
    submit = SubmitField('submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<User %r>' % self.name

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

@app.shell_context_processor
def create_context():
    return dict(db=db, User=User)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LogOnForm()
    if form.validate_on_submit():
        flash('in function')
        #check if this user has registered
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            session['known'] = True
            session['user'] = user.name
            if form.password.data == user.password:
                flash('log on success')
                return redirect(url_for('home'))
            else:
                flash('password error')
                return redirect(url_for('index'))
        else:
            flash('please register')
            return redirect(url_for('login'))
    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LogInForm()

    if login_form.validate_on_submit():
        name = login_form.name.data
        password = login_form.password.data
        email = login_form.email.data

        if User.query.filter_by(name=name).first():
            flash('User name has already in use, choose for another user name.')
            return redirect(url_for('login'))
        else:
            newUser = User(name=name, password=password, email=email)
            db.session.add(newUser)
            db.session.commit()

            flash('You now have a new account, please verify your email as soom as you can.')
            send_email(email, 'New User Regiter!', 'email', name=name)
            return redirect(url_for('index'))

    return render_template('log-in.html', form=login_form)

@app.route('/home')
def home():
    return render_template('user-home.html', user=session.get('user'))

if "__main__" == __name__:
    app.run(debug=True)

