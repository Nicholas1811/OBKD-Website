from flask import Flask, render_template, redirect, url_for,request,session
from datetime import date, timedelta, datetime
from datetime import datetime
import requests
import json
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

#py script. add in your codes here. default page is index so when you run on 127.0.0.1:5000, do include the route at the back.
#For example, on browser, 127.0.0.1:5000/
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = "4df4a6c7c44c4d49cfa3f8299a06b4c2"
clientid = "1af01ca68824cd82"
clientsecret = "4df4a6c7c44c4d49cfa3f8299a06b4c2"
authorizationbaseurl = 'https://apm.tp.sandbox.fidorfzco.com/oauth/authorize'
tokenurl = 'https://apm.tp.sandbox.fidorfzco.com/oauth/token'
redirecturl = "http://localhost:5000/callback"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)
#Main 
@app.route("/index", methods = ['GET'])
def index():
    return render_template("index.html")
#About us route
@app.route("/aboutUs", methods = ['GET','POST'])
def aboutUs():
    return render_template("about.html")
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
#Shows the equity info plus, routing for the pages, uses 2 alphavantage + 1 outside API
@app.route("/usequityinfo", methods = ['GET', 'POST'])
def usequityinfo():
    try:
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
        marketcap = round(float(eqdata['MarketCapitalization']) , 2)
        trailingPE = round(float(eqdata['TrailingPE']) , 2)
        forwardPE = round(float(eqdata['ForwardPE']) , 2)
        pegRatio = round(float(eqdata['PEGRatio']) , 2)
        pricetosales = round(float(eqdata['PriceToSalesRatioTTM']), 2)
        pricetobook = round(float(eqdata['PriceToBookRatio']), 2)
        profitmargin = round(float(eqdata["ProfitMargin"])* 100, 2)
        operatingmargin = round(float(eqdata['OperatingMarginTTM']) * 100, 2)
        returnonasset = round(float(eqdata['ReturnOnAssetsTTM']) * 100 ,2)
        returnonequity =  round(float(eqdata['ReturnOnEquityTTM']) * 100 ,2)
        quarterlyrevenuegrowth = round(float(eqdata['QuarterlyRevenueGrowthYOY'])*100 ,2)
        quarterlyearningsgrowth = round(float(eqdata['QuarterlyEarningsGrowthYOY'])*100 ,2)
        eneb = round(float(eqdata['EVToEBITDA']),2)
        envrev = round(float(eqdata['EVToRevenue']) ,2)
        revpershare = round(float(eqdata['RevenuePerShareTTM']),2)
        grossprofit = round(float(eqdata['GrossProfitTTM']),2)
        ebitda = round(float(eqdata['EBITDA']),2)
        epsttm = round(float(eqdata['DilutedEPSTTM']),2)
        beta = round(float(eqdata['Beta']),2)
        weekhigh = round(float(eqdata['52WeekHigh']),2)
        weeklow = round(float(eqdata['52WeekLow']),2)
        shortma = round(float(eqdata['50DayMovingAverage']) ,2)
        longma = round(float(eqdata['200DayMovingAverage']) ,2)
        sharesoutstanding = round(float(eqdata['SharesOutstanding']),2)
        sharesfloat = round(float(eqdata['SharesFloat']),2)
        sharesshort = round(float(eqdata['SharesShort']),2)
        shortratio = round(float(eqdata['ShortRatio']),2)
        insider = eqdata['PercentInsiders']
        institutions = eqdata['PercentInstitutions']
        forwardannualdividendrate = round(float(eqdata['ForwardAnnualDividendRate']))
        forwardannualdividendyield = round(float(eqdata['ForwardAnnualDividendYield']))
        payoutratio = round(float(eqdata['PayoutRatio']))
        divdate = eqdata['DividendDate']
        exdivdate = eqdata['ExDividendDate']
        lastsplitfactor = eqdata['LastSplitFactor']
        lastsplitdate = eqdata['LastSplitDate']
        historic = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+stockticker+"&apikey=RU0OE9SIH6R38HXY"
        historicresponse = requests.request("GET", historic, headers=headers, data=payload)
        historicdata = json.loads(historicresponse.text)
        cleanedhistoric = historicdata['Time Series (Daily)']
        print(cleanedhistoric)
        for k, v in cleanedhistoric.items():
            print(k)
            print(v["1. open"])
        incomeurl = "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol="+stockticker+"&apikey=RU0OE9SIH6R38HXY"
        incomeresponse = requests.request("GET", incomeurl, headers=headers, data = payload)
        incomestatement = json.loads(incomeresponse.text)
        incomestatementdic = incomestatement['annualReports']
        for i in range(0,5):
            for k,v in incomestatementdic[i].items():
                if v != "None" and k != "fiscalDateEnding" and v != "0" and k!= "reportedCurrency":
                    v = v[:-3]
                    v = int(v)
                    v = "{:,}".format(v)
                    print(v)
                    incomestatementdic[i][k] = v
                else:
                    pass
        print(incomestatementdic)
        balanceurl = "https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol="+stockticker+"&apikey=RU0OE9SIH6R38HXY"
        balanceresponse = requests.request('GET', balanceurl, headers = headers, data = payload)
        balancesheet = json.loads(balanceresponse.text)
        balancesheetdic = balancesheet['annualReports']
        generalnewsurl = "https://stocknewsapi.com/api/v1/category?section=general&items=50&token=6x0ns49l6v9xchu3rltziknbiogcyaltdljm8oee"
        stocknewsurl = "https://stocknewsapi.com/api/v1?tickers="+stockticker+"&items=50&token=6x0ns49l6v9xchu3rltziknbiogcyaltdljm8oee"
        generalnewsresponse = requests.request("GET", generalnewsurl, headers=headers, data=payload)
        stocknewsresponse = requests.request('GET', stocknewsurl, headers = headers, data = payload)
        generalnewsdic = json.loads(generalnewsresponse.text)
        stocknewdic = json.loads(stocknewsresponse.text)
        cleanednews = generalnewsdic['data']
        stocknews = stocknewdic['data']
        print(cleanednews)
        return render_template ('usequityinfo.html', pricesdic = pricesdic, pastprices = pastprices, eqdata = eqdata, sgd = sgd, 
        totalvalue = totalvalue, industry = industrytype,operatingmargin  = operatingmargin ,profitmargin = profitmargin, returnonasset = returnonasset, returnonequity = returnonequity,
        quarterlyrevenuegrowth = quarterlyrevenuegrowth, quarterlyearningsgrowth = quarterlyearningsgrowth, insider = insider, 
        institutions = institutions, trailingPE = trailingPE, forwardPE = forwardPE, pegRatio = pegRatio, pricetosales = pricetosales,
        pricetobook = pricetobook, enrev = envrev, eneb = eneb, revpershare = revpershare, gp = grossprofit, ebitda = ebitda,
        epsttm = epsttm, beta = beta, weekhigh = weekhigh, weeklow = weeklow, shortma = shortma, longma = longma, sharesoutstanding = sharesoutstanding,
        sharesfloat = sharesfloat, sharesshort = sharesshort, shortratio = shortratio, forwardannualdividendyield = forwardannualdividendyield, 
        forwardannualdividendrate = forwardannualdividendrate, payoutratio = payoutratio, divdate = divdate, exdivdate = exdivdate, 
        lastsplitdate = lastsplitdate, lastsplitfactor = lastsplitfactor, marketcap = marketcap,historicdata = cleanedhistoric, incomestatement = incomestatementdic,
        balancesheetdic = balancesheetdic, generalnewsdic = cleanednews, stocknews = stocknews)
    except KeyError:
        print(eqdata)
        return "MAX API Calling"
   
