# swe1-app

main: [![Build Status](https://app.travis-ci.com/AleenaBoscoK/swe1-app.svg?branch=main)](https://app.travis-ci.com/AleenaBoscoK/swe1-app) [![Coverage Status](https://coveralls.io/repos/github/AleenaBoscoK/swe1-app/badge.svg)](https://coveralls.io/github/AleenaBoscoK/swe1-app)

A Django polls app built from Parts 1–4 of the official Django tutorial, deployed on AWS Elastic Beanstalk.

**Live app:** http://swe1-env.eba-zci4prtk.us-east-2.elasticbeanstalk.com/polls/

## Continuous integration

Every push and pull request runs on Travis CI:

- Formatting check with `black --check`
- Linting with `flake8` (max line length 88, to match black)
- Test suite run under `coverage.py`, with results reported to Coveralls
- Automatic deploy to Elastic Beanstalk when a build on `main` passes

## Run locally

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/polls/
