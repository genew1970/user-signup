
def alphabet_position(letter, rotate):
    # initialize the return message
    new_rot = ""

    # creates lower and upper alphabet variables
    low_alpha = "abcdefghijklmnopqrstuvwxyz"
    upper_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # checks to see if the character is upper or lower case and rotates
    # the character by the rotation
    if letter in low_alpha:
        new_rot = rotate_character(low_alpha.index(letter), rotate)
        new_rot = low_alpha[new_rot]
    elif letter in upper_alpha:
        new_rot = rotate_character(upper_alpha.index(letter), rotate)
        new_rot = upper_alpha[new_rot]

    # returns the final message
    return new_rot

def rotate_character(char, rot):

    newLetter = char + rot
    # there are 26 letters in the alphabet and the index
    # starts at zero so anything past 25 is returned to the
    # remainder of the equation following the test condition
    if newLetter >= 26:
        newLetter = (newLetter % 26)
    #print(char, rot, newLetter)
    return newLetter

def encrypt(text, rot):
    # initializes variables and takes the rot to lower case

    message_encrypt = ""

    # iterates through the loop through the entire message

    for i in text:
        if not i.isalpha():
            message_encrypt += i
        else:
            message_encrypt += alphabet_position(i, rot)

    return message_encrypt
