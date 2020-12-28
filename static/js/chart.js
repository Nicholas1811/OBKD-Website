var request = new XMLHttpRequest();
var stockticker = document.getElementById('stocktickerforchart').innerHTML
console.log('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + stockticker + '&interval=1min&apikey=RU0OE9SIH6R38HXY')
request.open('GET', 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stockticker + '&interval=1min&apikey=RU0OE9SIH6R38HXY', true)
newArray = []

var chart = LightweightCharts.createChart(document.getElementById('chart'), {
  width: 400,
  height: 300,
  layout: {
    backgroundColor: '#121212',
    textColor: 'rgba(255, 255, 255, 0.9)',
  },
  grid: {
    vertLines: {
      color: '#ffffff00',
    },
    horzLines: {
      color: '#CDCDCD',
    },
  },
  crosshair: {
    mode: LightweightCharts.CrosshairMode.Normal,
  },
  rightPriceScale: {
    borderColor: '#CDCDCD',
  },
  timeScale: {
    borderColor: '#CDCDCD',
  },
});
var candleSeries = chart.addCandlestickSeries({
  upColor: '#32CD32',
  downColor: '#B22222',
  borderDownColor: '#B22222',
  borderUpColor: '#32CD32',
  wickDownColor: '#B22222',
  wickUpColor: '#32CD32',
});

request.onload = function () {
  var data = JSON.parse(request.responseText)
  arraylength = data['Time Series (Daily)']
  for (i in arraylength) {
    var datas = data['Time Series (Daily)'][i]
    var objectfordata = {time: '', open: 0, high: 0, low: 0, close: 0}
    objectfordata.time = new Date(i).toISOString().split('T')[0].toString()
    objectfordata.open = Number((Math.round(Number(datas['1. open']) * 100) / 100).toFixed(2))
    objectfordata.high = Number((Math.round(Number(datas['2. high']) * 100) / 100).toFixed(2))
    objectfordata.low = Number((Math.round(Number(datas['3. low']) * 100) / 100).toFixed(2))
    objectfordata.close = Number((Math.round(Number(datas['4. close']) * 100) / 100).toFixed(2))
    newArray.push(objectfordata)
    //candleSeries.update(objectfordata)
  }
  console.log(newArray)
  newArray = newArray.reverse()
  candleSeries.setData(newArray)
}
// Send request
request.send()

  

