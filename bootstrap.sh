#!/bin/sh
set FLASK_APP=./app/index.py
$env FLASK_APP=./app/index.py
flask run -h 0.0.0.0
