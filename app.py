from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

@app.route("/")
def hello():
    print(os.getcwd())
    return render_template("index.htm")
