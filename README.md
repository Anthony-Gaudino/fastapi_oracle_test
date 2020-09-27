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

If necessary, use the SQL in the `db.sql` file to create the database tables.

**Note:** The SQL in this file was generated automatically and was not tested,
changes may be necessary for it to generate the tables correctly!

Populate the database with data.

**Example data:**

### Badge
|BADGE_NUMBER|BADGE_STATUS|BADGE_EXPIRY_DATE  |
| ---------- | ---------- | ----------------- |
|1           | Active     |2021-01-01 12:00:00|

### Department
|DEPARTMENT_CODE|DEPARTMENT_NAME|
| ------------- | ------------- |
|1              |HR             |

### Employee
|ID|FIRSTNAME|LASTNAME|BADGE_NUMBER|COUNTRY_CODE|JOB_TITLE_CODE|START_DATE         |LEAVE_DATE         |
|--| ------- | ------ |----------- |----------- |------------- |------------------ |------------------ |
|1 |John     |Doe     |1           |us          |11            |2018-01-01 12:00:00|2021-01-01 12:00:00|

### Job title
|JOB_TITLE_CODE|JOB_TITLE_NAME  |DEPARTMENT_CODE|
| ------------ | -------------- | ------------- |
|1	           |Software Support|1              |

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

Then run the `unicorn` server:
```console
(fastapi_oracle_test-Xvyp61cG) foo@bar:~$ uvicorn app.main:app
```

Visit http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc to see the API
documentation, from the first URL you can execute API calls.

Use the username `user` and password `pass` to authenticate.
