## Virtual Machine Control REST Server

# Functionalities
This is a project created with Django Framework in Pycharm IDE.

A django server on a special LabNet pc, which accepts commands both ways:
1. By using the React frontend;
2. By using the provided endpoints (check put the urls.py files).

It has the following functionalities:
1. Providing a Login functionality;
2. Accepting command to control virtual machines installed on the same pc, where
this server is hosted;
3. Accepting uploaded python scripts, which can be then executed on the same
pc, where this server is hosted;


# Environment variables
In terminal: pip install python-decouple
In settings.py: from decouple import config, Csv
Add the needed variables
Create a dir 'env' in the main dir and a file inside called '.env'
point the path in Edit Configurations -> Path to ".env" files like this:
`C:/Appl/Projects/Python/1350-FBW_lab_pc_rest_api_server_backend/envs/.env`
and add the needed variables


# Running the project
1. Create a VENV and install the dependencies from the requirements.txt file;
2. Examine the contents in setting.py and adjust as see fit to your settings;
3. Run the server with `python manage.py runserver or by Pycharm IDE;
4. The server is hosted on http://localhost:8000/.


# Structure
1. The project is divided into several apps, which provide unique functionalities: login, control
of virtual machines and execution of python scripts, respectively;
2. The controllers folder must provide the logic for the factual control of the 
virtual machines using `virtualbox` and the execution of python scripts using `python3`;
3. The core folder contains the decorators for control of method execution: timing, logging, etc.. Also
the main engine class which connects the controllers with the views. The views are made abstract,
combining the common logic into the view_templates.py file;
4. The media_files folder contains the uploaded python scripts;
5. Then each one of the apps is structured as per the Django principles: models, views, urls, etc.;


# ToDo:
1. Currently, the server only provides responses to the requests, and
the factual connection to virtual machines and the running of python scripts
needs to be added to the same methods which provide the responses.
2. Afterward we need to test if running 2 different virtual machines at
the same time by the server is possible and feasible.
