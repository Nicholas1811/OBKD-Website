from flask import Flask, render_template, redirect, url_for,request
from datetime import date, timedelta, datetime
from datetime import datetime
import requests
import json

#py script. add in your codes here. default page is index so when you run on 127.0.0.1:5000, do include the route at the back.
#For example, on browser, 127.0.0.1:5000/
app = Flask(__name__)
#Main 
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
    tickerCodes = [{"Name" : "Facebook, Inc", "Symbol" : "FB", 'image':"https://img.freepik.com/free-photo/3d-facebook-logo-minimalist-with-blank-space_85867-246.jpg?size=626&ext=jpg&ga=GA1.2.2098196052.1601510400",
    "Industry" : "Internet Content & Information"},
    {"Name" : "Microsoft Corporations", "Symbol": "MSFT", 'image' : 
    "https://cdn.vox-cdn.com/thumbor/NeSo4JAqv-fFJCIhb5K5eBqvXG4=/7x0:633x417/1200x800/filters:focal(7x0:633x417)/cdn.vox-cdn.com/assets/1311169/mslogo.jpg",
    "Industry" : "Software Infrastructure"},
    {"Name" : "Visa", "Symbol" : "V", "image": "https://pbs.twimg.com/media/EnrGEFNVgAEim2T?format=jpg&name=small", "Industry" : "Credit Services"},
    {"Name": "Intel", "Symbol" : "INTC", "image": "https://pbs.twimg.com/media/EnrGdrDUUAAw1i3?format=jpg&name=small", "Industry" : "Semiconductors" },
    {'Name': "Oracle Corporation","Symbol" : "ORCL" , "image": "https://pbs.twimg.com/media/EnrGrIZVQAIVEY2?format=jpg&name=small" , "Industry" : "Software Infrastructure"}]
    return render_template("usequity.html",usequitylist = tickerCodes)
#Shows the equity info plus, routing for the pages, something similar to a SPA
@app.route("/usequityinfo", methods = ['GET', 'POST'])
def usequityinfo():
    stockticker = request.form['stockticker']
    industrytype = request.form['industry']
    url = "https://www.alphavantage.co/query?apikey=IXYARDFBT1Y30V7J&function=OVERVIEW&symbol=" + stockticker
    pricingurl = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+stockticker+"&interval=5min&apikey=IXYARDFBT1Y30V7J"
    fxurl = "https://api.exchangeratesapi.io/latest?base=USD"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    pricingdata = requests.request("GET", pricingurl, headers=headers, data = payload)
    fxresponse = requests.request("GET", fxurl, headers=headers, data=payload)
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
    return render_template ('usequityinfo.html', pricesdic = pricesdic, pastprices = pastprices, eqdata = eqdata, sgd = sgd, totalvalue = totalvalue, industry = industrytype)
#Shows the fundementals of the stock like balance sheet and income statement.
@app.route("/fundementals", methods = ['GET', 'POST'])
def financialstatement():
    fun = request.form['stockticker']
    indus = request.form['industry']
    equityname = request.form['equityname']
    url = "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol="+fun+"&apikey=IXYARDFBT1Y30V7J"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    incomestatement = json.loads(response.text)
    incomestatementdic = incomestatement['annualReports']
    pastyearincomestatement = incomestatement['annualReports'][1]
    pastyearincomestatement.pop("")
    return render_template("usfundementals.html", incomestatement = incomestatementdic,
     tickercode = fun, industry = indus, equityname = equityname)
