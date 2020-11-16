from flask import Flask, render_template, redirect, url_for,request
import requests
#py script. add in your codes here. default page is index so when you run on 127.0.0.1:5000, do include the route at the back.
#For example, on browser, 127.0.0.1:5000/index
app = Flask(__name__)
@app.route("/index", methods = ['GET'])
def index():
    return render_template("index.html")