from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test/<testName>')
def test(testName):
    if "test-flask-moment" == testName:
        return render_template('test-flask-moment.html', current_time = datetime.utcnow())
    else:
        return redirect(url_for('index'))

if "__main__" == __name__:
    app.run(host="0.0.0.0", port=5000, debug=True)
