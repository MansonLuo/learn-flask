from flask import Flask, render_template, url_for, redirect, session, flash
from flask_bootstrap import Bootstrap
from forms import NameForm

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test/<testName>', methods=['POST', 'GET'])
def test(testName):
    name = None
    form = NameForm()
    if 'baseFlaskWtfForm' == testName:
        if form.validate_on_submit():
            name = form.name.data
            form.name.data = ''
        return render_template('baseFlaskWtfForm.html', form=form, name=name)
    elif 'redirectAndUserSession' == testName:
        if form.validate_on_submit():
            session['name'] = form.name.data
            form.name.data = ''

            return redirect(url_for('test', testName='redirectAndUserSession', form=form, name=name))
        return render_template('redirectAndUserSession.html', form=form, name=session.get('name'))
    elif 'flashedMessages' == testName:
        if form.validate_on_submit():
            old_name = session.get('name')
            if old_name is not None and form.name.data != old_name:
                flash("Look like you have changed your name!")
            session['name'] = form.name.data
            return redirect(url_for('test', testName='flashedMessages',form=form, name=session.get('name')))
        return render_template('flashedMessages.html', form=form, name=session.get('name'))

if '__main__' == __name__:
    app.run(host="0.0.0.0", port=5000, debug=True)
