from flask import Flask, Blueprint, redirect, url_for

test = Blueprint('test', __name__)


@test.route("/")
def home():
    return "Hello world"


@test.route("/test", methods=['GET', 'POST'])
def testy():
    return {"name": "This is test"}
