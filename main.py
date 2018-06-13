#!/usr/bin/python

import cgi
import cgitb
import generating_html as webgen
import error_user_input as error
import processing_data as processed
import find_school

print("Content-type: text/html\n")

# See errors
cgitb.enable()

# Global var
form = dict()
any_error = False


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


def error_handler():
    # Check if user entered valid information and make user reenter if wrongly filled
    error_web = error.error_website(form)
    if error_web is not None:  # Means there are errors
        print(error.error_website(form))
        global any_error
        any_error = True


def prepare_data_sat():
    # Based on types
    section_type = form["SAT_choice"]

    # Sort
    type = form["processed_format"]
    if type == 'top':
        processed.sort_sat('d', section_type)
    elif type == 'bottom':
        processed.sort_sat('i', section_type)
    elif type == 'random':
        processed.randomize_sat()  # Will be limited to the amount wanted later
    else:
        processed.certain_SAT(find_school.get_school(form["name_school"]), section_type)

    # Limit
    if type != "name":
        MATCH_INPUT = {"top": "top_school", "bottom": "bottom_school",
                       "random": "random_school", "name": "name_school"}

        processed.amount_limiter('sat', int(form[MATCH_INPUT[type]]))
        processed.amount_limiter('survey', int(form[MATCH_INPUT[type]]))

    processed.calculate_averages()


def prepare_data_survey():
    processed.initialize_survey()
    processed.simplify_survey()
    request_to_index = {"teacher": 6, "parent": 5, "student": 7, "safety": 8, "communication": 9,
                        "engagement": 10, "academic": 11, "overall": 12}
    type = form["processed_format"]
    if type == 'top':
        processed.sort_survey('d', request_to_index[form["Survey_choice"]])
    elif type == 'bottom':
        processed.sort_survey('i', request_to_index[form["Survey_choice"]])
    elif type == 'random':
        processed.randomize_survey()


def body_generation():
    """To make it easy, webpage is being built from innermost child to outermost parent
    starting with right side of screen to left side of the screen"""

    # Left side screen
    left_parent_div = left_div_creation()

    # Right side screen
    right_parent_div = right_div_creation()

    # Div holding all the divs
    main_heading = webgen.make_header(1, "", "Data generated")
    outermost_div = webgen.make_div("", main_heading, left_parent_div, right_parent_div)

    # Adding all the parts together
    return outermost_div


def left_div_creation():
    ordered_list = ""
    if form["processed_based"] == "survey":
        ordered_list = webgen.make_ordered_list("", fill_the_list_survey())
    else:
        ordered_list = webgen.make_ordered_list("", fill_the_list_sat())
    # Div is the only one that can be scrolled
    left_parent_div_design = """float: left; width: 50vw; height: 88vh; overflow: scroll; border-right: 3px solid black"""

    left_parent_div_title = webgen.make_header(3, "", "Data generated for {} schools (scroll on this side of screen)".format(len(processed.sorted_sat)))
    return webgen.make_div(left_parent_div_design, left_parent_div_title, ordered_list)


def right_div_creation():
    right_parent_div_design = """float: left; width: 48vw; overflow: hidden; height: 88vh; padding-left: 5px"""
    right_parent_div_title = webgen.make_header(3, "", "General Data")
    return webgen.make_div(right_parent_div_design, right_parent_div_title, general_data())


def fill_the_list_sat():
    list = ""  # Includes paragraph and <list>
    # All new lines will be replaced with <br> (done automatically with webgen)
    section_names = ["SAT Amount of Test Takers: {0}\n", "SAT Reading Average: {1}\n", "SAT Math Average: {2}\n",
                     "SAT Writing Average: {3}\n", "SAT Combined Average: {4}\n"]
    section_labels = ['n', 'r', 'm', 'w', 't']  # Each one corresponds to section_names

    for school in processed.sorted_sat:
        # Naming of school
        naming_format = "{}<br>(DBN: {})".format(school[1], school[0])

        # Makes a paragraph description of the school
        paragraph = ""
        for index, section_name in enumerate(section_names):
            if section_labels[index] == processed.chosen_selection_sat:
                # Bold since this is what the user wants to see
                paragraph += webgen.make_bold(section_name)
            else:
                paragraph += section_name

        paragraph = paragraph.format(school[2], school[3], school[4], school[5], school[6])
        list += webgen.make_list("", naming_format, webgen.make_paragraph(paragraph))
    return list


