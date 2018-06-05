#!/usr/bin/python

import cgi
import cgitb
import generating_html as webgen
import processing_data as data
import error_user_input as error

print("Content-type: text/html\n")

# See errors
cgitb.enable()


def get_cgi_dict():
    """Get the dictionary of the user inputs"""
    field_storage = cgi.FieldStorage()
    ans = {}
    for key in field_storage.keys():
        ans[key] = field_storage[key].value

    # Makes it easier to debug by removing the "useless" parts
    ans.pop("submit")
    return ans


def generate_webpage(body):
    head_html = webgen.get_head()
    tail_html = webgen.get_tail()
    print(webgen.generate_webpage(head_html, body, tail_html))


def main():
    # Dictionary of inputs
    form = get_cgi_dict()

    # Check if user entered valid information and make user reenter if wrongly filled
    error_web = error.error_website(form)
    if error_web is not None:  # Means there are errors
        print(error.error_website(form))
        return  # Can return since this function is only called once, at the end

    # Generate all the data to be used
    data.initialize()

    # Generation of body to pass into generate_webpage
    body = ""
    body += str(form)
    generate_webpage(body)



main()
