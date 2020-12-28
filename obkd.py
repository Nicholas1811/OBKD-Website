from flask import Flask, render_template, redirect, url_for,request,session,json
from datetime import date, timedelta, datetime
from datetime import datetime
import requests
import json
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import random
import string

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
@app.before_request
def make_session_permanent():
    session.permanent = True
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
    print(session)
    return render_template("usequity.html",usequitylist = tickerCodes)
#Shows the equity info plus, routing for the pages, uses 2 alphavantage + 1 outside API
def callEquity(stockticker):
        url = "https://www.alphavantage.co/query?apikey=IXYARDFBT1Y30V7J&function=OVERVIEW&symbol="+stockticker
        pricingurl = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol="+stockticker+"&interval=1min&apikey=IXYARDFBT1Y30V7J"
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
        pastprices = pricesdic["Time Series (1min)"][lastrefreshed]
        for v in pastprices:
            print(v)
            print(pastprices[v])
            pastprices[v] = round(float(pastprices[v]),2)
        sgd = round(float(fxrate['rates']["SGD"]),2)
        sgdrate = sgd
        currentprice = pastprices["4. close"]
        currentpriceint = round(float(currentprice),2)
        valuetoberounded = sgdrate*currentpriceint
        totalvalue = round(valuetoberounded,2)
        marketcap = int(round(round(float(eqdata['MarketCapitalization']) , 2)/1000000000,2))
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
        grossprofit = int(round(round(float(eqdata['GrossProfitTTM']),2)/1000000,2))
        ebitda = int(round(round(float(eqdata['EBITDA']),2)/1000000 ,2))
        epsttm = round(float(eqdata['DilutedEPSTTM']),2)
        beta = round(float(eqdata['Beta']),2)
        weekhigh = round(float(eqdata['52WeekHigh']),2)
        weeklow = round(float(eqdata['52WeekLow']),2)
        shortma = round(float(eqdata['50DayMovingAverage']) ,2)
        longma = round(float(eqdata['200DayMovingAverage']) ,2)
        sharesoutstanding = int(round(round(float(eqdata['SharesOutstanding']),2)/1000000,0))
        sharesfloat = int(round(round(float(eqdata['SharesFloat']),2),0)/1000000)
        sharesshort = int(round(round(float(eqdata['SharesShort']),2),0)/1000000)
        shortratio = round(float(eqdata['ShortRatio']),2)
        insider = round(float(eqdata['PercentInsiders']),2)
        institutions = round(float(eqdata['PercentInstitutions']),2)
        forwardannualdividendrate = round(float(eqdata['ForwardAnnualDividendRate']))
        forwardannualdividendyield = round(float(eqdata['ForwardAnnualDividendYield']))
        payoutratio = round(float(eqdata['PayoutRatio']))
        divdate = eqdata['DividendDate']
        exdivdate = eqdata['ExDividendDate']
        lastsplitfactor = eqdata['LastSplitFactor']
        lastsplitdate = eqdata['LastSplitDate']
        checker = "False"
        if not session.get("watchList") is None:
            checker = "False"
            sessionwatchlist = session['watchList']
            for i in range(0, len(sessionwatchlist)):
                print(i)
                print(sessionwatchlist[i])
                if sessionwatchlist[i]['stockticker'] == stockticker:   
                    checker = True
                    checker = str(checker)
                    break
            else:
                checker = False
                checker = str(checker)
                print(checker+ "item does not exist")
        incomestatementurl = "https://financialmodelingprep.com/api/v3/income-statement/"+stockticker+"?limit=120&apikey=9496cb244ba6da3d33f1f7f6f234e387"
        incomestatementresponse = requests.request('GET', incomestatementurl, headers = headers, data = payload)
        incomestatementdic = json.loads(incomestatementresponse.text)
        for i in reversed(range(len(incomestatementdic))):
            if i < 5:
                 pass
            else:
                del incomestatementdic[i]
        for i in range(len(incomestatementdic)):
            for k,v in incomestatementdic[i].items():
                if k != "eps" and k!= "epsdiluted" and k!= "link" and k!= "finalLink" and k != "symbol" and k!= "fillingDate" and k!= "acceptedDate" and k!= "date" and k!= "period" :
                    v = v/1000000
                    v = int(v)
                    incomestatementdic[i][k] = v
        balancesheeturl = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/"+stockticker+"?limit=120&apikey=9496cb244ba6da3d33f1f7f6f234e387"
        balancesheetresponse = requests.request('GET', balancesheeturl, headers = headers , data = payload)
        balancesheetdic = json.loads(balancesheetresponse.text)
        for i in reversed(range(len(balancesheetdic))):
            if i > 4:
                del balancesheetdic[i]
        for i in range(len(balancesheetdic)):
            for k,v in balancesheetdic[i].items():
                if k!= "link" and k!= "finalLink" and k != "symbol" and k!= "fillingDate" and k!= "acceptedDate" and k!= "date" and k!= "period":
                    v = v/1000000
                    v = int(v)
                    balancesheetdic[i][k] = v
        cashflowurl = "https://financialmodelingprep.com/api/v3/cash-flow-statement/"+stockticker+"?limit=120&apikey=9496cb244ba6da3d33f1f7f6f234e387"
        cashflowresponse = requests.request('GET', cashflowurl, headers = headers , data = payload)
        cashflowdic = json.loads(cashflowresponse.text)
        for i in reversed(range(len(cashflowdic))):
            if i > 4:
                del cashflowdic[i]
        for i in range(len(cashflowdic)):
            for k,v in cashflowdic[i].items():
                if k!= "link" and k!= "finalLink" and k != "symbol" and k!= "fillingDate" and k!= "acceptedDate" and k!= "date" and k!= "period":
                    v = v/1000000
                    v = int(v)
                    cashflowdic[i][k] = v
        historic = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol="+stockticker+"&apikey=ELNT38TEYXQOL7WS"
        historicresponse = requests.request("GET", historic, headers=headers, data=payload)
        historicdata = json.loads(historicresponse.text)
        cleanedhistoric = historicdata['Weekly Time Series']
        for k,v in cleanedhistoric.items():
            v['1. open'] = round(float(v['1. open']),2)
            v['2. high'] = round(float(v['2. high']),2)
            v['3. low'] = round(float(v['3. low']),2)
            v['4. close'] = round(float(v['4. close']),2)
            v['5. volume'] = int(float(v['5. volume'])/1000000)
        generalnewsurl = "https://stocknewsapi.com/api/v1/category?section=general&items=5&token=ou8oq2qc8dlnl3v5ejansi6fcp0msblaqluzzg8j"
        stocknewsurl = "https://stocknewsapi.com/api/v1?tickers="+stockticker+"&items=5&token=ou8oq2qc8dlnl3v5ejansi6fcp0msblaqluzzg8j"
        generalnewsresponse = requests.request("GET", generalnewsurl, headers=headers, data=payload)
        stocknewsresponse = requests.request('GET', stocknewsurl, headers = headers, data = payload)
        generalnewsdic = json.loads(generalnewsresponse.text)
        stocknewdic = json.loads(stocknewsresponse.text)
        cleanednews = generalnewsdic['data']
        stocknews = stocknewdic['data']
        print(cleanednews)
        for i in stocknews:
            i['date'] = i['date'][:-14]
        for i in cleanednews:
             i['date'] = i['date'][:-14]
        return render_template ('usequityinfo.html', pricesdic = pricesdic, pastprices = pastprices, eqdata = eqdata, sgd = sgd, 
        totalvalue = totalvalue, operatingmargin  = operatingmargin ,profitmargin = profitmargin, returnonasset = returnonasset, returnonequity = returnonequity,
        quarterlyrevenuegrowth = quarterlyrevenuegrowth, quarterlyearningsgrowth = quarterlyearningsgrowth, insider = insider, 
        institutions = institutions, trailingPE = trailingPE, forwardPE = forwardPE, pegRatio = pegRatio, pricetosales = pricetosales,
        pricetobook = pricetobook, enrev = envrev, eneb = eneb, revpershare = revpershare, gp = grossprofit, ebitda = ebitda,
        epsttm = epsttm, beta = beta, weekhigh = weekhigh, weeklow = weeklow, shortma = shortma, longma = longma, sharesoutstanding = sharesoutstanding,
        sharesfloat = sharesfloat, sharesshort = sharesshort, shortratio = shortratio, forwardannualdividendyield = forwardannualdividendyield, 
        forwardannualdividendrate = forwardannualdividendrate, payoutratio = payoutratio, divdate = divdate, exdivdate = exdivdate, 
        lastsplitdate = lastsplitdate, lastsplitfactor = lastsplitfactor, marketcap = marketcap, historic = cleanedhistoric, checker = checker,
        incomestatementdic = incomestatementdic, balancesheetdic = balancesheetdic, cashflowdic = cashflowdic,generalnewsdic = cleanednews, stocknews=stocknews,)

