# Fastapi Oracle Test

This is a Python Fastapi test application that connects with an Oracle database.


## Installation

This application should to be run on a x64 Debian based Linux distribution.

Tested on Ubuntu 20.04.1 x64, should also work on Debian 10.

**Note:** Requires Python >= 3.8

On a Linux terminal cd to the project root directory (same this file is
present).

Run the `install.sh` script as root, this will install all necessary system
dependencies:

```console
foo@bar:~$ ./install.sh
```

Then install Python dependencies executing:
```console
foo@bar:~$ pipenv install
```


## Create database tables

![Database Diagram](diagram.png?raw=true "Database Diagram")

Executing the `db.sql` in Oracle will create the necessary database tables and
populate them with some data.



## Set database connection configuration

On the project root, edit the file `app/database.py`:
```console
foo@bar:~$ vim app/database.py
```

On the section:

```python
connect_url = URL(
    "oracle+cx_oracle",
    username="",
    password="",
    host="",
    port="",
    database=""
)
```

Fill in the host, username, password and database name.


## Executing the test server instance

First switch to the project virtual environment:
```console
foo@bar:~$ pipenv shell
```

Then run the `uvicorn` server:
```console
(fastapi_oracle_test-Xvyp61cG) foo@bar:~$ uvicorn app.main:app
```

Visit http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc to see the API
documentation, from the first URL you can execute API calls.

Use the username `user` and password `pass` to authenticate.
