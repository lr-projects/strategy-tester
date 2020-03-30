# Read the CSV
# Sort it by the date
# Imagine a set of investors, who each begin investing 1k into the FTSE 100 on a monthly basis and continue for 20 years
# We want to calculate the capital they have at the end (through investing alone)
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def readData(filepath):
  raw = list(csv.reader(open(filepath), delimiter=','))[1:]
  data = sorted(list(map(lambda x: (datetime.strptime(x[0], '%b %d, %Y'), x[4]), raw)), key = lambda x: x[0])
  return data
  
def expectedValue(input):
  hi = np.histogram(input, bins = xrange(int(input.min()), int(input.max()+1), 1), density = True)
  
  expectedValue = 0
  for i in xrange(0, len(hi)):
    expectedValue += hi[0][i]*hi[1][i]
  return expectedValue

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
  
  

path = "C:\Users\Luke\Documents\Finance\FTSE_monthly.csv"
workingData = readData(path)

monthlyInvestment = 1000.0
years = 30
yearsInMonths = years * 12
yearlyYield=0.02

capitalAppreciationModel(workingData, yearsInMonths, monthlyInvestment, yearlyYield)

# We should ignore any yield initially
# We could extend this to consider their drawdown after this initial 20 year period is over