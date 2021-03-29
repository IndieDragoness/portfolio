from flask import Flask, render_template, request

# Static is where all of our static files are stored
app = Flask(__name__, static_url_path='/static')

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.htm")

# Section correlates to the Contact Form in index.htm
@app.route('/contact_form_action', methods=['POST'])
def contact_form_action():
    # Retrieve data from HTML inputs
    name = request.form['Name']
    email = request.form['Email']
    subject = request.form['Subject']
    message = request.form['Message']

    # Scroll the page down to the Contact Form, after Submit is pressed, and say 'Thank you!'
    return render_template("/index.htm", submit_button_pressed="contact")