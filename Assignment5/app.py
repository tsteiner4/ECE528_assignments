from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
