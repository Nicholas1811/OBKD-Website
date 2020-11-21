from flask import Flask, render_template, redirect, url_for,request
from datetime import date, timedelta, datetime
from datetime import datetime
import requests
import json
import numpy as np
import pandas as pd

#py script. add in your codes here. default page is index so when you run on 127.0.0.1:5000, do include the route at the back.
#For example, on browser, 127.0.0.1:5000/
app = Flask(__name__)
#Main route
@app.route("/index", methods = ['GET'])
def index():
    return render_template("index.html")
#About us route
@app.route("/aboutUs", methods = ['GET','POST'])
def aboutUs():
    return render_template("about.html")
@app.route("/profile", methods = ['GET','POST'])
def profile():
    return render_template("profile.html")
#Nicholas's US Equity Main Page which shows different equities.
@app.route("/USEquities", methods = ['GET', 'POST'])
def USEquities():
    tickerCodes = ["FB", "GOOG", "TWTR"]
    usequitylist = []
    for i in tickerCodes:
        url = "https://www.alphavantage.co/query?apikey=IXYARDFBT1Y30V7J&function=OVERVIEW&symbol=" + i
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        eqdata = json.loads(response.text)
        if i == "FB":
            eqdata["image"] = "https://visme.co/blog/wp-content/uploads/2015/07/Facebook.png"
        elif i == "GOOG":
            eqdata["image"] = "https://dvh1deh6tagwk.cloudfront.net/finder-us/wp-uploads/2020/03/AlphabetLogo_Supplied_450x250.png"
        else:
            eqdata["image"] = "https://yaspaces.files.wordpress.com/2014/01/twitter-logo.png"
        usequitylist.append(eqdata.copy())
    print(usequitylist)
    return render_template("usequity.html",usequitylist = usequitylist)
@app.route("/usequityinfo", methods = ['GET', 'POST'])
def usequityinfo():
    date = datetime.now() - timedelta(1)
    prevdate = date.strftime('%Y-%m-%d')
    stockticker = request.form['stockticker']
    url = "https://www.alphavantage.co/query?apikey=IXYARDFBT1Y30V7J&function=OVERVIEW&symbol=" + stockticker
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    eqdata = json.loads(response.text)
    pricingurl = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+stockticker+"&interval=5min&apikey=IXYARDFBT1Y30V7J"
    pricepayload = {}
    priceheaders= {}
    pricingdata = requests.request("GET", pricingurl, headers=priceheaders, data = pricepayload)
    pricesdic = json.loads(pricingdata.text)
    print(pricesdic)
    pastprices = pricesdic["Time Series (5min)"]["2020-11-20 20:00:00"]
    print(stockticker)
    print(eqdata)
    return render_template ('usequityinfo.html', pricesdic = pricesdic, pastprices = pastprices, eqdata = eqdata)
