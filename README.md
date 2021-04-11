# Portfolio Website Documentation

# Table of Contents
* Quick commands and steps for management: [Quick Reference](#quick-reference)
* [Summary](#summary)
  * [Directory Structure](#directory-structure)
  * [Adding a New Webpage](#adding-a-new-webpage)
  * [Adding a Download File Button](#adding-a-download-file-button)
  * [Accessing the Cosmos Database](#accessing-the-cosmos-database)
  * [Run Web App Locally for Testing](#run-web-app-locally-for-testing)
  * [Tools Involved in this Project](#tools-involved-in-this-project)
  * [Environment Variables](#environment-variables)

## Microsoft Azure Specific Sections
* [Quickstart for Python Flask](#microsoft-azure-quickstart-for-python-flask)
* [Environment Variables](#microsoft-azure-environment-variables)
* [Flask Webapp Troubleshooting Guide](#microsoft-azure-flask-webapp-troubleshooting-guide)

## Microsoft Azure Cosmos DB
* [Cosmos DB](#cosmos-db)
  * [Partition Key](#partition-key)

## Python Flask Specific Sections
* [Python Flask](#python-flask)
  * [Error: Template Not Found](#template-not-found)
  * [Error: Missing End of Comment Tag](#missing-end-of-comment-tag)
  * [Interfacing with HTML Contact Form](#interfacing-with-html-contact-form)

## CSS Specific Sections
* [CSS Structures](#css-structures)
  * [Tailoring to Mobile vs Desktop using Media Queries](#tailoring-to-mobile-vs-desktop-using-media-queries)
  * [Autoscaling Youtube Videos to Any Resolution](#autoscaling-youtube-videos)
* [CSS Sources](#css-sources)

## HTML Specific Sections
* [HTML Structures](#html-structures)
  * [Main Tag](#main-tag)
* [HTML Example Elements](#html-example-elements)
  * [Navbar on Small Screens](#navbar-on-small-screens)
  * [Navbar on Bigger Screens](#navbar-on-bigger-screens)
  * [Page Content and Header](#page-content-and-header)
  * [About Section](#about-section)
  * [Grid for Pricing Tables](#grid-for-pricing-tables)
  * [Testimonials](#testimonials)
  * [Portfolio Section](#portfolio-section)
  * [Footer](#footer)
* [HTML Sources](#html-sources)

## VENV
* [venv Lightweight Python Virtual Environment](#venv-lightweight-python-virtual-environment)
  * [Creating Virtual Environments](#creating-virtual-environments)

# Quick Reference
Workflow goes like this:
1. Dev in Visual Studio, from `C:\Users\R\Documents\GitHub\portfolio`.
2. `Commit`, then `Push` to GitHub repo `https://github.com/IndieDragoness/portfolio`.
3. Go to the [Microsoft Azure Portal, Deployment Center](https://portal.azure.com/#@gtvault.onmicrosoft.com/resource/subscriptions/e52de545-f8f0-424a-9954-5a4d4aa548d2/resourceGroups/portfolio-app/providers/Microsoft.Web/sites/sages-portfolio/vstscd) and make sure you have a GitHub actions setup to automatically deploy the GitHub repo Master to the app.

# Summary
The goal of this worksheet is to provide the steps to develop and maintain a Python Flask based portfolio
website on Microsoft Azure's free cloud service/subdomain. The subdomain is `<app_name>.azurewebsites.net` and while
normally having your own domain name would be preferable, this subdomain confirms to viewers that the Azure
service has been used. This demonstrates both my projects, but also my Microsoft Azure skills. In addition,
doxygen can be used to connect this tutorials to others in a web format in combination with Markdown.

When deploying a web app to Azure, Azure creates a `gunicorn` web server to serve your app. This looks for a file called
`app.py` in your directory.

Good reference page is: [Configure a Linux Python app for Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python)

## Directory Structure
`/app.py` - Where URL's are defined. Returns HTML pages from `templates` folder. Also returns downloads, and interfaces with Cosmos DB.

`/templates` - Where HTML pages are stored.

`/static` - All static files go here, and can be referred to in HTML pages using `static/your_resource`.
`/static/images` - All `.jpeg` and `.png` go here.
`/static/documents` - All `.pdf` and other docs go here.
`/static/styles` - All `.css` go here.
`/static/favicon.png` - The tiny icon that appears on the tab of the browser.
`/static/prism.js` - Javascript for PRISM code highlighting.

`/scripts` - Storage folder for additional Python scripts
`/scripts/__init__.py` - Used to tell Python this directory is a module. Don't put this in `/` home directory.
`/scripts/utilities.py` - Commonly used, generic functions go here.

`/requirements.txt` - Specifies the packages that the host should have loaded for the web app.

`/record.txt` - Records the App logging output. Custom logging can be added to `app.py` and other python scripts.

## Adding a New Webpage
All `.html` pages go in `/templates`. To add a new webpage, put it in there and then go to `app.py` and add a 
new 'reference' link to it so that the web app knows to serve it.
```
# Link to linux_project.htm
@app.route('/linux_project')
def linux_project():
    return render_template("linux_project.htm")
```

## Adding a Download File Button
First, add the new file to the `/static` folder (preferably in a spot that makes sense organizationally).

Second, make a reference to it in `app.py`. The `app.logger` portion is a custom log note that is added to `record.txt`.
```
# Download my RL-PCG Paper
@app.route('/unity_project/download_rlpcg_paper', methods=['POST'])
def download_rlpcg_paper():
    app.logger.info('Paper Download Detected!')
    return send_file('static/documents/Teaching_RL_PCG_via_Educational_Game.pdf', as_attachment=True)
```

Third, place the button in the `.html` page.
```
<form action="/unity_project/download_rlpcg_paper" method="POST">
    <button class="w3-button w3-light-grey w3-padding-large w3-section">
        <i class="fa fa-download"></i> Download My RLPCG Paper
    </button>
</form>
```

## Accessing the Cosmos Database
Theres several steps to accessing the database.

The first is to have a Database setup in the first place, with a Container in it. 
This is similar to the Database:Table relationship in MariaDB. When setting up the Container, be sure to add a good partition key
for the data you will need. For example, the data for the Contact Form on the main page is on the `contact_form` partition.
Additionally, in `app.py` the initialization is shown below the Azure text block.

Each entry to the Container needs to have a reference to the partition key `contact_form`.
```
item = container.read_item(email, partition_key="contact_form")
```

Second, make sure new entries include the `contact_form` key:value pair, or else they will be excluded.

To create new entries:
```
new_entry = {'id': email, 'name': name, 'message': subject + ": " + message, 'portfolio_section': "contact_form"}
container.create_item(new_entry)
```

To update an existing entry:
```
item["message{}".format(message_count)] = subject + ": " + message
updated_item = container.upsert_item(item)
```

## Run Web App Locally for Testing
See the VENV section for setting up a local environment to test the web app. `requirements.txt` specifies the modules to include,
such as Azure and Flask.

If running first time on a Windows computer: Using `CMD Prompt`, perform the following from within the `portfolio` directory (the one with app.py). 
```
py -3 -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt
```

If re-running existing project: Using `CMD Prompt`, perform the following from within the `portfolio` directory (the one with app.py). 
```
.venv\scripts\activate
pip install -r requirements.txt
```

If running first time on a Linux computer: Using `bash`, perform the following from within the `portfolio` directory (the one with app.py). 
```
# Linux systems only
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If re-running existing project: Using `bash`, perform the following from within the `portfolio` directory (the one with app.py). 
```
# Linux systems only
source .venv/bin/activate
pip install -r requirements.txt
```

Note: If you get an error saying the project wasn't found, make sure you are in the same directory as `app.py`.

## Environment Variables
Locally, set `.venv` environment variables in `activate.bat` for Windows using the `set` command.

In Azure, set the environment variables in `azure_portal/sages-portfolio/Configuration/Application settings`.

## Tools Involved in this Project
1. Hosting/Cloud: [Microsoft Azure/Azure CLI](https://docs.microsoft.com/en-us/cli/azure/)
2. Language: [Python 3.6+](https://www.python.org/download/releases/3.0/)
3. Backend: [Python Flask](https://flask.palletsprojects.com/en/1.1.x/)
  * Detect if a device is Mobile or Not: [Flask-Mobility](https://flask-mobility.readthedocs.io/en/latest/)
4. Frontend/Designing the UI/UX: [Adobe XD](https://www.adobe.com/products/xd.html)
  * [Mobile Version Design Video](https://www.youtube.com/watch?v=CORrv-qvfkU)
5. HTML Template: [W3 Porfolio Template Reactive Webpage](https://www.w3schools.com/w3css/tryw3css_templates_dark_portfolio.htm)
6. CSS
7. Javascript (Prism)
8. venv for virtual python environments (testing): [venv](https://docs.python.org/3/library/venv.html)

# Microsoft Azure Quickstart for Python Flask
* This page came from: [Microsoft Azure Quickstart for Python Flask](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask)
* Deploying Flask: [Python Flask Deployment Options (including Azure)](https://flask.palletsprojects.com/en/master/deploying/)

# Microsoft Azure Environment Variables
If your application requires any Environment Variables, create equivalent [App Service application settings](https://docs.microsoft.com/en-us/azure/app-service/configure-common#configure-app-settings).
These App Service settings appear to your code as environment variables, as described on [Access environment variables](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python#access-app-settings-as-environment-variables).

# Microsoft Azure Flask Webapp Troubleshooting Guide
The guide is [located here](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python#troubleshooting).

# Cosmos DB
The URI for the Portfolio app Cosmos DB is: [https://sage-portfolio-app-cosmos-db.documents.azure.com:443/](https://sage-portfolio-app-cosmos-db.documents.azure.com:443/)
You may also have to use the Database key.

## Partition Key
Cosmos DB uses a Partition Key that you must manually specify in the Container and then implement as a `PartitionKey:Value` pair in your data.

More information [found here](https://azure.microsoft.com/en-us/resources/videos/azure-documentdb-elastic-scale-partitioning/).

# Python Flask
This portion of the `README` covers Python `Flask` steps. Python `Flask` is used by `Gunicorn` on Microsoft Azure to serve up the app.

[Full Flask Tutorial Series](https://www.tutorialspoint.com/flask/index.htm)

**Tips**
* Store `.html` files in the `templates` folder.
* Use `render_template` to render an entire `.html` page.
* Use `{% raw %}` to escape any special characters that throw errors.

## Template Not Found
This error frequently popped up due to `.html` files being in the wrong place. By default, `Flask` looks in the `/templates` folder.

## Missing End of Comment Tag
This error frequently popped up due to special characters in the `.html` files. The Flask Template system required me to use the following
to surround the special characters in the affect `.html` file:
```
{% raw %}Affected section of HTML{% endraw %}

{% raw %}
@media only screen and (max-width: 600px) {#main {margin-left: 0}}
{% endraw %}
```

## Interfacing with HTML Contact Form
Use [this tutorial](https://stackoverflow.com/questions/19213226/how-to-html-input-to-flask) to setup a contact form with Flask and HTML.

# CSS Structures
CSS is used for the 'style' of the webpage(s). It removes what used to be tags added to every page, and centralizes
them under a single 'style' section. It can be used to define the mobile vs. desktop render.

## Style Tag
* [Style Tag Reference](https://www.w3schools.com/tags/tag_style.asp)

Use of the <style> element to apply a simple style sheet to an HTML document:
```
<style>
body, h1,h2,h3,h4,h5,h6 {font-family: "Montserrat", sans-serif}
.w3-row-padding img {margin-bottom: 12px}
/* Set the width of the sidebar to 120px */
.w3-sidebar {width: 120px;background: #222;}
/* Add a left margin to the "page content" that matches the width of the sidebar (120px) */
#main {margin-left: 120px}
/* Remove margins from "page content" on small screens */
@media only screen and (max-width: 600px) {#main {margin-left: 0}}
</style>
```

The `<style>` tag is used to define style information (CSS) for a document.

Inside the `<style>` element you specify how HTML elements should render in a browser.

Note: When a browser reads a style sheet, it will format the HTML document according to the information in the style sheet. If some properties have been defined for the same selector (element) in different style sheets, the value from the last read style sheet will be used!
Tip: To link to an external style sheet, use the `<link>` tag.
Tip: To learn more about style sheets, please read our [CSS Tutorial](https://www.w3schools.com/css/default.asp).

## Tailoring to Mobile vs Desktop using Media Queries
The `@media` tag in the `<style>` section of the page can be used to tailor the webpage to different devices.

Media queries can be used to check many things, such as:

* width and height of the viewport
* width and height of the device
* orientation (is the tablet/phone in landscape or portrait mode?)
* resolution

Using media queries are a popular technique for delivering a tailored style sheet (responsive web design) to desktops, laptops, tablets, and mobile phones.

You can also use media queries to specify that certain styles are only for printed documents or for screen readers (mediatype: print, screen, or speech).

In addition to media types, there are also media features.
Media features provide more specific details to media queries, by allowing to test for a specific feature of the user agent or display device.
For example, you can apply styles to only those screens that are greater, or smaller, than a certain width.

## Autoscaling Youtube Videos
By default, YouTube videos do not scale easily between Desktop and Mobile. To fix this, use the following code (placed where the video should be):
```
<div style="left: 0; width: 100%; height: 0; position: relative; padding-bottom: 56.25%;">
    <iframe style="border: 0; top: 0; left: 0; width: 100%; height: 100%; position: absolute;"
            src="https://youtube.com/embed/your_video_code"
            allowFullScreen="allowFullScreen">
    </iframe>
</div>
```

# CSS Sources
* [CSS Tutorial](https://www.w3schools.com/css/default.asp)

# HTML Structures
This section covers the different code structures that exist in the portfolio webpage. Some are or are not used
in the actual end-state, this is for reference and to assist in creating future websites.

## Main Tag
The `<main>` tag specifies the main content of a document.

The content inside the `<main>` element should be unique to the document.
It should not contain any content that is repeated across documents such as sidebars, navigation links, copyright information, site logos, and search forms.

Note: There must not be more than one `<main>` element in a document.
The `<main>` element must NOT be a descendant of an `<article>`, `<aside>`, `<footer>`, `<header>`, or `<nav>` element.

# HTML Example Elements
Some general procedures.

Step 1: Specify Doctype
```
Add this to the top of the page: `<!DOCTYPE html>`
```

Step 2: HTML Tag
```
Open the html code with this: <html>
Put code here.
Close the html code with this: </html>
```

Step 3: Title
```
Add a title: <title>Sage Portfolio</title>
```

Step 4: Character Set
```
Add a character set: <meta charset="UTF-8">
```

Step 5: Viewport
```
Specify the viewport: <meta name="viewport" content="width=device-width, initial-scale=1">

The viewport is the user's visible area of a web page. Varies by device. Useful for interacting with both phones and computers.
```

Step 6: HTML Link Tag
```
To specify an external stylesheet: <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">

The <link> tag defines the relationship between the current document and an external resource.
The <link> tag is most often used to link to external style sheets.
The <link> element is an empty element, it contains attributes only.
```

Step 7: Specify [Style](#style-tag)
```
<style>
body, h1,h2,h3,h4,h5,h6 {font-family: "Montserrat", sans-serif}
.w3-row-padding img {margin-bottom: 12px}
/* Set the width of the sidebar to 120px */
.w3-sidebar {width: 120px;background: #222;}
/* Add a left margin to the "page content" that matches the width of the sidebar (120px) */
#main {margin-left: 120px}
/* Remove margins from "page content" on small screens. 'Raw' escapes special characters for Python Flask */
{% raw %}
@media only screen and (max-width: 600px) {#main {margin-left: 0}}
{% endraw %}
</style>
```

Step 8: Specify Body of Document
```
<body class="w3-black">
HTML Code here
</body>

The <body> tag defines the document's body.
The <body> element contains all the contents of an HTML document, such as headings, paragraphs, images, hyperlinks, tables, lists, etc.
```

Step 9: Use Div Tag to Separate Sections inside the Body:
```
   <div class="w3-row w3-center w3-padding-16 w3-section w3-light-grey">
      <div class="w3-quarter w3-section">
        <span class="w3-xlarge">11+</span><br>
        Partners
      </div>
      <div class="w3-quarter w3-section">
        <span class="w3-xlarge">55+</span><br>
        Projects Done
      </div>
      <div class="w3-quarter w3-section">
        <span class="w3-xlarge">89+</span><br>
        Happy Clients
      </div>
      <div class="w3-quarter w3-section">
        <span class="w3-xlarge">150+</span><br>
        Meetings
      </div>
    </div>

A <span> element which is used to color a part of a text:
The <span> tag is an inline container used to mark up a part of a text, or a part of a document.
The <span> tag is easily styled by CSS or manipulated with JavaScript using the class or id attribute.
The <span> tag is much like the <div> element, but <div> is a block-level element and <span> is an inline element.

A <div> element which is used as a container:
The <div> tag defines a division or a section in an HTML document.
The <div> tag is used as a container for HTML elements - which is then styled with CSS or manipulated with JavaScript.
The <div> tag is easily styled by using the class or id attribute.

Any sort of content can be put inside the <div> tag! 

Note: By default, browsers always place a line break before and after the <div> element.
```

Step 10: Use the Class Attribute to point to a Class Name in a Style Sheet.
```
<div class="w3-padding-64 w3-content" id="projects">

It can also be used by a JavaScript to access and manipulate elements with the specific class name.
```

Example:
```
Style sheet specifies the class:
<style>
.city {
  background-color: tomato;
  color: white;
  border: 2px solid black;
  margin: 20px;
  padding: 20px;
}
</style>

Div uses the class:
<div class="city">
  <h2>London</h2>
  <p>London is the capital of England.</p>
</div>
```

## Navbar on Small Screens

```
<!-- Navbar on small screens (Hidden on medium and large screens) -->
<div class="w3-top w3-hide-large w3-hide-medium" id="myNavbar">
  <div class="w3-bar w3-black w3-opacity w3-hover-opacity-off w3-center w3-small">
    <a href="#" class="w3-bar-item w3-button" style="width:25% !important">HOME</a>
    <a href="#about" class="w3-bar-item w3-button" style="width:25% !important">ABOUT</a>
    <a href="#projects" class="w3-bar-item w3-button" style="width:25% !important">PROJECTS</a>
    <a href="#contact" class="w3-bar-item w3-button" style="width:25% !important">CONTACT</a>
  </div>
</div>
```

## Navbar on Bigger Screens
The `<nav>` tag defines a set of navigation links.

Notice that NOT all links of a document should be inside a `<nav>` element.
The `<nav>` element is intended only for major block of navigation links.

Browsers, such as screen readers for disabled users, can use this element to determine whether to omit the initial rendering of this content.

Use `href="#"` to setup in-document navigation. For example, `href="#contact"` will take the user to the `contact` section.

```
<!-- Icon Bar (Sidebar - hidden on small screens) -->
<nav class="w3-sidebar w3-bar-block w3-small w3-hide-small w3-center">
  <!-- Avatar image in top left corner -->
  <img src="/images/chairs.jpg" style="width:100%">
  <a href="#" class="w3-bar-item w3-button w3-padding-large w3-black">
    <i class="fa fa-home w3-xxlarge"></i>
    <p>HOME</p>
  </a>
  <a href="#about" class="w3-bar-item w3-button w3-padding-large w3-hover-black">
    <i class="fa fa-user w3-xxlarge"></i>
    <p>ABOUT</p>
  </a>
  <a href="#projects" class="w3-bar-item w3-button w3-padding-large w3-hover-black">
    <i class="fa fa-eye w3-xxlarge"></i>
    <p>PROJECTS</p>
  </a>
  <a href="#contact" class="w3-bar-item w3-button w3-padding-large w3-hover-black">
    <i class="fa fa-envelope w3-xxlarge"></i>
    <p>CONTACT</p>
  </a>
</nav>
```
## Page Content and Header
Specifies the main class and the header. This is where the `Home` button sends the viewer when clicked.
The string `I'm` is not shown in mobile view. `Sage` is.
```
<!-- Page Content -->
<div class="w3-padding-large" id="main">
  <!-- Header/Home -->
  <header class="w3-container w3-padding-32 w3-center w3-black" id="home">
    <h1 class="w3-jumbo"><span class="w3-hide-small">I'm</span> Sage.</h1>
    <p>Senior Software Engineer.</p>
    <img src="static/images/laptop_rainbow.jpg" alt="laptop_rainbow" class="w3-image" width="992" height="1108">
  </header>
```

## About Section
```
  <!-- About Section -->
  <div class="w3-content w3-justify w3-text-grey w3-padding-64" id="about">
    <h2 class="w3-text-light-grey">My Name</h2>
    <hr style="width:200px" class="w3-opacity">
    <p>Some text about me. Some text about me. I am lorem ipsum consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
      ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum consectetur
      adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    </p>
    <h3 class="w3-padding-16 w3-text-light-grey">My Skills</h3>
    <p class="w3-wide">Photography</p>
    <div class="w3-white">
      <div class="w3-dark-grey" style="height:28px;width:95%"></div>
    </div>
    <p class="w3-wide">Web Design</p>
    <div class="w3-white">
      <div class="w3-dark-grey" style="height:28px;width:85%"></div>
    </div>
    <p class="w3-wide">Photoshop</p>
    <div class="w3-white">
      <div class="w3-dark-grey" style="height:28px;width:80%"></div>
    </div><br>
    
    <div class="w3-row w3-center w3-padding-16 w3-section w3-light-grey">
      <div class="w3-quarter w3-section">
        <span class="w3-xlarge">11+</span><br>
        Partners
      </div>
      <div class="w3-quarter w3-section">
        <span class="w3-xlarge">55+</span><br>
        Projects Done
      </div>
      <div class="w3-quarter w3-section">
        <span class="w3-xlarge">89+</span><br>
        Happy Clients
      </div>
      <div class="w3-quarter w3-section">
        <span class="w3-xlarge">150+</span><br>
        Meetings
      </div>
    </div>

    <button class="w3-button w3-light-grey w3-padding-large w3-section">
      <i class="fa fa-download"></i> Download Resume
    </button>
```
## Grid for Pricing Tables
```
      <!-- Grid for pricing tables -->
      <h3 class="w3-padding-16 w3-text-light-grey">My Price</h3>
      <div class="w3-row-padding" style="margin:0 -16px">
          <div class="w3-half w3-margin-bottom">
              <ul class="w3-ul w3-white w3-center w3-opacity w3-hover-opacity-off">
                  <li class="w3-dark-grey w3-xlarge w3-padding-32">Basic</li>
                  <li class="w3-padding-16">Web Design</li>
                  <li class="w3-padding-16">Photography</li>
                  <li class="w3-padding-16">5GB Storage</li>
                  <li class="w3-padding-16">Mail Support</li>
                  <li class="w3-padding-16">
                      <h2>$ 10</h2>
                      <span class="w3-opacity">per month</span>
                  </li>
                  <li class="w3-light-grey w3-padding-24">
                      <button class="w3-button w3-white w3-padding-large w3-hover-black">Sign Up</button>
                  </li>
              </ul>
          </div>

          <div class="w3-half">
              <ul class="w3-ul w3-white w3-center w3-opacity w3-hover-opacity-off">
                  <li class="w3-dark-grey w3-xlarge w3-padding-32">Pro</li>
                  <li class="w3-padding-16">Web Design</li>
                  <li class="w3-padding-16">Photography</li>
                  <li class="w3-padding-16">50GB Storage</li>
                  <li class="w3-padding-16">Endless Support</li>
                  <li class="w3-padding-16">
                      <h2>$ 25</h2>
                      <span class="w3-opacity">per month</span>
                  </li>
                  <li class="w3-light-grey w3-padding-24">
                      <button class="w3-button w3-white w3-padding-large w3-hover-black">Sign Up</button>
                  </li>
              </ul>
          </div>
          <!-- End Grid/Pricing tables -->
```

## Testimonials

```
<!-- Testimonials -->
<h3 class="w3-padding-24 w3-text-light-grey">My Reputation</h3>  
<img src="/w3images/bandmember.jpg" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="width:80px">
<p><span class="w3-large w3-margin-right">Chris Fox.</span> CEO at Mighty Schools.</p>
<p>John Doe saved us from a web disaster.</p><br>

<img src="/w3images/avatar_g2.jpg" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="width:80px">
<p><span class="w3-large w3-margin-right">Rebecca Flex.</span> CEO at Company.</p>
<p>No one is better than John Doe.</p>
```
## Portfolio Section
```
  <!-- Portfolio Section -->
  <div class="w3-padding-64 w3-content" id="projects">
    <h2 class="w3-text-light-grey">My Projects</h2>
    <hr style="width:200px" class="w3-opacity">

    <!-- Grid for photos -->
    <div class="w3-row-padding" style="margin:0 -16px">
      <div class="w3-half">
        <img src="/w3images/wedding.jpg" style="width:100%">
        <img src="/w3images/rocks.jpg" style="width:100%">
        <img src="/w3images/sailboat.jpg" style="width:100%">
      </div>

      <div class="w3-half">
        <img src="/w3images/underwater.jpg" style="width:100%">
        <img src="/w3images/chef.jpg" style="width:100%">
        <img src="/w3images/wedding.jpg" style="width:100%">
        <img src="/w3images/p6.jpg" style="width:100%">
      </div>
    <!-- End photo grid -->
    </div>
  <!-- End Portfolio Section -->
  </div>
```

## Footer
```
<!-- Footer with Social Media Icons -->
<footer class="w3-content w3-padding-64 w3-text-grey w3-xlarge">
    <i class="fa fa-facebook-official w3-hover-opacity"></i>
    <i class="fa fa-instagram w3-hover-opacity"></i>
    <i class="fa fa-snapchat w3-hover-opacity"></i>
    <i class="fa fa-pinterest-p w3-hover-opacity"></i>
    <i class="fa fa-twitter w3-hover-opacity"></i>
    <i class="fa fa-linkedin w3-hover-opacity"></i>
    <p class="w3-medium">Powered by <a href="https://www.w3schools.com/w3css/default.asp" target="_blank" class="w3-hover-text-green">w3.css</a></p>
    <!-- End footer -->
</footer>
```

# HTML Sources
* 

# PRISM Code Highlighting
The PRISM CSS and JavaScript files help label code in a beautiful way on the website.

The `prism.js` file needs to be stored in `static/` and the `prism.css` file needs to be stored in `static/styles/`.

To change plugins, re-download with the appropriate plugs checked/unchecked.

First, add the CSS and JavaScript references to the HTML page.
`prism.css`
```
<link rel="stylesheet" href="static/styles/prism.css">
```
`prism.js`
```
<script src="static/prism.js"></script>
</body>
```

Second, highlight the code. You can do this by removing an `<p>` paragraph tags, as those are not necessary.
Add the `<pre>` tag:
```
<pre>

</pre>
```

Third, use the `<code>` tag:
```
<pre>
    <code>

    </code>
</pre>
```

Fourth, add a class to code that calls out the specific language. Some possible ones are `language-javascript`, `language-python`, etc.
```
<pre>
    <code class="language-<this_language>">

    </code>
</pre>
```

# venv Lightweight Python Virtual Environment
Source (check for updates): [venv documentation](https://docs.python.org/3/library/venv.html)

The [venv](https://docs.python.org/3/library/venv.html#module-venv) module provides support for creating lightweight “virtual environments” with their own site directories, optionally isolated from system site directories.
Each virtual environment has its own Python binary (which matches the version of the binary that was used to create this environment) and can have its own independent set of installed Python packages in its site directories.

## Creating Virtual Environments
Useful for running local servers to test web pages!

Creation of virtual environments is done by executing the command `venv`:

```
### Linux Version
python3 -m venv /path/to/new/virtual/environment
```
```
### Windows Version
python -m venv c:\path\to\myenv
```

Running this command creates the target directory (creating any parent directories that don’t exist already) and places a `pyvenv.cfg` file in it with a home key pointing to the Python installation from which the command was run (a common name for the target directory is `.venv`).
It also creates a bin (or Scripts on Windows) subdirectory containing a copy/symlink of the Python binary/binaries (as appropriate for the platform or arguments used at environment creation time).
It also creates an (initially empty) `lib/pythonX.Y/site-packages` subdirectory (on Windows, this is `Lib\site-packages`).
If an existing directory is specified, it will be re-used.

The created `pyvenv.cfg` file also includes the `include-system-site-packages` key, set to true if `venv` is run with the `--system-site-packages` option, false otherwise.
Unless the `--without-pip` option is given, `ensurepip` will be invoked to bootstrap `pip` into the virtual environment.
Multiple paths can be given to `venv`, in which case an identical virtual environment will be created, according to the given options, at each provided path.
Once a virtual environment has been created, it can be “activated” using a script in the virtual environment’s binary directory. The invocation of the script is platform-specific (<venv> must be replaced by the path of the directory containing the virtual environment):

| Platform | Shell | Command to activate virtual environment |
| POSIX | bash/zsh | `$ source <venv>/bin/activate` |
| | fish | `$ source <venv>/bin/activate.fish` |
| | csh/tcsh | `$ source <venv>/bin/activate.csh` |
| | PowerShell Core | `$ <venv>/bin/Activate.ps1` |
| Windows | cmd.exe | `C:\> <venv>\Scripts\activate.bat` |
| | PowerShell | `PS C:\> <env>\Scripts\Activate.ps1` |

When a virtual environment is active, the VIRTUAL_ENV environment variable is set to the path of the virtual environment.
This can be used to check if one is running inside a virtual environment.

You don’t specifically need to activate an environment; activation just prepends the virtual environment’s binary directory to your path, so that “python” invokes the virtual environment’s Python interpreter and you can run installed scripts without having to use their full path.
However, all scripts installed in a virtual environment should be runnable without activating it, and run with the virtual environment’s Python automatically.

You can deactivate a virtual environment by typing “deactivate” in your shell.
The exact mechanism is platform-specific and is an internal implementation detail (typically a script or shell function will be used).




