import data_analysis as analysis

# Global variables for readability
# SAT
processed_SAT = []
total_average = ["test_takers", "reading", "math", "writing", "overall"]  # Will be converted to numbers

# Survey
processed_survey = []

'''
Helper function:

initialize() --> generates all the global variables value
since I don't think we can use __init__()

read_file(file_path) --> gives the raw data of the file

'''


def initialize():
    read_SAT()
    read_survey()


def read_file(file_path):
    file = open(file_path, 'r')
    information = file.readlines()
    file.close()
    return information


def is_valid_school(dbn):
    """If the school didn't take the SAT then we don't care"""
    valid_school = False
    for school in processed_SAT:
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
            name_school += part_name + ","
        data[1] = name_school[:-2]  # Remove trailing comma
        processed_SAT.append(data)


def read_SAT():
    global processed_SAT
    processed_SAT = []

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
            data.append(rest_data)

        processed_survey.append(data)


def read_survey():
    global processed_survey
    processed_survey = []

    PATH = "Survey.csv"
    raw_data = read_file(PATH)
    process_survey(raw_data)


# Bug testing
if __name__ == "__main__":
    initialize()
    for item in processed_survey:
        print(len(item))