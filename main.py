#!/usr/bin/python
print "Content-type: text/html\n"

import cgi
import cgitb
import generating_html as webgen

#See errors
cgitb.enable()

def cgiFieldStorageToDict(fieldStorage):
	ans = {}
	for key in fieldStorage.keys():
		ans[key] = fieldStorage[key].value
	return ans

