#!/usr/bin/env python
import random
from flask import Flask

app = Flask(__name__)
with open("fortunes.dat", "r") as fh:
    fortunes = fh.readlines()

@app.route("/")
def return_fortune():
    return random.choice(fortunes)

@app.route("/boom")
def boom():
    return 1/0

if __name__ == "__main__":
    app.run(host="0.0.0.0")
