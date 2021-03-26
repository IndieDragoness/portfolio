from flask import Flask
from flask import render_template

# Static is where all of our static files are stored
app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.htm")
