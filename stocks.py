import Quandl
import datetime
import uuid
import numpy as np
import pandas as pd

import dbFunctions

def getData(symbol):
	#define the column rows we want
	s = 'WIKI/' + symbol
	s1 = s + ".8"
	s2 = s + ".9"
	s3 = s + ".10"
	s4 = s + ".11"
	s5 = s + ".12"

	#perform the Quandl request
	data = Quandl.get(
		[s1,s2,s3,s4,s5], trim_start='2016-01-01', trim_end='2016-02-01', authtoken="VAjcx6n-wo8WLqb6VD-p")

	array = data.to_records().tolist() #convert the returned Panadas DataFrame to a list of tuples
	array = [list(i) for i in array] #converting list of tuples into list of lists
	array = convertArrayDateTimeToString(array) #converting datetime objects to strings
	return array

def convertArrayDateTimeToString(array):
	for row in array:
		#converts datetime object to string in format "YYYY-mm-DD"
		row[0] = row[0].isoformat('-')[:10]
	return array


def dateTimeToMillis(date):
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta = date - epoch
	delta = delta.total_seconds() * 1000
	return int(delta)

def genUUID(date):
	return cassandra.util.uuid_from_time(date)