# Web API #

This repository provides Web API for DoanTongHop CNPM

## Prerequisites

Install following dependencies beforehand. Check out [.env](.env) and make sure you have all the infos

### Python env

1. Create virtual environments `venv`: Currently, we are using Python 3.9

```bash
python3 -m venv venv
```

2. Activate venv

```bash
.\venv\Scripts\activate
```

3. Install library

```bash
pip install -r requirements.txt
```

### PostgreSQL DB

https://www.postgresql.org/


## Environments

We have the following environment and their abbreviation

* `.env`: environment

In this file, when we mention `<env>`, we're talking about the above environment

## Source structure & overview

This section will explain and overview in high level of source code structure and point out some important files/folders

* *.env*: environment
* *requirements.txt*: List of library and software used
* *run.py* For running flask app, have these parameters:
    * *api*: web API router
    * *config*: config flask app
    * *db*: query processing (SELECT, INSERT, UPDATE, ...) of DB
    * *entity*: model of DB
    * *pkg*: common process for logic
    * *usecase*: business logic processing

## Commands

For all of these commands, if you want to run on local environment, then just omit `--env <end>`

### Running Flask app

```bash
python run.py
```

To serve the Flask app

### Migrate DB

```bash
python run.py migrate
```

To create migrate files, which will be inside `/migrations/versions`

### Upgrade DB

```bash
python run.py 'migrate up'
```

To apply upgrade to DB with the current latest version

## Migrate

Checkout [migrate detail and usage](migrations/README.md)

## Libraries

We use:

* [Flask](https://flask.palletsprojects.com/en/2.2.x/): for web framework
* [PostgreSQL](https://www.postgresql.org/): for DB
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) (base
  on [SQLAlchemy](https://www.sqlalchemy.org/)): for DB access and ORM
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/): for migrations
* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/): for CORS
* [Python-dotenv](https://pypi.org/project/python-dotenv/): for read `<env>` files
