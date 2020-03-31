# Deducate

## Installation

1. Install postgres database and Python interface
```sudo apt install postgresql postgresql-server-dev-9.6 postgis python-psycopg2```
1. Create a role "app" in postgress
1. Create a new database called "careercoach" and make app the owner
1. Set the password of your "postgres" user to "postgres" (or change it in the config file)
1. Add the following to ```/etc/postgresql/10/main/pg_hba.conf```:
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# app
local   dbtutor         app                                     trust
```
! Be sure to add this above local all all peer !

1. Restart the postgres server using ```sudo systemctl restart postgresql```
1. Download dependencies
```
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
```
1. Set the schema for the database
```
flask db init; flask db migrate; flask db upgrade
```
1. Start the server
```
flask run
```

## Pycharm configuration
Edit configurations > "+" > "Flask Server" > Leave everything as the default, except the "Python interpreter", this must go to [PlaceHoleder Location]/venv/bin/python

