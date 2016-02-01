import Quandl
import datetime
import uuid
import numpy as np
import pandas as pd
from cassandra.cluster import Cluster
import cassandra.util

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

	#convert the returned Panadas DataFrame to a 2D array (so that it's actually useful)
	array = data.to_records()
	return array

#connect to the Cassandra database
def initSession():
	cluster = Cluster(['91.121.25.208'])
	session = cluster.connect('nyse')
	return session

def getSymbol(session, symbol):
	rows = session.execute('SELECT * FROM ' + symbol)
	return rows

def printRows(resultSet):
	for row in resultSet:
		print row[0], row[1], row[2], row[3], row[4]

def arrayToDatabase(session,array):
	for row in array:
		print(row)
		rowToDatabase(session, row)

def rowToDatabase(session, array):
	date = dateTimeToMillis(array[0])
	op = array[1]
	hi = array[2]
	lo = array[3]
	cl = array[4]
	vol = int(array[5])
	uid = genUUID(array[0])

	session.execute(
		"""
		INSERT INTO jpm (uid, date, open, high, low, close, volume)
		VALUES(%s, %s, %s, %s, %s, %s, %s)
		""",
		(uid, date, op, hi, lo, cl, vol)
		)

def dateTimeToMillis(date):
	epoch = datetime.datetime.utcfromtimestamp(0)
	delta = date - epoch
	delta = delta.total_seconds() * 1000
	return int(delta)

def genUUID(date):
	return cassandra.util.uuid_from_time(date)