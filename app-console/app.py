from flask import Flask, render_template, redirect, abort
import os
app = Flask(__name__)

@app.route('/')
def index():
    images = os.listdir("./static/images")
    return render_template("index.html", images=images)

