# Prerequisites
Create a Python virtualenv & install the pip modules in `requirements.txt`.


# Runme 

## Dev
Run `fortune.py` to start a webserver on `localhost:5000`.

## Prod
`<venv>/bin/gunicorn --chdir=/fortune -b 0.0.0.0:80 fortune:app`