def general_data():
    """Same for Survey and SAT
    Note that \n are going to be replaced with <br> in the webgen.make_paragraph"""
    # SAT overview
    section_names = ["SAT Amount of Test Takers: {} (Overall: {})\n", "SAT Reading Average: {} (Overall: {})\n",
                     "SAT Math Average: {} (Overall: {})\n", "SAT Writing Average: {} (Overall: {})\n",
                     "SAT Combined Average: {} (Overall: {})\n"]
    introduction_sat = "SAT Details:\nFor generating these numbers, we ignored schools that have less than six people who took the exam, they are noted by the score of 0\n\n"

    shown_average_intro = "Here are the averages for school(s) you selected:\n"
    sat_selected_grades = []
    for index in range(len(section_names)):
        sat_selected_grades.append(section_names[index].format(processed.sat_averages_selected[index], processed.sat_average[index]))

    # Survey overview
    info_survey = "The scale for score is 1 to 10 inclusive, with 10 being the best score (the group strongly agrees) \n"
    intro_survey = "Not all high schools that have students who took the SAT have survey results (if one doesn't in the list, correlation is 0), but here are some correlations (These correlations can be off since there are multiple factors affect SAT score. In addition the amount of students taking SATs in all high schools aren't a significant amount. These surveys also include teachers, students, and parents that are not associated with SAT score at all):\n\n"
    correlation = ""
    correlation_values = processed.survey_break_down()
    correlation_structure = "Correlation between SAT Scores and {}: {}\n"
    correlation_order = ["parent", "teacher", "student", "overall survey"]
    for index, values in enumerate(correlation_values):
        correlation += correlation_structure.format(correlation_order[index], values)

    # String concat is the easiest and most readable method
    message = introduction_sat + shown_average_intro + "".join(sat_selected_grades) + "\n\n" + intro_survey + correlation
    return webgen.make_paragraph(message)


def fill_the_list_survey():
    list = ""
    section_names = ["Safety and Respect Score: {}\n", "Communication Score: {}\n", "Engagement Score: {}\n",
                     "Academic Expectation Score: {}\n", "Overall Parents Score: {}\n", "Overall Teacher Score: {}\n",
                     "Overall Student Score: {}\n", "Overall Response Score: {}\n"]
    section_match = [8, 9, 10, 11, 5, 6, 7, 12]
    for school in processed.simplified_sorted_survey:
        naming_format = "{}<br>(DBN: {})".format(school[1], school[0])

        paragraph = ""
        for index, section_name in enumerate(section_names):
            if section_match[index] == processed.chosen_selection_survey:
                paragraph += webgen.make_bold(section_name.format(school[section_match[index]]))
            else:
                paragraph += section_name.format(school[section_match[index]])
        list += webgen.make_list("", naming_format, webgen.make_paragraph(paragraph))
    return list


def main():
    # Dictionary of inputs
    global form
    form = get_cgi_dict()

    error_handler()

    global any_error
    if any_error:
        return  # Stop everything, user must input correct data first

    '''Website building'''
    # Generates right side of page with static information
    # If user didn't choose survey option default to overall
    if "Survey_choice" not in form:
        form["Survey_choice"] = "overall"
    prepare_data_survey()
    prepare_data_sat()
    processed.better_name()  # Makes better school name based on dbn if available

    # Generation of body to pass into generate_webpage
    generate_webpage(body_generation())


main()

# debugging
if __name__ == "__main__":

    pass
