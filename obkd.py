from flask import Flask, render_template, redirect, url_for,request
import requests
#py script. add in your codes here.
app = Flask(__name__)
@app.route("/index", methods = ['GET'])
def index():
    return render_template("index.html")