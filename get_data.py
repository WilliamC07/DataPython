import data_analysis as analysis

# Global variables for readability
# SAT
sat = []

# Survey
survey = []

#DBN
dbn_dictionary = dict()

'''
Helper function:

initialize() --> generates all the global variables value
since I don't think we can use __init__()

read_file(file_path) --> gives the raw data of the file

'''


def initialize():
    read_SAT()
    read_survey()
    read_dbn()


def read_file(file_path):
    file = open(file_path, 'r')
    information = file.readlines()
    file.close()
    return information


def is_valid_school(dbn):
    """If the school didn't take the SAT then we don't care"""
    valid_school = False
    for school in sat:
        if school[0] == dbn:
            valid_school = True
    return valid_school


'''
SAT Functions
'''


def process_SAT(raw):
    for line in raw[1:]:  # Remove csv file column name
        data = ["DBN", "School name", "number of test takers",
                "reading", "math", "writing", "total average"]

        # Clean up reading file
        line = line.replace("\n", "")
        array = line.split(",")

        # Schools with missing data (less than or equal to 5 test takers)
        if array[-1] == 's':
            data[-5:] = [0, 0, 0, 0, 0]
        else:
            data[-5: -1] = array[-4:]
            # Average of sat scores (this function requires integer input)
            data[-1] = analysis.mean([int(x) for x in data[-4:-1]])

        # School code doesn't need processing
        data[0] = array[0]

        # Fix school name to include comma
        name_school = ""
        for part_name in array[1:-4]:
            name_school += part_name + ","  # No need for ", " since .split only removes "," and not white space
        data[1] = name_school[:-2]  # Remove trailing comma
        sat.append(data)


def read_SAT():
    global sat
    sat = []

    PATH = "SAT.csv"
    raw_data = read_file(PATH)
    process_SAT(raw_data)


'''
Survey functions
'''


def process_survey(raw):
    """Note that not all schools have their survey results posted"""
    for line in raw[1:]:
        data = ["DBN"]

        array = line.split(",")
        if len(array) < 27:
            continue  # Invalid school data
        if not is_valid_school(array[0]):
            # Skips school that didn't take the SAT or we don't have the data for
            continue
        else:
            data[0] = array[0]

        # Generates school name in case there is a comma in the name
        school_name = ""
        for part in array[1:-25]:
            school_name += part+", "
        data.append(school_name[:-2])  # Removes trailing comma and space

        for rest_data in array[-25:]:
            data.append(rest_data.strip())
        survey.append(data)


def read_survey():
    global survey
    survey = []

    PATH = "Survey.csv"
    raw_data = read_file(PATH)
    process_survey(raw_data)


'''
DBN
'''

def read_dbn():
    global dbn_dictionary
    dbn_dictionary = dict()

    PATH = "dbn_to_name.csv"
    information = read_file(PATH)
    for school in information[1:]:
        # csv file only has 1 comma separated value
        dbn_value = school[0:6]
        school_name = school[7:].strip()
        dbn_dictionary[dbn_value] = school_name


# Bug testing
if __name__ == "__main__":
    initialize()
    pass
