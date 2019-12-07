try:
    from re import sub
except [ImportError, ModuleNotFoundError] as e:
    print("There was an error importing a utility package. Exiting program.")
    exit(1)


def validate_input(choice, parameters):
    """
    Validates user input for a number of different selections.

    Parameters:
    -----------
    :param choice:
        Is what the user put selected to be validated.
    :param parameters:
        All of the possible valid selections the user can make.

    Returns:
    --------
    :return:
        The string value of the validated choice that the user made.
    """

    while choice not in parameters:
        print("Sorry, looks like you chose wrong, you fool! Please enter a valid choice.")
        print(parameters)
        choice = input()

    return choice


def strip_keys(inputted, to_strip):
    inputted = sub(to_strip, "", inputted)
    return inputted
