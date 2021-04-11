from flask import Flask, render_template, request, send_file
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.core.exceptions import ResourceExistsError
from scripts import utilities
import logging
import json
import os

# ================================== #
#    _____                                  
#   /  _  \  ________ __ __ _______   ____  
#  /  /_\  \ \___   /|  |  \\_  __ \_/ __ \ 
# /    |    \ /    / |  |  / |  | \/\  ___/ 
# \____|__  //_____ \|____/  |__|    \___  >
#         \/       \/                    \/ 
#                                           
# ================================== #

# Microsoft Azure Cosmos DB Initialization
# Create Cosmos Client
endpoint = os.environ["COSMOS_DATABASE_ENDPOINT"]
key = os.environ["COSMOS_DATABASE_KEY"]
client = CosmosClient(endpoint, key)

database_name = os.environ["COSMOS_DATABASE_NAME"]
database = client.get_database_client(database_name)

container_name = os.environ["COSMOS_CONTAINER_NAME"]
container = database.get_container_client(container_name)

# ================================== #
# ___________.__                    __    
# \_   _____/|  |  _____     ______|  | __
#  |    __)  |  |  \__  \   /  ___/|  |/ /
#  |     \   |  |__ / __ \_ \___ \ |    < 
#  \___  /   |____/(____  //____  >|__|_ \
#      \/               \/      \/      \/
# ================================== #

# Static is where all of our static files are stored
app = Flask(__name__, static_url_path='/static')

# Setup Flask Logging to record events at Runtime
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route("/")
def main():
    return render_template("index.htm")

# Link to disc_drive_project.htm
@app.route('/disc_drive_project')
def disc_drive_project():
    return render_template("disc_drive_project.htm")

# Link to particle_accelerator_project.htm
@app.route('/particle_accelerator_project')
def particle_accelerator_project():
    return render_template("particle_accelerator_project.htm")

# Link to tensorflow_project.htm
@app.route('/tensorflow_project')
def tensorflow_project():
    return render_template("tensorflow_project.htm")

# Link to unity_project.htm
@app.route('/unity_project')
def unity_project():
    return render_template("unity_project.htm")

# Link to microsoft_azure_project.htm
@app.route('/microsoft_azure_project')
def microsoft_azure_project():
    return render_template("microsoft_azure_project.htm")

# Link to docker_project.htm
@app.route('/docker_project')
def docker_project():
    return render_template("docker_project.htm")

# Link to linux_project.htm
@app.route('/linux_project')
def linux_project():
    return render_template("linux_project.htm")

# Link to linux_project.htm
@app.route('/awx_ansible_project')
def awx_ansible_project():
    return render_template("awx_ansible_project.htm")

# Download my RL-PCG Paper
@app.route('/unity_project/download_rlpcg_paper', methods=['POST'])
def download_rlpcg_paper():
    app.logger.info('Paper Download Detected!')
    return send_file('static/documents/Teaching_RL_PCG_via_Educational_Game.pdf', as_attachment=True)

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
    try: # Try to create a new entry with given data
        app.logger.info('Checking if email is already present in database...')
        # Portfolio Section is the Partition Key for the Portfolio Container (used for point reads and writes)
        new_entry = {'id': email, 'name': name, 'message': subject + ": " + message, 'portfolio_section': "contact_form"}
        container.create_item(new_entry)
        app.logger.info('Email not present! Created new database entry successfully: ' + email)
    except ResourceExistsError: # Add to existing entry if unable to create a new one
        app.logger.info('Email already present in database. Adding new message to existing entry: ' + email)

        # Get the current entry in the database for this email and add this new message
        properties = container.read()
        app.logger.info(properties)
        items = container.read_all_items()
        app.logger.info(items)

        item = container.read_item(email, partition_key="contact_form")
        app.logger.info('Acquired item.\n{}'.format(item))

        # Get the number of keys containing "message" substring
        message_count = utilities.count_string_in_dictionary_keys(str_value="message", dict_value=item)

        app.logger.info('This is the {} message for this id.'.format(message_count))
        item["message{}".format(message_count)] = subject + ": " + message
        updated_item = container.upsert_item(item)

    # Scroll the page down to the Contact Form, after Submit is pressed, and say 'Thank you!'
    return render_template("/index.htm", submit_button_pressed="contact")