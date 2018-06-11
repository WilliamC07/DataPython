import get_data as data
import data_analysis as analysis
import random

# Read the files
data.initialize()

# It is called sorted, but can be random
sorted_sat = []
sat_average = [0, 0, 0, 0, 0]
sat_averages_selected = [0, 0, 0, 0, 0]
sorted_survey = []
simplified_sorted_survey = []
dbn_dict = data.dbn_dictionary
chosen_selection_sat = ""
chosen_selection_survey = 0
copy_sat = []
copy_survey = []


def _sort(direction, list, index_comparison):
    """
    Using quick sort algorithm
    Direction: 'i' for increasing, 'd' for decreasing
    """
    if len(list) <= 1:
        return list
    else:
        pivot = float(list[0][index_comparison])

        left = []
        right = []
        for element in list[1:]:
            comparison = float(element[index_comparison])
            if comparison > pivot:
                right.append(element)
            else:
                left.append(element)

        # Check for increasing or decreasing order
        right_sort = _sort(direction, right, index_comparison)
        left_sort = _sort(direction, left, index_comparison)
        if direction == "d":
            return right_sort + [list[0]] + left_sort
        else:
            return left_sort + [list[0]] + right_sort


def _average_precise(list, index):
    """Finds average of a certain index in a matrix removing all values that are equal to 0"""
    items = []
    for item in list:
        if int(item[index]) != 0:
            items.append(int(item[index]))
    if len(items) == 0:
        return 0
    else:
        return analysis.mean(items)


def _randomize_list(list):
    # shuffle modifies the variable input; function itself returns None.
    random.shuffle(list)
    return list


def _fix_name(list):
    for index, school in enumerate(list):
        if school[0] in data.dbn_dictionary:
            list[index][1] = data.dbn_dictionary[school[0]]
    return list


def better_name():
    global sorted_sat
    sorted_sat = _fix_name(sorted_sat)
    global simplified_sorted_survey
    simplified_sorted_survey = _fix_name(simplified_sorted_survey)


def amount_limiter(type, max):
    """type: 'sat' or 'survey'"""
    # Before lost of data calculate some parts
    global sorted_sat
    global simplified_sorted_survey
    global copy_sat
    global copy_survey
    copy_sat = sorted_sat[:]
    copy_survey = simplified_sorted_survey[:]

    if type == "sat":
        sorted_sat = sorted_sat[0:max]
    elif type == 'survey':
        simplified_sorted_survey = simplified_sorted_survey[0:max]


def sort_sat(direction, section, list=data.sat):
    """
    Section: 'n': number of test takers, 'r': reading, 'm': math, 'w': writing, 't': total
    Direction: 'i': increasing, 'd': decreasing
    """
    global sorted_sat
    section_index_dict = {'n': 2, 'r': 3, 'm': 4, 'w': 5, 't': 6}
    sorted_sat = _sort(direction, list, section_index_dict[section])
    global chosen_selection_sat
    chosen_selection_sat = section


def randomize_sat():
    global sorted_sat
    sorted_sat = _randomize_list(data.sat)


def certain_SAT(schools, section):
    global sorted_sat
    dbns = schools[0]
    for school in data.sat:
        if school[0] in dbns:
            sorted_sat.append(school)
    sort_sat('d', section, sorted_sat)


def calculate_averages():
    global sat_average
    global sat_averages_selected
    index = 0
    while index < 5:
        sat_average[index] += _average_precise(data.sat, index + 2)
        sat_averages_selected[index] += _average_precise(sorted_sat, index + 2)
        index += 1


'''
Survey section
'''


def initialize_survey():
    global sorted_survey
    global simplified_sorted_survey
    sorted_survey = data.survey
    simplify_survey()


def sort_survey(direction, section):
    global sorted_survey
    global simplified_sorted_survey
    global chosen_selection_survey

    simplified_sorted_survey = _sort(direction, simplified_sorted_survey, section)
    chosen_selection_survey = section


def simplify_survey():
    global sorted_survey
    global simplified_sorted_survey
    simplified_sorted_survey = []
    '''
    simplified_sorted_survey - basically removes/simplify parts
    Each list contains these elements
    0. dbn
    1. school name
    
    2. parent response rate *note the switch from original
    3. teacher
    4. student *note the switch from orginal
    
    5. overall parent
    6. teacher
    7. student
    
    8. safety
    9. communication
    10. engagement
    11. academic expectation
    12. overall 8 through 11 inclusive
    '''
    for raw in sorted_survey:
        hold = [None for _ in range(13)]  # To make length 12
        hold[:2] = raw[:2]
        hold[2] = float(raw[4])
        hold[3] = float(raw[3])
        hold[4] = float(raw[2])
        hold[5] = analysis.mean([float(x) for x in raw[11:15]])
        hold[6] = analysis.mean([float(x) for x in raw[15:19]])
        hold[7] = analysis.mean([float(x) for x in raw[19:23]])
        hold[8:12] = [float(x) for x in raw[23:]]
        hold[12] = analysis.mean([float(x) for x in hold[8:12]])
        simplified_sorted_survey.append(hold)


def randomize_survey():
    global sorted_survey
    sorted_survey = _randomize_list(sorted_survey)
    simplify_survey()


def _match_from_survey(dbn):
    global copy_sat
    for school in copy_sat:
        if school[0] == dbn and school[-1] != 0:
            return school[-1]  # Returns total score
    return 0  # No matching found


def survey_break_down():
    global copy_survey
    global copy_sat
    """Arranging to allow for correlation between survey group response and overall grade"""
    correlate = [[], [], [], [], []]
    # Since there are less survey than sat, we will use survey as reference
    for school in copy_survey:
        score = _match_from_survey(school[0])
        if score != 0:
            correlate[0].append(score)
            correlate[1].append(school[5])
            correlate[2].append(school[6])
            correlate[3].append(school[7])
            correlate[4].append(school[12])

    # Find correlation between [0] and [1:]
    correlate[1] = analysis.correlation(correlate[0], correlate[1])
    correlate[2] = analysis.correlation(correlate[0], correlate[2])
    correlate[3] = analysis.correlation(correlate[0], correlate[3])
    correlate[4] = analysis.correlation(correlate[0], correlate[4])

    return correlate[1:]  # First item is useless now


# Debugging purposes
if __name__ == "__main__":
    initialize_survey()
    simplify_survey()
    sort_survey('d', -1)
    certain_survey([["02M475"]], '3')
    print(simplified_sorted_survey)
    pass
