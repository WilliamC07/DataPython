"""
The only thing you will ever need from this is error_website(form).
Don't use anything else.
"""

import generating_html as web_build
import find_school


# Global variables for readability
MATCH_INPUT = {"top": "top_school", "bottom": "bottom_school",
               "random": "random_school", "name": "name_school"}


def error_website(form):
    """Generates website telling user what to fix"""
    to_fix = get_errors(form)

    # If there are no error, the server can start generating data
    if not to_fix:
        return None
    else:
        # Create a string listing all the errors
        errors = "Please fix these first:\n"

        for error in to_fix:
            errors += "{}\n".format(error)

        paragraph = web_build.paragraph(errors)
        website = web_build.generate_webpage(web_build.get_head(title="Error!!!!!"), paragraph, web_build.get_tail())
        return website


def get_errors(form):
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
    missing_format = "Fill out {} section"
    if "export_type" not in form:
        error_highlight.append(missing_format.format("'How do you want the data exported?'"))

    if "processed_format" not in form:
        error_highlight.append(missing_format.format("'Processed Data Formatted'"))

    if "processed_based" not in form:
        error_highlight.append(missing_format.format("'Based on'"))

    return error_highlight


type = ""  # Matches radio button to textfield


def missing_matching_radio(form):
    """A number/name for each radio button on section 'Processed Data Formatted'"""
    error_highlight = []

    global type
    type = form["processed_format"]

    if MATCH_INPUT[type] not in form:
        error_highlight.append("Fill in the textfield that corresponds to the radio button you submitted")
    return error_highlight


def check_correct_type_input(form):
    """School name enters exists or number given for fields needing them"""
    error_highlight = []
    if type == "name":
        if find_school.find_school(form["name_school"]) is None:
            error_highlight.append("The school you entered does not exist")
    else:
        # Has to be numerical value less than or equal to amount of high schools(640)
        if form[MATCH_INPUT[type]].isdigit():
            num_schools = int(form[MATCH_INPUT[type]])
            if num_schools > 640:
                error_highlight.append("You want a list of {} high schools, but there are only 640".format(num_schools))
            elif num_schools <= 0:
                error_highlight.append("You must enter a positive number (A number greater than 0)")
        else:
            error_highlight.append("Enter a integer greater than 0 but less than 461. No decimals/fractions")
    return error_highlight


# Debugging

if __name__ == "__main__":
    pass