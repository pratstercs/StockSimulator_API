#!/usr/bin/env python

from flask import Flask, make_response
import json
import dbFunctions
app = Flask(__name__)

import stocks

def formatDate(date):
	return date[:4] + '-' + date[4:6] + '-' + date[6:8]

def makeResponse(data):
	return make_response(json.dumps(data))

@app.route('/')
def details():
	details = """
	<h1>StockSimulator API</h1>
	<p>
	<code>/[symbol]</code> gets the last year's data for the specified stock symbol (e.g. JPM)
	<br />
	<code>/[symbol]/[startDate]</code> gets the data for that symbol since the specified date in the format YYYYMMDD (e.g. /JPM/20151231)
	<br />
	<code>/[symbol]/[startDate]/[endDate]</code> gets the data for that symbol in the specified range, in the same format as above.
	<p/>
	All queries respond with either a text array or a 500 error:
	<ul>
	<li>Ticker is invalid</li>
	<li>Ticker is not in Quandl's data (check https://www.quandl.com/data/WIKI/<symbol>)</li>
	<ul>
	"""
	return details

@app.route('/<symbol>')
def requestSymbol(symbol):
	print("Request recieved: " + symbol)

	data = stocks.getYearsData(symbol)
	return makeResponse(data)

@app.route('/<symbol>/<date>')
def requestSymbolStartDate(symbol, date):
	print("Request recieved: " + symbol + ", date: " + date)
	dateStr = formatDate(date)

	data = stocks.getDataSince(symbol,dateStr)
	return makeResponse(data)

@app.route('/<symbol>/<startDate>/<endDate>')
def requestSymbolDateRange(symbol, startDate, endDate):
	print("Request recieved: " + symbol + ", startDate: " + startDate + ", endDate: " + endDate)
	start = formatDate(startDate)
	end = formatDate(endDate)

	data = stocks.getData(symbol,startDate,endDate)
	return makeResponse(data)

@app.route('/<symbol>/<startDate>/<endDate>/c')
def requestChange(symbol, startDate, endDate):
	print("Request recieved: " + symbol + ", startDate: " + startDate + ", endDate: " + endDate + " percentage change")
	start = formatDate(startDate)
	end = formatDate(endDate)

	data = stocks.getChange(symbol,startDate,endDate)
	return makeResponse(data)

if __name__ == "__main__":
    app.run('0.0.0.0') #run on requests from all IPs, not just localhost