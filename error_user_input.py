"""
The only thing you will ever need from this is errors(form).
Don't use anything else.
"""


# Global variables for readability
MATCH_INPUT = {"top": "top_school", "bottom": "bottom_school",
               "random": "random_school", "name": "name_school"}


def errors(form):
    """Returns message of what user didn't give in"""
    # Used to highlight what field the user messed up on
    error_highlight = []

    # Check if user gave one of each main input and not anymore
    # (denoted by <h3> excluding <h3>Extra</h3>)
    error_highlight.extend(check_all_radio_inputs(form))

    # Forces the user to enter all the radio buttons first
    if error_highlight:
        return error_highlight

    # Forces the user to give a response to the radio button in processed data format
    error_highlight.extend(missing_matching_radio(form))

    if error_highlight:
        return error_highlight

    # Checks if user gave a valid school name or a numeric response
    error_highlight.extend(check_correct_type_input(form))

    return error_highlight

'''
Helper functions
'''


def check_all_radio_inputs(form):
    """User clicked all 3 radio buttons"""
    error_highlight = []
    missing_format = "Missing {}"
    if "export_type" not in form:
        error_highlight.append(missing_format.format("export_type"))

    if "processed_format" not in form:
        error_highlight.append(missing_format.format("processed_format"))

    if "processed_based" not in form:
        error_highlight.append(missing_format.format("processed_based"))

    return error_highlight


type = ""  # Matches radio button to textfield


def missing_matching_radio(form):
    """A number/name for each radio button on section 'Processed Data Formatted'"""
    error_highlight = []

    global type
    type = form["processed_format"]

    if MATCH_INPUT[type] not in form:
        error_highlight.append("Missing {}".format(MATCH_INPUT[type]))
    return error_highlight


def check_correct_type_input(form):
    """School name enters exists or number given for fields needing them"""
    error_highlight = []
    if type == "name":
        pass
    else:
        # Has to be numerical value less than or equal to amount of highschools(640)
        if form[MATCH_INPUT[type]].isdigit():
            if int(form[MATCH_INPUT[type]]) > 640:
                error_highlight.append("overflow_school {}".format(form["processed_format"]))
        else:
            error_highlight.append("not_number {}".format(form["processed_format"]))
    return error_highlight

