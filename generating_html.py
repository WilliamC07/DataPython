"""This is only used to generate elements of a HTML page with inline css"""


def get_head(title="Data!"):
    """Gives the start of html files"""
    return '''<!DOCTYPE html><html><head><title>{}</title>
    </head>'''.format(title)


def get_tail():
    return ''' </body></html>'''


def make_div(design, *args):
    div_head = "<div style= \"{}\">".format(design)
    for body in args:
        div_head += body
    return "{}</div>".format(div_head)


def make_header(heading, design, body):
    return "<h{0} style= \"{1}\"> {2} </h{0}>".format(heading, design, body)


def make_paragraph(message):
    # \n doesn't work on <p>, must use <br/> instead
    return "<p>{}</p>".format(message.replace("\n", "<br/>"))


def make_ordered_list(design, body):
    frame = "<ol style = \"{0}\"> {1} </ol>".format(design, body)
    return frame


def make_list(design, inside, outside):
    """Makes item inside a <li></li> but also allows things outside: <li></li><p></p>"""
    return "<li style = \"{0}\">{1}</li> {2}".format(design, inside, outside)


def generate_webpage(*args):
    """First element passed in must be the get_head"""
    html = ""
    for element in args:
        html += element
    return html


def make_bold(text):
    return "<b>{}</b>".format(text)


# Debugging
if __name__ == "__main__":
    print(make_div(3, "", "General Data"))
