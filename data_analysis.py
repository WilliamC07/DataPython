#  correlation coefficient r
def prod(list1, list2):
  '''Generate list from the product of elements of the same index'''
  newList = []
  idx = 0
  while idx < len(list1):
    newList.append(list1[idx] * list2[idx])
    idx += 1
  return newList

def squareList(list1):
  '''squares the values in a list'''
  newList = []
  idx = 0
  while idx < len(list1):
    newList.append(list1[idx]**2)
    idx += 1
  return newList

def correlation(x,y):
  '''solve for r, the strength and direction between 2 points on a scatterplot
  value of r is between +1 and -1'''
  n = len(x)  # the number of pairs given that x and y are the same length
  numerator = (n * (sum(prod(x,y))) - sum(x) * sum(y))
  denominator = ((n*sum(squareList(x))-((sum(x))**2)) * (n*sum(squareList(y))-((sum(y))**2)))**.5
  return numerator / denominator  # the correlation coefficient r
 
# print(correlation([43,21,25,42,57,59],[99,65,79,75,87,81]))
# => 0.5298089018901744


# Line of best fit
def mean(list):
  '''finds the mean of a list'''
  return sum(list)/float(len(list))

def calc(list1):
  '''creates a list of the calculated result for the numerator of the slope'''
  newList = []
  idx = 0
  while idx < len(list1):
    newList.append(list1[idx]-mean(list1))  # calculates the difference of each index of list1 minus the mean of list1
    idx += 1
  return newList

def regressionLine(x,y):
  '''Find the values of a and b in the eqtn, y = ax +  b, for the line of best fit of the scatterplot data from lists, x and y'''
  eqtn = {}
  A = 0  # A is the slope
  numerator = sum(prod(calc(x),calc(y)))
  denominator = sum(squareList(calc(x)))
  A = numerator / denominator  # slope
  B = mean(y) - A * mean(x)  # B is the y-intercept
  eqtn["a"] = A  # value of a
  eqtn["b"] = B  # value of b
  return eqtn

# print(regressionLine([9,13,21,30,31,31,34,25,28,20,5],[260,320,420,530,560,550,590,500,560,440,300]))
# => {'a': 11.7312808818, 'b': 193.852147472}
