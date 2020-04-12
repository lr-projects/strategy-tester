#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import os
from datetime import datetime

def get_jsonparsed_data(url):
  """
  Receive the content of ``url``, parse it as JSON and return the object.

  Parameters
  ----------
  url : str

  Returns
  -------
  dict
  """
  response = urlopen(url)
  data = response.read().decode("utf-8")
  return json.loads(data)
  
def getStocks(url):
  data = get_jsonparsed_data(url)
  result = []
  for stock in data["symbolsList"]:
    result.append(stock["symbol"])
  return result

def calculateROIC(ebit, equities, longTermDebt, cash):
  try:
    value = ebit / (equities + longTermDebt - cash)
  except ZeroDivisionError:
    value = None
  return value

def sortListByDate(unsortedList, dateFieldName, dateFormat):
  try:
    result = sorted(unsortedList, key = lambda x: datetime.strptime(x[dateFieldName],dateFormat))[-1]
  except ValueError:
    result = unsortedList[0]
  return result

def convertValueToFloat(value):
  try:
    floatValue = float(value)
  except ValueError:
    print value
    floatValue = None
  return floatValue
  
def dataToROIC(incomeStatement, balanceStatement):
  latestIncomeStatement = sortListByDate(incomeStatement["financials"], "date", "%Y-%m-%d")
  latestBalanceStatement = sortListByDate(balanceStatement["financials"], "date", "%Y-%m-%d")
  
  ebit = convertValueToFloat(latestIncomeStatement["EBIT"])
  equities = convertValueToFloat(latestBalanceStatement["Total shareholders equity"])
  debt = convertValueToFloat(latestBalanceStatement["Long-term debt"])
  cash = convertValueToFloat(latestBalanceStatement["Cash and cash equivalents"])
  
  if ebit == None or equities == None or debt == None or cash == None:
    return None
  else:
    return calculateROIC(ebit, equities, debt, cash)
  
def getDataForTicker(ticker, baseURL):
  incomeURL = baseURL + "/api/v3/financials/income-statement/" + ticker
  balanceURL = baseURL + "/api/v3/financials/balance-sheet-statement/" + ticker
  
  return (get_jsonparsed_data(incomeURL), get_jsonparsed_data(balanceURL))
	
if __name__=='__main__':
  stockListURI = "/api/v3/company/stock/list"
  baseURL = "https://financialmodelingprep.com"
  
  pathToStocks = "./data/stocks.txt"
  
  if os.path.exists(pathToStocks):
    f=open(pathToStocks, "r")
    f1 = f.readlines()
    stocks = []
    for line in f1:
      stocks.append(line)
    f.close()
  else:
    stocks = getStocks(baseURL + stockListURI)
    f=open(pathToStocks,'w')
    for ele in stocks:
      f.write(ele+'\n')
    f.close()
  
  result = {}
  numStocks = len(stocks)
  completed = 0
  for stock in stocks:
    data = getDataForTicker(stock, baseURL)
    if len(data[0].keys()) > 0:
      try:
        roic = dataToROIC(data[0], data[1])
        result[stock] = roic
      except:
        print "could not process " + stock
    completed += 1
    print "completed " + str(completed) + " out of a total of " + str(numStocks) + " stocks."
  
  f=open("./data/results.csv",'w')
  for k, v in result.iteritems():
    f.write(str(k) + ',' + str(v) +'\n')
  f.close()