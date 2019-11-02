from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return '<p>hello</p>'

if "__main__" == __name__:
    app.run(host="0.0.0.0", host=5000, debug=True)
