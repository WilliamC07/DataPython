#  Line of best fit


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
