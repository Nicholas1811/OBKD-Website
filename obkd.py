from flask import Flask, render_template, redirect, url_for,request
from datetime import date, timedelta, datetime
from datetime import datetime
import requests
import json

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
    tickerCodes = [{"Name" : "Facebook, Inc", "Symbol" : "FB", 'image':"https://visme.co/blog/wp-content/uploads/2015/07/Facebook.png"},
    {"Name" : "Microsoft Corporations", "Symbol": "MSFT", 'image' : 
    "data:image/png;base64,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"},
    {"Name" : "Twitter", "Symbol" : "TWTR", "image": "https://yaspaces.files.wordpress.com/2014/01/twitter-logo.png"}]
    return render_template("usequity.html",usequitylist = tickerCodes)
@app.route("/usequityinfo", methods = ['GET', 'POST'])
def usequityinfo():
    stockticker = request.form['stockticker']
    url = "https://www.alphavantage.co/query?apikey=IXYARDFBT1Y30V7J&function=OVERVIEW&symbol=" + stockticker
    pricingurl = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+stockticker+"&interval=5min&apikey=IXYARDFBT1Y30V7J"
    fxurl = "https://api.exchangeratesapi.io/latest?base=USD"
    payload = {}
    headers= {}
    pricepayload = {}
    priceheaders= {}
    fxpayload={}
    fxheaders = {}
    response = requests.request("GET", url, headers=headers, data = payload)
    pricingdata = requests.request("GET", pricingurl, headers=priceheaders, data = pricepayload)
    fxresponse = requests.request("GET", fxurl, headers=fxheaders, data=fxpayload)
    eqdata = json.loads(response.text)
    pricesdic = json.loads(pricingdata.text)
    fxrate = json.loads(fxresponse.text)    
    lastrefreshed = pricesdic["Meta Data"]["3. Last Refreshed"]
    pastprices = pricesdic["Time Series (5min)"][lastrefreshed]
    sgd = fxrate['rates']["SGD"]
    sgdrate = sgd
    currentprice = pastprices["4. close"]
    currentpriceint = float(currentprice)
    totalvalue = sgdrate*currentpriceint
    return render_template ('usequityinfo.html', pricesdic = pricesdic, pastprices = pastprices, eqdata = eqdata, sgd = sgd, totalvalue = totalvalue)
@app.route("/useqfinancialstatement", methods = ['GET', 'POST'])
def financialstatement():
    stockticker = request.form['stockticker']
    return render_template("useqfs.html", stockticker = stockticker)
