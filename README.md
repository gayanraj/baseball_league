# Baseball League | API

This project contains REST API for Baseball League system.

## Getting Started

* Checkout project from GitHub

```shell
https://github.com/gayanraj/baseball_league.git
```

### Prerequisites

Setting up local development environment.

* Install Python 3.9.5

### Setup

* Create a virtual environment for the project
* Install required packages
    ```
    pip install -r requirements.txt
    ```
* Add SQLite database with name 'db.sqlite3' to the project
* Create database models
    ```
    python manage.py migrate
    ```

* add dummy data
    ```
    python manage.py createdata
    ```

### Test Project

* Execute API unit tests
    ```
    python manage.py test
    ```

### Run Project

* Run the Baseball League API project
    ```
    python manage.py runserver
    ```