from flask import Flask, render_template, request
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.core.exceptions import ResourceExistsError
import logging
import json

# Microsoft Azure Cosmos DB Initialization
# Create Cosmos Client
endpoint = "https://sage-portfolio-app-cosmos-db.documents.azure.com:443/"
key = '7nRJrStRSOvKyV4VbONqB10qZ2SjOiASCqsjNWa3CXMs8tabxOvl2o68MN4A7FJ9P20TfPsR7zMpIym0Zm7tUA=='
client = CosmosClient(endpoint, key)

database_name = 'Portfolio_DB'
database = client.get_database_client(database_name)

container_name = 'Portfolio_Container'
container = database.get_container_client(container_name)

# Flask
# Static is where all of our static files are stored
app = Flask(__name__, static_url_path='/static')

# Setup Flask Logging to record events at Runtime
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.htm")

# Section correlates to the Contact Form in index.htm
@app.route('/contact_form_action', methods=['POST'])
def contact_form_action():
    app.logger.info('Contact Form Submission Detected!')

    # Retrieve data from HTML inputs
    name = request.form['Name']
    email = request.form['Email']
    subject = request.form['Subject']
    message = request.form['Message']

    # Log data entered
    app.logger.info('Name: ' + name)
    app.logger.info('Email: ' + email)
    app.logger.info('Subject: ' + subject)
    app.logger.info('Message: ' + message)

    # Post data to Contact_Form container in Microsoft Azure Cosmos DB
    try:
        app.logger.info('Checking if email is already present in database...')
        # Portfolio Section is the Partition Key for the Portfolio Container (used for point reads and writes)
        new_entry = {'id': email, 'name': name, 'subject': subject, 'message': message, 'portfolio_section': "contact_form"}
        container.create_item(new_entry)
        app.logger.info('Email not present! Created new database entry successfully: ' + email)
    except ResourceExistsError:
        app.logger.info('Email already present in database. Adding new message to existing entry: ' + email)

        # Get the current entry in the database for this email and add this new message
        properties = container.read()
        app.logger.info(properties)
        items = container.read_all_items()
        app.logger.info(items)

        item = container.read_item(email, partition_key="contact_form")
        app.logger.info('Acquired item.\n{}'.format(item))

        message_count = 0
        for entry in item.keys():
            if 'message' in entry:
                message_count += 1
        app.logger.info('This is the {} message for this id.'.format(message_count))
        item["message{}".format(message_count)] = message
        updated_item = container.upsert_item(item)

    # Scroll the page down to the Contact Form, after Submit is pressed, and say 'Thank you!'
    return render_template("/index.htm", submit_button_pressed="contact")