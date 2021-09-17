# Baseball League | API

This project contains REST API for Baseball League system.

## Getting Started

```shell
git clone git url
```

### Prerequisites

Setting up local development environment.

* Install Python 3.9.5

### Setup

* Install required packages
    ```
    pip install -Ur requirements.txt
    ```
* Create database models
    ```
    python manage.py makemigrations
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