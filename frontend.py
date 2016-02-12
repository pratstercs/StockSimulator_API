#!/usr/bin/env python

from flask import Flask, make_response
import json
app = Flask(__name__)

import stocks

def formatDate(date):
	return date[:4] + '-' + date[4:6] + '-' + date[6:8]

def makeResponse(data):
	return make_response(json.dumps(data))

@app.route('/')
def details():
	return 'Insert API details here!'

@app.route('/<symbol>')
def requestSymbol(symbol):
	print("Request recieved: " + symbol)

	data = stocks.getMonthsData(symbol)
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

if __name__ == "__main__":
    app.run('0.0.0.0') #run on requests from all IPs, not just localhost