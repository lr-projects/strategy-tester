# Read the CSV
# Sort it by the date
# Imagine a set of investors, who each begin investing 1k into the FTSE 100 on a monthly basis and continue for 20 years
# We want to calculate the capital they have at the end (through investing alone)
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from utils import *

def capitalAppreciationModel(data, numMonths, monthlyAmount, yearlyYield):
  result = {}
  
  for i in xrange(0, len(data) - numMonths):
    result[i] = [[0, 0.0]]
    for j in xrange(i, i + numMonths):
      quantity = (monthlyAmount / float(data[j][1])) * ( 1 + (yearlyYield / 12))
      previousResult = result[i][-1]
      newResult = [previousResult[0] + quantity, (previousResult[0] + quantity) * float(data[j][1])]
      result[i].append(newResult)
  
  toPlot = map(lambda x: [x[0], x[1][-1]], result.items())
  
  x = []
  y = []
  
  for item in toPlot:
    x.append(item[0])
    y.append(item[1][1])
  
  # Plot the return for each investor
  plt.plot(x,y)
  plt.plot(x, np.zeros([len(x),1])+(numMonths * monthlyAmount))
  plt.show()
  
  # Plot the ROIC 
  roic = ((np.asarray(y) / float(numMonths * monthlyAmount)) - 1)*100
  plt.hist(roic, bins=xrange(-100,100,2))
  plt.show()
  
  print expectedValue(roic)
  
  
if __name__=='__main__':
  path = "C:\Users\Luke\Documents\Finance\FTSE_monthly.csv"
  workingData = readData(path, 0, 4, '%b %d, %Y')

  monthlyInvestment = 1000.0
  years = 5
  yearsInMonths = years * 12
  yearlyYield=0.02
  
  capitalAppreciationModel(workingData, yearsInMonths, monthlyInvestment, yearlyYield)