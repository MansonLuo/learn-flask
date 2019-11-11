from flask import Flask, render_template, flash, url_for, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

import os

basedir = os.path.abspath(os.path.dirname(__name__))

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

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LogOnForm()

    if form.validate_on_submit():
        #check if this user has registered
        user = User.query.filter_by(name=form.name.data).first()
        if user:
            session['known'] = True
            session['user'] = user.name
            if form.password.data == user.password:
                flash('log on success')
                return render_template('user-home.html')
            else:
                flash('password error')
                return redirect(url_for('index'))
        else:
            flash('please register')
            return render_template('log-in.html')
    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logon_form = LogOnForm()
    login_form = LogInForm()

    if login_form.validate_on_submit():
        pass
    return render_template('index.html', form=logon_form)

if "__main__" == __name__:
    app.run(debug=True)

