from flask import Flask, render_template, redirect, abort
import os
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    images = os.listdir("./static/images")
    return render_template("index.html", images=images)

if "__main__" == __name__:
    app.run(host='0.0.0.0', port=5000, debug=True)
