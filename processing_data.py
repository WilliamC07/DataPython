import data_analysis as analysis

# Global variables for readability
# SAT
processed_SAT = []
total_average = ["test_takers", "reading", "math", "writing", "overall"]  # Will be converted to numbers

# Survey

'''
Helper function:

initialize() --> generates all the global variables value
since I don't think we can use __init__()

read_file(file_path) --> gives the raw data of the file

'''


def initialize():
    read_SAT()


def read_file(file_path):
    file = open(file_path, 'r')
    information = file.readlines()
    file.close()
    return information


'''
SAT Functions
'''


def process_SAT(raw):
    for line in raw[1:]:  # Remove csv file column name
        data = ["DBN", "School name", "number of test takers",
                "reading", "math", "writing", "total average"]
        array = []

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
Class Size Functions
'''


# Bug testing
if __name__ == "__main__":
    initialize()
    print(processed_SAT)