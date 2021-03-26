# Portfolio Website Documentation

# Table of Contents
* [Summary](#summary)

## Microsoft Azure Specific Sections
* [Sources](#sources)
* [Setting up Initial Environment](#setting-up-initial-environment)
* [Checking Versions and Signing into Azure CLI](#checking-versions-and-signing-into-azure-cli)
* [Getting a Sample from Azure Github](#getting-a-sample-from-azure-github)
* [Run the Sample](#run-the-sample)
* [Deploy the App](#deploy-the-app)
  * [Things to Note](#things-to-note)
* [Browse to the App](#browse-to-the-app)
* [Redeploy Updates](#redeploy-updates)
* [Stream Logs](#stream-logs)
* [Manage the Azure App from the Azure Portal](#manage-the-azure-app-from-the-azure-portal)
* [Clean up Resources](#clean-up-resources)
* [Troubleshooting Guide](#troubleshooting-guide)

## Python Flask Specific Sections

## CSS Specific Sections
* [CSS Structures](#css-structures)
  * [Tailoring to Mobile vs Desktop using Media Queries](#tailoring-to-mobile-vs-desktop-using-media-queries)
* [CSS Sources](#css-sources)

## HTML Specific Sections
* [HTML Structures](#html-structures)
  * [Main Tag](#main-tag)
* [HTML Example Elements](#html-example-elements)
  * [Navbar on Small Screens](#navbar-on-small-screens)
* [HTML Global Event Attributes and JavaScript](#html-global-event-attributes-and-javaScript)
  * [Window Events](#window-events)
  * [Form Events](#form-events)
  * [Keyboard Events](#keyboard-events)
  * [Mouse Events](#mouse-events)
  * [Drag Events](#drag-events)
  * [Clipboard Events](#clipboard-events)
  * [Media Events](#media-events)
  * [Misc Events](#misc-events)
* [HTML Sources](#html-sources)

## Summary
The goal of this worksheet is to provide the steps to develop and maintain a Python Flask based portfolio
website on Microsoft Azure's free cloud service/subdomain. The subdomain is `.azurewebsites.net` and while
normally having your own domain name would be preferable, this subdomain confirms to viewers that the Azure
service has been used. This demonstrates both my projects, but also my Microsoft Azure skills. In addition,
doxygen can be used to connect this tutorials to others in a web format.

### Tools Involved in this Project
1. Hosting/Cloud: [Microsoft Azure/Azure CLI](https://docs.microsoft.com/en-us/cli/azure/)
2. Language: [Python 3.6+](https://www.python.org/download/releases/3.0/)
3. Backend: [Python Flask](https://flask.palletsprojects.com/en/1.1.x/)
  * Detect if a device is Mobile or Not: [Flask-Mobility](https://flask-mobility.readthedocs.io/en/latest/)
4. Frontend/Designing the UI/UX: [Adobe XD](https://www.adobe.com/products/xd.html)
  * [Mobile Version Design Video](https://www.youtube.com/watch?v=CORrv-qvfkU)
5. HTML
6. CSS

## Sources
* This page came from: [Microsoft Azure Quickstart for Python Flask](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask)

## Setting up Initial Environment
* Have an Azure account with an active subscription. Create an account for free.
* Install `Python 3.6` or higher.
* Install the `Azure CLI 2.0.80` or higher, with which you run commands in any shell to provision and configure Azure resources.

### Checking Versions and Signing into Azure CLI
To check Python: `python3 --version`
To check Azure CLI: `az --version`

This command opens a browser to gather your credentials. When the command finishes, it shows JSON output containing information about your subscriptions.
To sign in: `az login`

### Getting a Sample from Azure Github
You can also get a sample of Python Flask Azure deployment from their Github repo. This can be a great way to get
started.

Clone the sample repository using the following command and navigate into the sample folder.
(Install [git](https://git-scm.com/downloads) if you don't have git already.)

The sample contains framework-specific code that Azure App Service recognizes when starting the app.
* [Container startup proces](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python#container-startup-process)

## Run the Sample
To run Azure's sample follow this procedure:
1. Change directory:
  * `cd python-docs-hello-world`
2. Startup the virtual environment and install dependencies:
  * `python3 -m venv .venv`
  * `source .venv/bin/activate`
  * `pip install -r requirements.txt`
3. Run the development server:
  * `flask run`

By default, the server assumes that the app's entry module is in `app.py`, as used in the sample.
If you use a different module name, set the `FLASK_APP` environment variable to that name.
If you encounter the error, "Could not locate a Flask application. You did not provide the 'FLASK_APP' environment variable,
and a 'wsgi.py' or 'app.py' module was not found in the current directory.", make sure you're in the python-docs-hello-world
folder that contains the sample.

Open a web browser and go to the sample app at: http://localhost:5000/
The app displays the message Hello, World!.

In your terminal window, press Ctrl+C to exit the development server.

## Deploy the Sample/The App
Deploy the code in your local folder (python-docs-hello-world) using the az webapp up command:
* `az webapp up --sku FREE --name <app-name>`

### Things to Note
* If the az command isn't recognized, be sure you have the Azure CLI installed as described in [Set up your initial environment](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask#set-up-your-initial-environment).
* If the webapp command isn't recognized, it's because that your `Azure CLI` version isn't `2.0.80` or higher. [Install the latest version](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
* Replace `<app_name>` with a name that's unique across all of Azure (valid characters are a-z, 0-9, and -). A good pattern is to use a combination of your company name and an app identifier.
* The `--sku B1` argument creates the web app on the Basic pricing tier, which incurs a small hourly cost. Omit this argument to use a faster premium tier.
  * Example Tiers: `--sku {B1, B2, B3, D1, F1, FREE, I1, I1v2, I2, I2v2, I3, I3v2, P1V2, P1V3, P2V2, P2V3, P3V2, P3V3, PC2, PC3, PC4, S1, S2, S3, SHARED}`
* You can optionally include the argument `--location <location-name>` where `<location_name>` is an available Azure region. You can retrieve a list of allowable regions for your Azure account by running the `az account list-locations` command.
* If you see the error, "Could not auto-detect the runtime stack of your app," make sure you're running the command in the python-docs-hello-world folder (Flask) or the `python-docs-hello-django` folder (Django) that contains the requirements.txt file. (See [Troubleshooting auto-detect issues with az webapp up (GitHub)](https://github.com/Azure/app-service-linux-docs/blob/master/AzWebAppUP/runtime_detection.md).

The command may take a few minutes to complete. While running, it provides messages about creating the resource group, the App Service plan and hosting app, configuring logging, then performing ZIP deployment. It then gives the message, "You can launch the app at `http://<app-name>.azurewebsites.net`", which is the app's URL on Azure.

The `az webapp up` command does the following actions:
* Create a default resource group.
* Create a default app service plan.
* Create an app with the specified name.
* Zip deploy files from the current working directory to the app.

Visual Studio Code provides powerful extensions for Python and Azure App Service, which simplify the process of deploying Python web apps to App Service.
For more information, see [Deploy Python apps to App Service from Visual Studio Code](https://docs.microsoft.com/en-us/azure/python/tutorial-deploy-app-service-on-linux-01).

## Browse to the App
Browse to the deployed application in your web browser at the URL `http://<app-name>.azurewebsites.net`. It can take a minute or two for the the app to start, so if you see a default app page, wait a minute and refresh the browser.

The Python sample code is running a Linux container in App Service using a built-in image.

## Redeploy Updates
In this section, you make a small code change and then redeploy the code to Azure. The code change includes a print statement to generate logging output that you work with in the next section.

Open `app.py` in an editor and update the hello function to match the following code.

```
def hello():
    print("Handling request to home page.")
    return "Hello, Azure!"
```

Save your changes, then redeploy the app using the `az webapp up` command again:
* `az webapp up`

This command uses values that are cached locally in the `.azure/config` file, including the `app name`, `resource group`, and `App Service plan`.

Once deployment is complete, switch back to the browser window open to `http://<app-name>.azurewebsites.net`. Refresh the page, which should display the modified message:
* `Hello, Azure!`

## Stream Logs
You can access the console logs generated from inside the app and the container in which it runs. Logs include any output generated using `print` statements.

To stream logs, run the [az webapp log tail](https://docs.microsoft.com/en-us/cli/azure/webapp/log#az_webapp_log_tail) command:
* `az webapp log tail`

You can also include the `--logs` parameter with then az webapp up command to automatically open the log stream on deployment.

Refresh the app in the browser to generate console logs, which include messages describing HTTP requests to the app. If no output appears immediately, try again in 30 seconds.

You can also inspect the log files from the browser at `https://<app-name>.scm.azurewebsites.net/api/logs/docker`.

To stop log streaming at any time, press `Ctrl+C` in the terminal.

## Manage the Azure App from the Azure Portal
1. Go to the [Azure portal](https://portal.azure.com/) to manage the app you created. Search for and select `App Services`.
2. Select the name of your Azure app.
3. Selecting the app opens its Overview page, where you can perform basic management tasks like browse, stop, start, restart, and delete.
4. The App Service menu provides different pages for configuring your app.

## Clean up Resources
In the preceding steps, you created Azure resources in a resource group. The resource group has a name like "appsvc_rg_Linux_CentralUS" depending on your location. If you keep the web app running, you will incur some ongoing costs (see App Service pricing).

If you don't expect to need these resources in the future, delete the resource group by running the following command:
* `az group delete --no-wait`

The command uses the resource group name cached in the `.azure/config` file.

The `--no-wait` argument allows the command to return before the operation is complete.

## Troubleshooting Guide
The guide is [located here](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python#troubleshooting).

## CSS Structures
CSS is used for the 'style' of the webpage(s). It removes what used to be tags added to every page, and centralizes
them under a single 'style' section. It can be used to define the mobile vs. desktop render.

### Style Tag
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

### Tailoring to Mobile vs Desktop using Media Queries
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

## CSS Sources
* [CSS Tutorial](https://www.w3schools.com/css/default.asp)

## HTML Structures
This section covers the different code structures that exist in the portfolio webpage. Some are or are not used
in the actual end-state, this is for reference and to assist in creating future websites.

### Main Tag
The `<main>` tag specifies the main content of a document.

The content inside the `<main>` element should be unique to the document.
It should not contain any content that is repeated across documents such as sidebars, navigation links, copyright information, site logos, and search forms.

Note: There must not be more than one `<main>` element in a document.
The `<main>` element must NOT be a descendant of an `<article>`, `<aside>`, `<footer>`, `<header>`, or `<nav>` element.

## HTML Example Elements

### Navbar on Small Screens

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

### Navbar on Bigger Screens

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

### Testimonials
![]()

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

## HTML Global Event Attributes and JavaScript
HTML has the ability to let events trigger actions in a browser, like starting a JavaScript when a user clicks on an element.

[JavaScript tutorial](https://www.w3schools.com/js/default.asp).

Below are the global event attributes that can be added to HTML elements to define event actions.

### Window Events
Events triggered for the window object (applies to the <body> tag):

| Attribute        | Description      |
| ---------------- | ---------------- |
| [onafterprint](https://www.w3schools.com/tags/ev_onafterprint.asp) | Script to be run after the document is printed |
| [onbeforeprint](https://www.w3schools.com/tags/ev_onbeforeprint.asp) | Script to be run before the document is printed |
| [onbeforeunload](https://www.w3schools.com/tags/ev_onbeforeunload.asp) | Script to be run when the document is about to be unloaded |
| [onerror](https://www.w3schools.com/tags/ev_onerror.asp) | Script to be run when an error occurs |
| [onhashchange](https://www.w3schools.com/tags/ev_onhashchange.asp) | Script to be run when there has been changes to the anchor part of the a URL |
| [onload](https://www.w3schools.com/tags/ev_onload.asp) | Fires after the page is finished loading |
| `onmessage` | Script to be run when the message is triggered |
| [onoffline](https://www.w3schools.com/tags/ev_onoffline.asp) | Script to be run when the browser starts to work offline |
| [ononline](https://www.w3schools.com/tags/ev_ononline.asp) | 	Script to be run when the browser starts to work online |
| `onpagehide` | Script to be run when a user navigates away from a page |
| [onpageshow](https://www.w3schools.com/tags/ev_onpageshow.asp) | 	Script to be run when a user navigates to a page |
| `onpopstate` | Script to be run when the window's history changes |
| [onresize](https://www.w3schools.com/tags/ev_onresize.asp) | Fires when the browser window is resized |
| `onstorage` | Script to be run when a Web Storage area is updated |
| [onunload](https://www.w3schools.com/tags/ev_onunload.asp) | Fires once a page has unloaded (or the browser window has been closed) |

### Form Events
Events triggered by actions inside a HTML form (applies to almost all HTML elements, but is most used in form elements):

| Attribute        | Description      |
| ---------------- | ---------------- |
| [onblur](https://www.w3schools.com/tags/ev_onblur.asp) | Fires the moment that the element loses focus |
| [onchange](https://www.w3schools.com/tags/ev_onchange.asp) | Fires the moment when the value of the element is changed |
| [oncontextmenu](https://www.w3schools.com/tags/ev_oncontextmenu.asp) | Script to be run when a context menu is triggered |
| [onfocus](https://www.w3schools.com/tags/ev_onfocus.asp) | Fires the moment when the element gets focus |
| [oninput](https://www.w3schools.com/tags/ev_oninput.asp) | Script to be run when an element gets user input |
| [oninvalid](https://www.w3schools.com/tags/ev_oninvalid.asp) | Script to be run when an element is invalid |
| [onreset](https://www.w3schools.com/tags/ev_onreset.asp) | Fires when the Reset button in a form is clicked |
| [onsearch](https://www.w3schools.com/tags/ev_onsearch.asp) | Fires when the user writes something in a search field (for `<input="search">`) |
| [onselect](https://www.w3schools.com/tags/ev_onselect.asp) | Fires after some text has been selected in an element |
| [onsubmit](https://www.w3schools.com/tags/ev_onsubmit.asp) | Fires when a form is submitted |

### Keyboard Events
| Attribute        | Description      |
| ---------------- | ---------------- |
| [onkeydown](https://www.w3schools.com/tags/ev_onkeydown.asp) | Fires when a user is pressing a key |
| [onkeypress](https://www.w3schools.com/tags/ev_onkeypress.asp) | Fires when a user presses a key |
| [onkeyup](https://www.w3schools.com/tags/ev_onkeyup.asp) | Fires when a user releases a key |

### Mouse Events
| Attribute        | Description      |
| ---------------- | ---------------- |
| [onclick](https://www.w3schools.com/tags/ev_onclick.asp) | Fires on a mouse click on the element |
| [ondblclick](https://www.w3schools.com/tags/ev_ondblclick.asp) | Fires on a mouse double-click on the element |
| [onmousedown](https://www.w3schools.com/tags/ev_onmousedown.asp) | Fires when a mouse button is pressed down on an element |
| [onmousemove](https://www.w3schools.com/tags/ev_onmousemove.asp) | Fires when the mouse pointer is moving while it is over an element |
| [onmouseout](https://www.w3schools.com/tags/ev_onmouseout.asp) | Fires when the mouse pointer moves out of an element |
| [onmouseover](https://www.w3schools.com/tags/ev_onmouseover.asp) | Fires when the mouse pointer moves over an element |
| [onmouseup](https://www.w3schools.com/tags/ev_onmouseup.asp) | Fires when a mouse button is released over an element |
| `onmousewheel` | Deprecated. Use the `onwheel` attribute instead |
| [onwheel](https://www.w3schools.com/tags/ev_onwheel.asp) | Fires when the mouse wheel rolls up or down over an element |

### Drag Events
| Attribute        | Description      |
| ---------------- | ---------------- |
| [ondrag](https://www.w3schools.com/tags/ev_ondrag.asp) | Script to be run when an element is dragged |
| [ondragend](https://www.w3schools.com/tags/ev_ondragend.asp | Script to be run at the end of a drag operation |
| [ondragenter](https://www.w3schools.com/tags/ev_ondragenter.asp) | Script to be run when an element has been dragged to a valid drop target |
| [ondragleave](https://www.w3schools.com/tags/ev_ondragleave.asp) | Script to be run when an element leaves a valid drop target |
| [ondragover](https://www.w3schools.com/tags/ev_ondragover.asp) | Script to be run when an element is being dragged over a valid drop target |
| [ondragstart](https://www.w3schools.com/tags/ev_ondragstart.asp) | Script to be run at the start of a drag operation |
| [ondrop](https://www.w3schools.com/tags/ev_ondrop.asp) | Script to be run when dragged element is being dropped |
| [onscroll](https://www.w3schools.com/tags/ev_onscroll.asp) | Script to be run when an element's scrollbar is being scrolled |

### Clipboard Events
| Attribute        | Description      |
| ---------------- | ---------------- |
| [oncopy](https://www.w3schools.com/tags/ev_oncopy.asp) | Fires when the user copies the content of an element |
| [oncut](https://www.w3schools.com/tags/ev_oncut.asp) | Fires when the user cuts the content of an element |
| [onpaste](https://www.w3schools.com/tags/ev_onpaste.asp) | Fires when the user pastes some content in an element |

### Media Events
Events triggered by medias like videos, images and audio (applies to all HTML elements, but is most common in media elements, like `<audio>`, `<embed>`, `<img>`, `<object>`, and `<video>`).

[HTML Audio and Video DOM Reference](https://www.w3schools.com/tags/ref_av_dom.asp)

| Attribute        | Description      |
| ---------------- | ---------------- |
| `onabort` | Script to be run on abort |
| `oncanplay` | Script to be run when a file is ready to start playing (when it has buffered enough to begin) |
| `oncanplaythrough` | 	Script to be run when a file can be played all the way to the end without pausing for buffering |
| `oncuechange` | Script to be run when the cue changes in a `<track>` element |
| `ondurationchange` | Script to be run when the length of the media changes |
| `onemptied` | Script to be run when something bad happens and the file is suddenly unavailable (like unexpectedly disconnects) |
| `onended` | Script to be run when the media has reach the end (a useful event for messages like "thanks for listening") |
| `onerror` | Script to be run when an error occurs when the file is being loaded |
| `onloadeddata` | Script to be run when media data is loaded |
| `onloadedmetadata` | Script to be run when meta data (like dimensions and duration) are loaded |
| `onloadstart` | Script to be run just as the file begins to load before anything is actually loaded |
| `onpause` | Script to be run when the media is paused either by the user or programmatically |
| `onplay` | Script to be run when the media is ready to start playing |
| `onplaying` | Script to be run when the media actually has started playing |
| `onprogress` | Script to be run when the browser is in the process of getting the media data |
| `onratechange` | Script to be run each time the playback rate changes (like when a user switches to a slow motion or fast forward mode) |
| `onseeked` | Script to be run when the seeking attribute is set to false indicating that seeking has ended |
| `onseeking` | Script to be run when the seeking attribute is set to true indicating that seeking is active |
| `onstalled` | Script to be run when the browser is unable to fetch the media data for whatever reason |
| `onsuspend` | Script to be run when fetching the media data is stopped before it is completely loaded for whatever reason |
| `ontimeupdate` | Script to be run when the playing position has changed (like when the user fast forwards to a different point in the media) |
| `onvolumechange` | Script to be run each time the volume is changed which (includes setting the volume to "mute") |
| `onwaiting` | 	Script to be run when the media has paused but is expected to resume (like when the media pauses to buffer more data) |

### Misc Events
| Attribute        | Description      |
| ---------------- | ---------------- |
| [ontoggle](https://www.w3schools.com/tags/ev_ontoggle.asp) | Fires when the user opens or closes the `<details>` element |

## HTML Sources
* [W3 Porfolio Template Reactive Webpage](https://www.w3schools.com/w3css/tryw3css_templates_dark_portfolio.htm)
* [JavaScript tutorial](https://www.w3schools.com/js/default.asp)
















