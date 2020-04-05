import csv
from datetime import datetime
import numpy as np

def readData(filepath, dateIndex, valueIndex, dateFormat):
  raw = list(csv.reader(open(filepath), delimiter=','))[1:]
  data = sorted(list(map(lambda x: (datetime.strptime(x[dateIndex], dateFormat), x[valueIndex]), raw)), key = lambda x: x[0])
  return data
  
def expectedValue(input):
  hi = np.histogram(input, bins = xrange(int(input.min()), int(input.max()+1), 1), density = True)
  
  expectedValue = 0
  for i in xrange(0, len(hi[0])):
    expectedValue += hi[0][i]*hi[1][i]
  return expectedValue