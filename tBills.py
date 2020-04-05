# Read the CSV
# Sort it by the date
# Imagine a set of investors, who each begin investing 1k into tBills on a monthly basis and continue for X years
# We want to calculate the capital they have at the end (through investing alone)
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from utils import *

def tBillMonthlyModel(data, numMonths, monthlyAmount):
  result = {}
  
  for i in xrange(0, len(data) - numMonths):
    result[i] = 0.0
    for j in xrange(i, i + numMonths):
      monthlyReturn = monthlyAmount * (1 + (float(data[j][1]) / 100.0))
      result[i] += monthlyReturn
  
  toPlot = map(lambda x: [x[0], x[1]], result.items())
  
  x = []
  y = []
  
  for item in toPlot:
    x.append(item[0])
    y.append(item[1])
  
  # Plot the return for each investor
  plt.plot(x,y)
  plt.plot(x, np.zeros([len(x),1])+(numMonths * monthlyAmount))
  plt.show()
  
  # Plot the ROIC 
  roic = ((np.asarray(y) / float(numMonths * monthlyAmount)) - 1)*100
  plt.hist(roic, bins=xrange(0,30,2))
  plt.show()
  
  print expectedValue(roic)
  
  
if __name__=='__main__':
  path = 'C:\\Users\\Luke\\Documents\\Finance\\1YearBond_monthly.csv'
  workingData = readData(path, 0, 1, '%b %y')

  monthlyInvestment = 1000.0
  years = 10
  yearsInMonths = years * 12
  
  tBillMonthlyModel(workingData, yearsInMonths, monthlyInvestment)