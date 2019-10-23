import re


def validate_input(choice, parameters):
    """
    Checks the user input, so that the program can run correctly.
    Choice is a string value.
    Parameters is a list of possible options.
    Returns void.
    """

    while choice not in parameters:
        print("Sorry, looks like you chose wrong, you fool! Please enter a valid choice.")
        print(parameters)
        choice = input()

    return choice


def strip_keys(inputted, to_strip):
    inputted = re.sub(to_strip, "", inputted)
    return inputted
