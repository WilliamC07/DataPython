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


def letter_occurrence(input):
    input_letters = dict()
    for letter in input:
        if letter not in input_letters:
            input_letters[letter] = 1
        else:
            input_letters[letter] += 1
    return input_letters


def percent_similar(dict_base, dict_new):
    pass

def find_school(input: str):
    # See if person enter DBN name
    if input[0].isdigit(): #  [0] instead of [0:2] in case someone just types random stuff
        # If school doesn't exist in SAT file, then we don't care
        schools = data.processed_SAT
        for school in schools:
            if school[0] == input:
                return input
        return None  # No school found (you should expect None when coding)
    else:
        '''
        Calculate the percent similar between input and actual school name
        Will always generate a name (Don't want to do percent in case a school in csv is named weirdly
        
        Doesn't include 'i' because the csv file is corrupt and is missing some 'i'  :(
        '''
        # Clean up user input
        input = clean_name(input)

        # Get amount of times a letter appears to compare
        input_letters = letter_occurrence(input)


        # Schools whose name are close
        percent = 0
        schools = []

        for school in data.processed_SAT:
            school_letters = letter_occurrence(school[1])



