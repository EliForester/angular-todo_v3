# Todo REST API
Project to catalog minerals

## Getting Started

Clone the repository

If using the default todos.sqlite, run migration.py to add the 'completed' field

```
python migration.py
```

Run app.py

### Prerequisites

Created on Python 3

requirements.txt
```
aniso8601==1.1.0
argon2-cffi==16.2.0
atomicwrites==1.2.1
attrs==18.2.0
cffi==1.8.3
click==6.6
coverage==4.2
Flask==0.11.1
Flask-RESTful==0.3.5
itsdangerous==0.24
Jinja2==2.8
limits==1.3
MarkupSafe==0.23
more-itertools==4.3.0
peewee==3.7.0
pluggy==0.7.1
py==1.6.0
pycparser==2.18
python-dateutil==2.5.3
pytz==2016.6.1
six==1.10.0
Werkzeug==0.11.10

```

## Test coverage

```

Name                    Stmts   Miss  Cover
-------------------------------------------
app.py                     11      3    73%
config.py                   5      0   100%
models.py                  25      6    76%
resources/__init__.py       0      0   100%
resources/todos.py         44      3    93%
tests.py                   87      0   100%
-------------------------------------------
TOTAL                     172     12    93%


```

## Running the tests

```
python tests.py
```

Or with coverage

```
coverage run tests.py
coverage report
```

