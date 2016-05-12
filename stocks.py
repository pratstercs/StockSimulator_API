import Quandl
import datetime
import uuid
import threading
import numpy as np
import pandas as pd

import dbFunctions

def getData(symbol, startDate, endDate):
	#define the column rows we want
	s = 'WIKI/' + symbol
	s1 = s + ".8"
	s2 = s + ".9"
	s3 = s + ".10"
	s4 = s + ".11"
	s5 = s + ".12"

	#perform the Quandl request
	data = Quandl.get(
		[s1,s2,s3,s4,s5], trim_start=startDate, trim_end=endDate, authtoken="VAjcx6n-wo8WLqb6VD-p")
	
	return convertQuandlToArray(data)

def requestRecieved(symbol,startDate,endDate):
	data = getData(symbol,startDate,endDate)
	#thread.start_new_thread(dbFunctions.arrayToDatabase(data))
	thread = threading.Thread(target = dbFunctions.arrayToDatabase, args = (data, symbol))
	thread.start()
	return data

def getDataSince(symbol,startDate):
	today = datetime.date.today()
	endDate = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
	#return getData(symbol,startDate,endDate)
	return requestRecieved(symbol,startDate,endDate)

def getMonthsData(symbol):
	today = datetime.date.today()
	start = today.replace(month=today.month-1) #get datetime for now - 1 month
	#return getData(symbol,startDate,endDate)
	return requestRecieved(symbol,startDate,endDate)

def getYearsData(symbol):
	today = datetime.date.today()
	start = today.replace(year=today.year-1) #get datetime for now - 1 month
	#return getData(symbol,startDate,endDate)
	return requestRecieved(symbol,startDate,endDate)

def convertQuandlToArray(data):
	array = data.to_records().tolist() #convert the returned Panadas DataFrame to a list of tuples
	array = [list(i) for i in array] #converting list of tuples into list of lists

	for row in array:
		#converts datetime object to string in format "YYYY-mm-DD"
		row[0] = row[0].isoformat('-')[:10]

	return array

def genUUID(date):
	return cassandra.util.uuid_from_time(date)