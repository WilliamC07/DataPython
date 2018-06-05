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

    # Generate all the data to be used
    data.initialize()

    # Check if user entered valid information and make user reenter if wrongly filled
    errors = error.errors(form)

    # Generation of body to pass into generate_webpage
    body = ""
    body += str(form)
    body += str(errors)
    generate_webpage(body)


if __name__ == "__main__":
    main()
