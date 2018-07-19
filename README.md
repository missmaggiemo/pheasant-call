# Bain Coding Challenge 2018-07-18
Applicant: Maggie Moreno

## Overview

* Python 3 Flask app, see http://flask.pocoo.org/ if you're not familiar

* Data in SQLite (for now, maybe I'll move it to something else later)

* Uses python virtualenv, see https://virtualenv.pypa.io/en/stable/ if you're not familiar

* One endpoint, /providers, that responds to a GET, parses query params, and spits back data

  - Empty query params spits back the first 10 results, maybe?

## How to use

### Run the app locally, in the background
```
make run
```

### Load the data into the SQLite DB, if it isn't already there
```
make load_data
```

### Why Flask?
Flask is a light-weight Python web server middleware framework. I've done most of my development in Python lately, so that's what I want to use now. Since the assignment asks for a read-only API for what is effectively just one table of data, I don't need a CRUD-oriented framework like Django.


## TODO

- [x] How to use
- [x] Flask app
- [x] Load data into SQLite
- [x] API endpoint to return data (JSON)
- [x] Parse query params
- [x] README
- [ ] Launch on my AWS instance
- [ ] Tests
