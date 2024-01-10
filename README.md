# Summer Camp Registration
An open source project summer camp administartion. The main purpose is to have a web solution with form to register new children for summer camp. The project is written in Python 3 and Django. At this moment the project is still in development.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

The project uses Python 3.11. After cloning the repository, create a virtual environment and install the requirements:

```bash
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

or if you are using windows:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

After succesfull instalaion of the requirements, you should make migrations and migrate:

```bash
python manage.py makemigrations
python manage.py migrate
```
Then you can run the server:

```bash
python manage.py runserver
```



## TODO LIST app
- automatic generation of the QR payment code
- automatic generation pdf from registration form
- sending notification to the useremail after successful registration
- better UI for customers
- switch to between CZ and EN language and others
- payment API integration
- admin form fields customisation 

## TODO LIST project & development
- testing environments
- automatic deployment
- unit tests for the app
- better description of the project
- documentation
