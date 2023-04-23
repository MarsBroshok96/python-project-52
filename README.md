# Task Manager
___

### Tests and linter status:
[![Actions Status](https://github.com/MarsBroshok96/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/MarsBroshok96/python-project-52/actions) ![example workflow](https://github.com/MarsBroshok96/python-project-52/actions/workflows/linter-and-tests.yml/badge.svg)
<a href="https://codeclimate.com/github/MarsBroshok96/python-project-52/maintainability"><img src="https://api.codeclimate.com/v1/badges/f9f018937c479cbac256/maintainability" /></a> <a href="https://codeclimate.com/github/MarsBroshok96/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/f9f018937c479cbac256/test_coverage" /></a>


For checking last build follow [this link](https://mars-task-manager.up.railway.app/).

### Dependencies
List of dependencies, without which the project code will not work correctly:
- python = "^3.10"
- django = "4.1.7"
- python-dotenv = "^1.0.0"
- dj-database-url = "^0.5.0"
- gunicorn = "^20.1.0"
- django-bootstrap4 = "^22.3"
- django-extensions = "^3.2.1"
- whitenoise = "^6.4.0"
- psycopg2-binary = "^2.9.5"
- factory-boy = "^3.2.1"
- django-filter = "^23.1"
- rollbar = "^0.16.3"

## Description
**Task Manager** is a task management system. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.

### Summary
* [Description](#description)
* [Installation](#installation)
* [Usage](#usage)
* [Development](#development)
  * [Dev Dependencies](#dev-dependencies)
  * [Root structure](#root-structure)

___

## Installation

To install, you must first install the following software:
| Tool | Description |
|----------|---------|
| [Python](https://www.python.org/downloads/) |  Programming language |
| [Poetry](https://python-poetry.org/) |  Python dependency manager |

```Bash
# clone via HTTPS:
$ git clone https://github.com/MarsBroshok96/python-project-52.git
# or clone via SSH:
$ git clone git@github.com:MarsBroshok96/python-project-52.git
$ cd python-project-52
$ make install
$ touch .env
You have to write into .env file SECRET_KEY for Django app and token for Rollbar.
$ make migrations
$ make migrate
$ make static
$ make dev
```


___

## Usage
There are structure of the app with details.
| Steps        | Description                                                                                                                                                               |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Registration | First, fill in all the required registation fileds to get access to all functions of the application.                                                                                            |
| Log in       | Then you have to log in using the information you've filled in the registration form.                                                                                     |
| User         | You can see all users on the relevant page. You can modify data only about yourself. If the user is an author of the task he cannot be deleted. |
| Statuses     | You can add, update, delete statuses of the tasks, if you are logged in. The statuses which correspond with any tasks cannot be deleted.                                  |
| Labels       | You can add, update, delete labels of the tasks, if you are logged in. The label which correspond with any tasks cannot be deleted.                                       |
| Tasks        | You can add, update, delete tasks, if you are logged in. You can also filter tasks on the relevant page with given statuses, executors and labels.                        |


___

## Development

### Dev Dependencies

List of dev-dependencies:
- flake8 = "^6.0.0"
- coverage = "^7.2.1"

### Project Organization

```bash
>> tree .
```
```bash

.
├── Makefile
├── Procfile
├── README.md
├── coverage.xml
├── db.sqlite3
├── exp.txt
├── locale
│   └── ru
│       └── LC_MESSAGES
│           ├── django.mo
│           └── django.po
├── manage.py
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── runtime.txt
├── setup.cfg
├── staticfiles
└── task_manager
    ├── __init__.py
    ├── __pycache__
    ├── asgi.py
    ├── general_models.py
    ├── labels
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── templates
    │   │   └── labels
    │   │       ├── form_label.html
    │   │       ├── label_confirm_delete.html
    │   │       └── label_list.html
    │   ├── urls.py
    │   └── views.py
    ├── mixins.py
    ├── settings.py
    ├── statuses
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations
    │   ├── models.py
    │   ├── templates
    │   │   └── statuses
    │   │       ├── delete_status.html
    │   │       ├── form_status.html
    │   │       └── status_list.html
    │   ├── urls.py
    │   └── views.py
    ├── tasks
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── filter.py
    │   ├── migrations
    │   ├── models.py
    │   ├── templates
    │   │   └── tasks
    │   │       ├── task_confirm_delete.html
    │   │       ├── task_detail.html
    │   │       ├── task_form.html
    │   │       └── task_list.html
    │   ├── urls.py
    │   └── views.py
    ├── templates
    │   ├── base.html
    │   ├── index.html
    │   └── registration
    │       └── login.html
    ├── tests
    │   ├── __pycache__
    │   ├── factories.py
    │   ├── test_labels.py
    │   ├── test_statuses.py
    │   ├── test_tasks.py
    │   └── test_users.py
    ├── urls.py
    ├── users
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── migrations
    │   ├── models.py
    │   ├── templates
    │   │   └── users
    │   │       ├── delete.html
    │   │       ├── register.html
    │   │       ├── update.html
    │   │       └── user_list.html
    │   ├── urls.py
    │   └── views.py
    ├── views.py
    └── wsgi.py
```
