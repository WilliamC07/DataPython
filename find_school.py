"""
Given user input, find school name closest to it.
If no schools found, return None
"""
import processing_data as data  # Yes I can get value from main.py, but it will make code hard to understand


# Removes "useless" symbols (comma, whitespace...)
def clean_name(input):
    input = input.strip();
    input = input.replace(",", "")
    input = input.replace(".", "")
    input = input.lower()
    return input


def comparison(base, new):
    # Makes sure the first two letters are the same and user gave enough letters
    if base[:2] == new[:2] and len(new) > 4:
        same = 0
        for letter in base:
            if letter in new:
                new.replace(letter, "", 1)
                same += 1

        # Percentage of similar characters
        return float(same) / float(len(base))
    else:
        return 0


def find_school(input):
    data.read_SAT()  # Don't need to run initialize since we only care about schools that took the SAT

    # See if person enter DBN name
    if input[0].isdigit():  # [0] instead of [0:2] in case someone just types random stuff
        # If school doesn't exist in SAT file, then we don't care
        schools = data.processed_SAT
        for school in schools:
            if school[0] == input:
                return [input] # Must be an array since other half of function returns array
        return None  # No school found (you should expect None when coding)
    else:
        '''
        Calculate the percent similar between input and actual school name
        Will always generate a name (Don't want to do percent in case a school in csv is named weirdly
        
        Csv file is corrupt and is missing some letters  :(
        '''
        # Clean up user input
        input = clean_name(input)

        # Schools whose name are close
        percent = 0
        schools = []

        for school in data.processed_SAT:
            name = clean_name(school[1])
            percent_similar = comparison(name, input)
            if percent_similar == percent:
                schools.append(school[0])  # Want to add the DBN value instead of school name
            elif percent_similar > percent:
                schools = [school[0]]
                percent = percent_similar

            #print("percent: {} name: {}".format(percent, name))

        schools.append(percent)  # Informs user how similar the names are
        if percent <= .3:  # No school fits it using my algorithm of finding names (arbitrary value)
            return None

        return schools


# Debugging purposes
if __name__ == "__main__":
    print(find_school("08X378"))
    pass