@app.route('/usbalancesheet', methods = ['GET', 'POST'])
def balancesheet():
    try:
        balancesheet = ['1']
        stockticker = request.form['stockticker']
        equityname = request.form['equityname']
        industry = request.form['industry']
        url = "https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol="+stockticker+"&apikey=RU0OE9SIH6R38HXY"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        balancesheetdata = json.loads(response.text)
        balancesheetreport = balancesheetdata['annualReports']

        print(balancesheetdata)
        for k, v in balancesheetreport.items():
            print(k)
            print(v)
        return render_template('usbalancesheet.html', balancesheet = balancesheet, stockticker = stockticker , equityname = equityname , 
        industry = industry)
    except KeyError:
        return "MAX API CALLING"
@app.route('/default', methods = ['GET', 'POST'])
def default():
    fidor = OAuth2Session(clientid,redirect_uri=redirecturl)
    authorizationurl, state = fidor.authorization_url(authorizationbaseurl)
    print(session)
    print(state)
    session['oauth_state'] = state
    print(state)
    print(session['oauth_state'])
    print ('auth url is' + authorizationurl)
    return redirect(authorizationurl)
@app.route('/callback', methods = ['GET'])
def callback():
    fidor = OAuth2Session(state=session['oauth_state'])
    print(fidor)
    authorizationcode = request.args.get('code')
    #potential bug area
    body = 'grant_type="authorization_code&code='+authorizationcode+ \
    '&redirect_uri=' + redirecturl+'&client_id='+clientid
    auth = HTTPBasicAuth(clientid, clientsecret)
    token = fidor.fetch_token(tokenurl, auth = auth, code = authorizationcode, body = body, method = "POST")
    session['oauth_token'] = token
    return redirect(url_for('.user')) 
