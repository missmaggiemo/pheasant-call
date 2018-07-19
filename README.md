# Bain Coding Challenge 2018-07-18
Applicant: Maggie Moreno

## Overview

* http://54.146.129.15:5000/providers

* Python 3 Flask app, see http://flask.pocoo.org/ if you're not familiar

* Data in SQLite

   - run `make load_data` to load the database the first time the app is run locally

* Uses python virtualenv, see https://virtualenv.pypa.io/en/stable/ if you're not familiar

* One endpoint, /providers, that responds to a GET, parses query params, and spits back data

  - Empty query params spits back the first 10 results

* Original Prompt https://gist.github.com/rbrowngt/4690f19441adf54872b4cee43ee86cef


## How to use

### Get data from the remote app
```
curl http://54.146.129.15:5000/providers
```

### Run the app locally, in the background
```
make run
```

### Load the data into the SQLite DB, if it isn't already there
```
make load_data
```

### Run the app locally, in the background
```
make test
```

## Technical Desicions Explanation

### Why Flask?

Flask is a light-weight Python web server middleware framework. I've done most of my development in Python lately, so in the interest of time, I'm sticking with that. Since the assignment asks for a read-only API for what is effectively just one table of data, I don't need a CRUD-oriented framework like Django.

### Why SQLite?

SQLite doesn't requite another process running anywhere else, and I've used with with Python projects before as a just-get-going starter DB. It's easy enough to swap in another SQL-like database in its place when it comes time to scale.

### Why did I deploy on AWS instead of something like Heroku?

I'm not that familiar with deploying anything other than a Rails app on Heroku, and I haven't done that since 2014. At my former company, we deployed everything on AWS, and I already had an instance standing. To be honest though, I think this was a poor decision on my part. I ran into a number of issues deploying my little app simply because I wasn't familiar enough with the AWS-Linux way of doing things and expected it to be more like the Ubuntu way of doing things. I learned a lot, for sure, but I think this project would have moved a little more quickly for me had I just committed to learning about using Postgres with Flask. There are plenty of docs for deploying on Heroku with Flask and Postgres-- a little more research would have gone a long way.


## TODO

- [x] How to use
- [x] Flask app
- [x] Load data into SQLite
- [x] API endpoint to return data (JSON)
- [x] Parse query params
- [x] README
- [x] Launch on my AWS instance `http://54.146.129.15:5000/providers`
- [x] Tests