@app.route("/usequityinfo", methods = ['GET', 'POST'])
def usequityinfo():
    stockticker = request.form['stockticker']
    return callEquity(stockticker)
@app.route("/search", methods = ['GET','POST'])
def searchinfo():
    try:
        searchticker = request.form['search']
        searchurl = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords="+searchticker+"&apikey=RU0OE9SIH6R38HXY"
        headers = {}
        payload = {}
        searchresponse = requests.request('GET', searchurl, headers = headers, data = payload)
        searchresult = json.loads(searchresponse.text)
        searchticker = searchresult['bestMatches'][0]["1. symbol"]
        return callEquity(searchticker)
    except IndexError:
        return "Bad Search result"
    except KeyError:
        return "MAX API Calling."
@app.route('/', methods = ['GET'])
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
    return redirect(url_for('.index')) 
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
            item['subject'] = item['subject'][61:]
            item['updated_at'] = item['updated_at'][:-10]
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
@app.route('/buy',methods= ['POST'])
def buy():
    if request.method == "POST":
        token = session['oauth_token']
        print(token)
        customerAccount = session['fidor_cust']
        customerDetails = customerAccount['data'][0]
        print(customerDetails)
        fidorID = customerDetails['id']
        customerEmail = "studentB17@email.com"
        amountOfStock = int(request.form['amount'])
        equityname = request.form['equityname']
        stockticker = request.form['stockticker']
        print(amountOfStock)
        print(request.form['priceinsgd'])
        transferAmount=int(float(request.form['priceinsgd'])*100)
        print(transferAmount)
        totalAmount = int(amountOfStock*transferAmount)
        transferRemarks = "Purchase of " + equityname + " (" + stockticker +")"
        letters = string.ascii_lowercase
        transferRandomNumeric = ''.join(random.choice(letters) for i in range(10))
        if totalAmount < 3500000:
            url = "https://api.tp.sandbox.fidorfzco.com/internal_transfers"

            payload="{\r\n    \"account_id\" : \""+fidorID+"\",\r\n    \"receiver\": \""+customerEmail+"\",\r\n    \"external_uid\" : \""+transferRandomNumeric+"\",\r\n    \"amount\" : \""+str(totalAmount)+"\",\r\n    \"subject\" : \""+transferRemarks+"\"\r\n}"
            headers = {
            'Authorization': 'Bearer ' + token['access_token'],
            'Accept': 'application/vnd.fidor.de;version=1;text/json',
            'Content-Type': 'application/json',
            'Cookie': 'session_token=a1945e8081f5c2c9a1aa5637462f2e469fbeb0dc; account=IntcImFjY291bnRcIjp7XCJhY2NvdW50X25vXCI6MzczNzgxNDIsXCJmaXJzdG5hbWVcIjpcIkN1c3RvbWVyXCIsXCJsYXN0bmFtZVwiOlwiQiBPTkVcIixcInRpdGxlXCI6bnVsbCxcImFkcl9zdHJlZXRcIjpcIlJvdGtlaGxjaGVuc3RyLlwiLFwiYWRyX3N0cmVldF9uclwiOlwiNjRiXCIsXCJhZHJfemlwXCI6XCIyMjg1MVwiLFwiYWRyX2NpdHlcIjpcIk5vcmRlcnN0ZWR0XCIsXCJhZHJfY291bnRyeVwiOlwiREVcIixcImFkcl9waG9uZVwiOm51bGwsXCJhZHJfbW9iaWxlXCI6bnVsbCxcImFkcl9mYXhcIjpudWxsLFwiYmlydGhkYXlcIjpcIjE5OTYtMDQtMzBcIixcImZvcmVpZ25fYWNjb3VudF9ub1wiOlwiNDQxNDQ5ODI0M1wiLFwiZW1haWxfZW1haWxcIjpcImN1c3RvbWVyYjFAZXhhbXBsZS5jb21cIixcImlzX2NvcnBvcmF0ZVwiOmZhbHNlLFwicGhvdG9cIjpudWxsLFwicHJlZmVycmVkX2xhbmd1YWdlXCI6bnVsbH19Ig%3D%3D--28309c9cf0e588e7d51ff4e38dc365860219f682'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            transactiondetails = json.loads(response.text)
            print(response.text + "process")
            new_data = {"stockticker" : stockticker, "equityname" : equityname, "totalamount" : totalAmount, "totalshare" : amountOfStock}
            if session.get("portfolio") is None:
                data = []
                data.append(new_data)
                session["portfolio"] = data
            else:
                currentport = session['portfolio']
                for i in currentport:
                    print(i['stockticker'])
                    if i['stockticker'] == stockticker:
                        totalIntToAdd = int(i['totalamount']) + int(totalAmount)
                        totalStockToAdd = int(i['totalshare']) + int(amountOfStock)
                        i['totalamount'] = totalIntToAdd
                        i['totalshare'] = totalStockToAdd
                        break
                else:
                    new_data_copy = new_data.copy()
                    currentport.append(new_data_copy)
                    session['portfolio'] = currentport
                    print(session['portfolio'])
            sector = request.form['sector']
            sector_data = {"sector" : sector, "totalamount" : totalAmount}
            if session.get("sectorportfolio") is None:
                sectordata = []
                sectordata.append(sector_data)
                session["sectorportfolio"] = sectordata
            else:
                sectorport = session['sectorportfolio']
                for i in sectorport:
                    if i['sector'] == sector:
                        totalAdd = int(i['totalamount']) + int(totalAmount)
                        i['totalamount'] = totalAdd
                        break
                else:
                    sector_data_copy = sector_data.copy()
                    sectorport.append(sector_data_copy)
                    session['sectorportfolio'] = sectorport
                    print(session)
            totalAmountdisplay = totalAmount/100
            return render_template("transactionComplete.html", transferRemarks = transferRemarks, totalAmount= totalAmountdisplay, id =customerDetails['account_number'], amountOfStock = amountOfStock)
        else:
            return render_template("transactionComplete.html" , totalAmount =totalAmount)
@app.route('/addToWishList', methods = ['POST'])
def addToWishList():
    stockticker = request.form['stocksymbol']
    equityname = request.form['equityname']
    new_data = {"stockticker" : stockticker , "equityname" : equityname}
    #ensuring that the session is empty then, add new value
    if session.get("watchList") is None:
        data = []
        data.append(new_data)
        session['watchList'] = data
    else:
        currentwatch = session['watchList']
        print(currentwatch)
        new_data_copy = new_data.copy()
        currentwatch.append(new_data_copy)
        session['watchList'] = currentwatch
        print(session['watchList'])
    return towatchlist()
@app.route("/openfromwatchlist", methods=["POST"])
def openfromwatchlist():
    stockticker = request.form['stockticker']
    return callEquity(stockticker)
@app.route("/removeFromWishlist", methods = ['POST'])
def removeFromWishlist():
    removing = session['watchList']
    stockticker = request.form['stocksymbol']
    for i in range (len(removing)):
        if removing[i]['stockticker'] == stockticker:
            del removing[i]
            break
    session['watchList'] = removing
    print(removing)
    return towatchlist()
@app.route("/watchlist", methods = ['GET'])
def watchlist():
    return towatchlist()
def towatchlist():
    userWatchlist = session['watchList']
    watchlist = []
    for i in userWatchlist:
        print(i)
        watchlist.append(i)
        print(watchlist)
    if len(watchlist) == 0:
        check = "True"
    else:
        check = "False"
    print(check)
    return render_template('viewWatchlist.html',watchlist = watchlist, check = check)
@app.route("/portfolio", methods = ['GET'])
def portfolio():
    userportfolio = session['portfolio']
    portfolio = []
    for i in userportfolio:
        print(i)
        portfolio.append(i)
        print(portfolio)
    sectorportfolio = session['sectorportfolio']
    sectorport = []
    for i in sectorportfolio:
        print(i)
        sectorport.append(i)
        print(sectorportfolio)
    return render_template('viewPortfolio.html', portfolio = json.dumps(portfolio), sectorport = json.dumps(sectorport))