@app.route('/user', methods = ['GET'])
def user():
    try:
        token = session['oauth_token']
        url = "https://api.tp.sandbox.fidorfzco.com/accounts"

        payload={}
        headers = {
            'Accept': 'application/vnd.fidor.de;version=1;text/json',
            'Content-Type': 'application/json',
            #this is important
            'Authorization': 'Bearer ' + token['access_token'] ,
            'Cookie': 'session_token=2ffc5b9254252d363be781dc8ccd0570c4d95420; account=IntcImFjY291bnRcIjp7XCJhY2NvdW50X25vXCI6NjY4MzcyNjAsXCJmaXJzdG5hbWVcIjpcIkIgU0VWRU5URUVOXCIsXCJsYXN0bmFtZVwiOlwiU3R1ZGVudFwiLFwidGl0bGVcIjpudWxsLFwiYWRyX3N0cmVldFwiOlwiQ2l0eS1Qb2ludFwiLFwiYWRyX3N0cmVldF9uclwiOlwiOTdiXCIsXCJhZHJfemlwXCI6XCI5MjY4NVwiLFwiYWRyX2NpdHlcIjpcIkZsb8OfXCIsXCJhZHJfY291bnRyeVwiOlwiREVcIixcImFkcl9waG9uZVwiOm51bGwsXCJhZHJfbW9iaWxlXCI6bnVsbCxcImFkcl9mYXhcIjpudWxsLFwiYmlydGhkYXlcIjpcIjE5OTQtMDYtMjJcIixcImZvcmVpZ25fYWNjb3VudF9ub1wiOlwiNTEyOTc2NjA4MFwiLFwiZW1haWxfZW1haWxcIjpcInN0dWRlbnRiMTdAZW1haWwuY29tXCIsXCJpc19jb3Jwb3JhdGVcIjpmYWxzZSxcInBob3RvXCI6bnVsbCxcInByZWZlcnJlZF9sYW5ndWFnZVwiOm51bGx9fSI%3D--a86b840dda679f193fb51c898359f9f5a274e3e8'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        customeraccount = json.loads(response.text)
        customerdetails = customeraccount['data'][0]
        custinfo = customerdetails['customers'][0]
        custbirthday = custinfo['birthday']
        custbirthday = custbirthday[:-15]
        session['fidor_cust'] = customeraccount
        transcurl = "https://api.tp.sandbox.fidorfzco.com/transactions"
        payload={}
        headers = {
            'Authorization': 'Bearer ' + token['access_token'],
            'Accept': 'application/vnd.fidor.de;version=1;text/json',
            'Content-Type': 'application/json',
            'Cookie': 'session_token=27a5a42b826bb91c41025094386f8fff53030584; account=IntcImFjY291bnRcIjp7XCJhY2NvdW50X25vXCI6NjY4MzcyNjAsXCJmaXJzdG5hbWVcIjpcIkIgU0VWRU5URUVOXCIsXCJsYXN0bmFtZVwiOlwiU3R1ZGVudFwiLFwidGl0bGVcIjpudWxsLFwiYWRyX3N0cmVldFwiOlwiQ2l0eS1Qb2ludFwiLFwiYWRyX3N0cmVldF9uclwiOlwiOTdiXCIsXCJhZHJfemlwXCI6XCI5MjY4NVwiLFwiYWRyX2NpdHlcIjpcIkZsb8OfXCIsXCJhZHJfY291bnRyeVwiOlwiREVcIixcImFkcl9waG9uZVwiOm51bGwsXCJhZHJfbW9iaWxlXCI6bnVsbCxcImFkcl9mYXhcIjpudWxsLFwiYmlydGhkYXlcIjpcIjE5OTQtMDYtMjJcIixcImZvcmVpZ25fYWNjb3VudF9ub1wiOlwiNTEyOTc2NjA4MFwiLFwiZW1haWxfZW1haWxcIjpcInN0dWRlbnRiMTdAZW1haWwuY29tXCIsXCJpc19jb3Jwb3JhdGVcIjpmYWxzZSxcInBob3RvXCI6bnVsbCxcInByZWZlcnJlZF9sYW5ndWFnZVwiOm51bGx9fSI%3D--a86b840dda679f193fb51c898359f9f5a274e3e8'
            }
        transcresponse = requests.request("GET", transcurl, headers=headers, data=payload)
        transcdic = json.loads(transcresponse.text)
        transcclean = transcdic['data']
        print(transcdic['data'])
        createdat = custinfo['created_at']
        updatedat = custinfo['updated_at']
        createdat = createdat[:-10]
        updateat = updatedat[:-10]
        for item in transcclean:
            item['amount'] = item['amount']/100
            item['transaction_type'] = item['transaction_type'].capitalize()
            item['booking_date'] = item['booking_date'][:-15]
            item['value_date'] = item['value_date'][:-15]
        currentuserurl = "https://api.tp.sandbox.fidorfzco.com/users/current"

        payload={}
        headers = {
        'Authorization': 'Bearer ' + token['access_token'],
        'Accept': 'application/vnd.fidor.de;version=1;text/json',
        'Cookie': 'session_token=eb8edd8c12a2509c16b03d117308de2e11598743; account=IntcImFjY291bnRcIjp7XCJhY2NvdW50X25vXCI6MzczNzgxNDIsXCJmaXJzdG5hbWVcIjpcIkN1c3RvbWVyXCIsXCJsYXN0bmFtZVwiOlwiQiBPTkVcIixcInRpdGxlXCI6bnVsbCxcImFkcl9zdHJlZXRcIjpcIlJvdGtlaGxjaGVuc3RyLlwiLFwiYWRyX3N0cmVldF9uclwiOlwiNjRiXCIsXCJhZHJfemlwXCI6XCIyMjg1MVwiLFwiYWRyX2NpdHlcIjpcIk5vcmRlcnN0ZWR0XCIsXCJhZHJfY291bnRyeVwiOlwiREVcIixcImFkcl9waG9uZVwiOm51bGwsXCJhZHJfbW9iaWxlXCI6bnVsbCxcImFkcl9mYXhcIjpudWxsLFwiYmlydGhkYXlcIjpcIjE5OTYtMDQtMzBcIixcImZvcmVpZ25fYWNjb3VudF9ub1wiOlwiNDQxNDQ5ODI0M1wiLFwiZW1haWxfZW1haWxcIjpcImN1c3RvbWVyYjFAZXhhbXBsZS5jb21cIixcImlzX2NvcnBvcmF0ZVwiOmZhbHNlLFwicGhvdG9cIjpudWxsLFwicHJlZmVycmVkX2xhbmd1YWdlXCI6bnVsbH19Ig%3D%3D--28309c9cf0e588e7d51ff4e38dc365860219f682'
        }
        currentuserresponse = requests.request("GET", currentuserurl, headers=headers, data=payload)
        currentuser = json.loads(currentuserresponse.text)
        currentuser['last_sign_in_at'] = currentuser['last_sign_in_at'][:-10]
        return render_template('profile.html', id = custinfo["id"], firstname = custinfo['first_name'], lastname = custinfo['last_name'],
        accountno = customerdetails['account_number'], balance = (customerdetails["balance"]/100), transcdata = transcclean, nick = custinfo['nick'], customerdetails = customerdetails, custinfo = custinfo, custbirthday = custbirthday, createdat = createdat,
        updateat = updateat, currentuser = currentuser)
    except KeyError:
        print("key error")
        return redirect(url_for('index'))