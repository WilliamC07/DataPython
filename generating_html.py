# Basic functions for creating a webpage


def get_head(cssLink="", title="Data!"):
    """Gives the start of html files"""
    return '''<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="{}">
<title>{}</title>
</head>
<body>
</html>'''.format(cssLink, title)


def get_tail():
    return ''' </body>
</html>'''


def make_div(design = "", body):
    return "<div style=\"{}\"> {} </div>".format(design, body)


def make_header(heading, design = "", body)
    return "<h{0} style=\"{1}\">{2}</h{0}>".format(heading, design, body)



def paragraph(message):
    # \n doesn't work on <p>, must use <br/> instead
    return "<p>{}</p>".format(message.replace("\n", "<br/>"))


def generate_webpage(*args):
    """First element passed in must be the get_head"""
    html = ""
    for element in args:
        html += element
    return html


# Debugging
if __name__ == "__main__":
    print(make_div("background-color: #444", "body"))
