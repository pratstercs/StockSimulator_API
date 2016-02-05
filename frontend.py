from flask import Flask, make_response
import json
app = Flask(__name__)

import stocks

@app.route('/')
def details():
	return 'Insert API details here!'

@app.route('/<symbol>')
def requestSymbol(symbol):
	#return 'Symbol: %s' % symbol
	print("Request recieved: " + symbol)
	data = stocks.getData(symbol)
	print(data)
	res = make_response(json.dumps(data))
	print(res)
	return res

@app.route('/<symbol>/<date>')
def requestSymbolStartDate(symbol, date):
	dateStr = date[:4] + '-' + date[4:6] + '-' + date[6:8]

	sym = 'Symbol: %s, ' % symbol
	dte ='from date %s' % dateStr
	toReturn = sym + dte

	return toReturn

if __name__ == "__main__":
    app.run('0.0.0.0')