#!/usr/bin/python
print "Content-type: text/html\n"

#Enable exec. permission by fileZilla

# We need these library modules to retrieve the user's answers
import cgi

#help you see errors
import cgitb
cgitb.enable()



head = '''<!DOCTYPE html>
<html>
  <head>
   <title>Demo!</title>
  </head>
  <body>'''

print head


print ''' </body>
</html>'''


# I include this function to convert a python cgi field storage to a standard dictionary.
# This is good enough for 95% of all forms you would want to create!
def cgiFieldStorageToDict( fieldStorage ):
   """Get a plain dictionary, rather than the cgi module field storage."""
   ans = {}
   for key in fieldStorage.keys():
     ans[ key ] = fieldStorage[ key ].value
   return ans
   print(ans)

def main():
    # ask the library function to retrieve all answers and put them
    #   into a dictionary
    form = cgiFieldStorageToDict(cgi.FieldStorage())

    #ONLY FOR DEBUGGING
    #print the form data!
    print form
    print "<br>"

    #lets say you want 2 pieces of information, the name, and the count (number of times to print the name)

    #pick some values that you want as default
    count = -1
    #try to replace it using the form (if it exists!)
    if "count" in form:
        #the data must be integer formatted!
        count = int(form['count'])

    #pick default value
    name = -1
    #try to replace it
    if "name" in form:
        name = form["name"]

    #after getting all the info you need, you can now
    #print the body of your html using the variables that
    #you initialized with the form elements.
    if count == -1 or name == -1:
        #ERROR BODY HERE
        print "<h2>error! Did not receive all required form data!</h2>"
    else:
        #GOOD BODY HERE
        for i in range(count):
            print "Hi "+form["name"]+"!<br>"

main()
