#!/usr/bin/python

import cgi
import cgitb
import generating_html as webgen

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

def correct_input(form):
    """Returns message of what user didn't give in"""

    # Used to highlight what field the user messed up on
    error_highlight = []

    # Check if user gave one of each main input (denoted by <h3> excluding <h3>Extra</h3>)
    if "export_type" not in form:
        error_highlight.append("export_type")
    else:
        form.pop("export_type")

    if "processed_format" not in form:
        error_highlight.append("processed_format")
    else:
        form.pop("processed_format")

    if "processed_based" not in form:
        error_highlight.append("processed_based")
    else:
        form.pop("processed_based")

    # Check if user gave correct text fill out for processed_format
    message_missing = "Missing:"
    message_too_many_fill = "You needed to fill {} but gave {}"

    if len(form) > 4:
        error_highlight.append("overflow_processed_format")
    # Value of processed_format
    type = ""

    if len(error_highlight) == 0:
        return None
    else:
        pass




def main():
    # Dictionary of inputs
    form = get_cgi_dict()

    # Check if user entered valid information and make user reenter if wrongly filled
    errors = correct_input(None)


    # Generation of body to pass into generate_webpage
    body = ""
    body += str(form)

    generate_webpage(body)


if __name__ == "__main__":
    main()
