from flask import Flask, render_template, request
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json

# Microsoft Azure Cosmos DB Initialization
# Create Cosmos Client
endpoint = "https://sage-portfolio-app-cosmos-db.documents.azure.com:443/"
key = '7nRJrStRSOvKyV4VbONqB10qZ2SjOiASCqsjNWa3CXMs8tabxOvl2o68MN4A7FJ9P20TfPsR7zMpIym0Zm7tUA=='
client = CosmosClient(endpoint, key)

database_name = 'Portfolio_DB'
database = client.get_database_client(database_name)

container_name = 'Contact_Form'
container = database.get_container_client(container_name)

# Flask
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

    # Get current Contact_Form container in Microsoft Azure Cosmos DB
    items = list(container.query_items(
    query="SELECT * FROM c WHERE c.name IN ('Sage')",
    enable_cross_partition_query=True
    ))

    # Post data to Contact_Form container in Microsoft Azure Cosmos DB
    new_entry = {'id': str(len(items) + 1), 'name': name, 'email': email, 'subject': subject, 'message': message}
    container.create_item(new_entry)

    # Scroll the page down to the Contact Form, after Submit is pressed, and say 'Thank you!'
    return render_template("/index.htm", submit_button_pressed="contact")