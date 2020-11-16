from flask import Flask, render_template, redirect, url_for,request
import requests

app = Flask(__name__)
@app.route("/index", methods = ['GET'])
def index():
    return render_template("index.html")