# README

> This is a project to support AP Computer Science Principles (CSP) as well as a UC articulated Data Structures course. It was crafted iteratively starting in 2020 to the present time.  The primary purposes are ...

- Used as starter code for student projects for `AP CSP 1 and 2` and `Data Structures 1` curriculum.
- Used to teach key principles in learning the Python Flask programming environment.
- Used as a backend server to service API's in a frontend-to-backend pipeline. Review the `api` folder in the project for endpoints.
- Contains a minimal frontend, mostly to support Administrative functionality using the `templates` folder and `Jinja2` to define UIs.
- Contains SQL database code in the `model` folder to introduce concepts of persistent data and storage.  Perisistence folder is `instance/volumes` for generated SQLite3 db.
- Contains capabilities for deployment and has been used with AWS, Ubuntu, Docker, docker-compose, and Nginx to `deploy a WSGI server`.
- Contains APIs to support `user authentication and cookies`, a great deal of which was contributed by Aiden Wu a former student in CSP.  

## Flask Portfolio Starter

Use this project to create a Flask Server.

- GitHub link: [flask_2025](https://github.com/nighthawkcoders/flask_2025)
- The runtime link is published under the About on the GitHub link.
- `Create a template from this repository` if you plan on making GitHub changes.

## The conventional way to get started

> Quick steps that can be used with MacOS, WSL Ubuntu, or Ubuntu; this uses Python 3.9 or later as a prerequisite.

- Open a Terminal, clone a project and `cd` into the project directory.  Use a `different link` and name for `name` for clone to match your repo.

```bash
mkdir -p ~/nighthawk; cd ~/nighthawk

git clone https://github.com/nighthawkcoders/flask_2025.git

cd flask_2025
```

- Install python dependencies for Flask, etc.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Open project in VSCode

- Prepare VSCode and run
  - From Terminal run VSCode

  ```bash
  code .
  ```

  - Open Setting: Ctrl-Shift P or Cmd-Shift
    - Search Python: Select Interpreter.
    - Match interpreter to `which python` from terminal.
    - Shourd be ./venv/bin/python

  - From Extensions Marketplace install `SQLite3 Editor`
    - Open and view SQL database file `instance/volumes/user_management.db`

  - Make a local `.env` file in root of project to contain your secret passwords

  ```shell
  # User Defaults
  ADMIN_USER='toby'
  ADMIN_PASSWORD='123Toby!'
  DEFAULT_USER='hop'
  DEFAULT_PASSWORD='123Hop!'
  ```

  - Make the database and init data.
  
  ```bash
  ./scripts/db_init.py
  ```

  - Explore newly created SQL database
    - Navigate too instance/volumes
    - View/open `user_management.db`
    - Loook at `Users` table in viewer

  - Run the Project
    - Select/open `main.py` in VSCode
    - Start with Play button
      - Play button sub option contains Debug
    - Click on loop back address in terminal to launch
      - Output window will contain page to launch http://127.0.0.1:8087
    - Login using your secrets

## Idea

### Visual thoughts

> The Starter code should be fun and practical.

- Organize with Bootstrap menu
- Add some color and fun through VANTA Visuals (birds, halo, solar, net)
- Show some practical and fun links (HREFs) like Twitter, Git, Youtube
- Build a Sample Page (Table)
- Show the project-specific links (HREFs) per page

### Files and Directories in this Project

The key files and directories in this project are in this online article.

[Flask Anatomy](https://nighthawkcoders.github.io/portfolio_2025/flask-anatomy)

Or read this entire series of articles starting with the Intro, Anatomy, and more ...

[Flask Intro](https://nighthawkcoders.github.io/portfolio_2025/flask-intro)

### Implementation Summary

#### July 2024

> Updates for 2024 too 2025 school year.  Primary addition is a fully functional backend for JWT login system.

- Full support for JWT cookies
- The API's for CRUD methods
- The model definition User Class and related tables
- SQLite and RDS support
- Minimal Server side UI in Jinja2

#### July 2023

> Updates for 2023 to 2024 school year.

- Update README with File Descriptions (anatomy)
- Add JWT and add security features using a SQLite user database
- Add migrate.sh to support sqlite schema and data upgrade

#### January 2023

> This project focuses on being a Python backend server.  Intentions are to only have simple UIs an perhaps some Administrative UIs.

#### September 2021

> Basic UI elements were implemented showing server side Flask with Jinja 2 capabilities.

- The Project entry point is main.py, this enables the Flask Web App and provides the capability to render templates (HTML files)
- The main.py is the  Web Server Gateway Interface, essentially it contains an HTTP route and HTML file relationship.  The Python code constructs WSGI relationships for index, kangaroos, walruses, and hawkers.
- The project structure contains many directories and files.  The template directory (containing HTML files) and static directory (containing JS files) are common standards for HTML coding.  Static files can be pictures and videos, in this project they are mostly javascript backgrounds.
- WSGI templates: index.html, kangaroos.html, ... are aligned with routes in main.py.
- Other templates support WSGI templates.  The base.html template contains common Head, Style, Body, and Script definitions.  WSGI templates often "include" or "extend" these templates.  This is a way to reuse code.
- The VANTA javascript statics (backgrounds) are shown and defaulted in base.html (birds) but are block-replaced as needed in other templates (solar, net, ...)
- The Bootstrap Navbar code is in navbar.html. The base.html code includes navbar.html.  The WSGI html files extend base.html files.  This is a process of management and correlation to optimize code management.  For instance, if the menu changes discovery of navbar.html is easy, one change reflects on all WSGI html files.
- Jinja2 variables usage is to isolate data and allow redefinitions of attributes in templates.  Observe "{% set variable = %}" syntax for definition and "{{ variable }}" for reference.
- The base.html uses a combination of Bootstrap grid styling and custom CSS styling.  Grid styling in observation with the "<Col-3>" markers.  A Bootstrap Grid has a width of 12, thus four "Col-3" markers could fit on a Grid row.
- A key purpose of this project is to embed links to other content.  The "href=" definition embeds hyperlinks into the rendered HTML.  The base.html file shows usage of "href={{github}}", the "{{github}}" is a Jinja2 variable.  Jinja2 variables are pre-processed by Python, a variable swap with value, before being sent to the browser.
