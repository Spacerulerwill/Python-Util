# helpful functions

from typing import Any, List
import time
import sys
from colorama import Fore, Back
from colorama import init as colorama_init
import os
import string
from pynput import keyboard
import random

colorama_init()

def clearLines(num):
    for i in range(num):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')

def validatedInput(msg:str, condition, datatype=str, err_msg:str=None) -> Any:
    '''
    Asks for input until a condition is met\n
    ---
    Arguments:
    * msg - The query to ask the user
    * condiition - The condition of the input, can be a function or a lambda function
    * datatype - The correct datatype for the input - optional
    * err_msg - An error message to display when user does not meet the condition - optional
    ---
    Return's data of type of parameter ```datatype```
    '''
    print(msg, end="")
    while True:
        try:
            choice = datatype(input())
            if condition(choice):
                break
            else:
                if err_msg != None:
                    print("Invalid Input! " + err_msg)
                print("Please try again: ", end="")
        except ValueError:
            print(f"Input must be of type: {datatype.__name__}. Please try again: ", end="")
    return choice

NUMERIC = "numeric"
BULLET = "bullet"

def selectOptions(msg:str, options:List[str], mode:str=NUMERIC, case_sensitive=False) -> Any:
    '''
    Function that creates a list of options for a user to select from\n
    ---
    Arguments:
    * msg - The query to ask the user
    * options - The list of possible options
    * mode - Either ```NUMERIC``` or ```BULLET``` (number list or bullet points) - if selecting
    ```NUMERIC``` the user must provide the index of the option, if using ```BULLET``` the user
    must provide the name of the option itself - defaults to ```NUMERIC```
    * case_sensitive - whether the input should be case_sensitive or not - defaults to ```False```
    ---
    Return's data of type of option selected. (```Any```)
    '''
    if mode != NUMERIC and mode != BULLET: raise ValueError(f"mode must either be NUMERIC or BULLET, not {mode}")

    #convert all options to strings
    options = [str(option) for option in options]

    if not case_sensitive:
        lowercase_options = [option.lower() for option in options]

    print(msg)
    for count, option in enumerate(options):
        if mode == NUMERIC:
            print(f"  {count+1}. {option}")
        else:
            print(f"  • {option}")

    print("Enter option: ", end="")

    while True:
        choice = input()
        if mode == NUMERIC:
            if not choice.isnumeric():
                print("Invalid Option! Please choose a valid index: ")
            else:
                num = int(choice)
                if 1 <= num <= len(options):
                    return options[num-1]
                else:
                    print(f"Option {num} does not exist!")
        else:
            if case_sensitive:
                if choice not in options:
                    print("Invalid Option! Please try again: ", end="")
                else:
                    return choice
            else:
                if choice.lower() not in lowercase_options:
                    print("Invalid Option! Please try again: ", end="")
                else:
                    return options[lowercase_options.index(choice.lower())]

def dropdownMenu(title, options, color=Back.WHITE):
    '''
    A function that creates a drop down menu the user can interact with via the up and down arrow keys
    and the enter button to submit
    '''
    indexSelected = 0  
    def draw():
        stringToPrint = title + "\n"
        for index, option in enumerate(options):
            if index == indexSelected:
                stringToPrint += f"  • {color}{Fore.BLACK}{option}{Back.BLACK}{Fore.WHITE}\n"
            else:
                stringToPrint += f"  • {option}\n"
        print(stringToPrint)

    def redraw():
        clearLines(len(options)+2)
        draw()
        
    draw()
    selectedOption = None
    def on_press(key):
        nonlocal selectedOption, indexSelected
        
        char_pressed = key

        keyboard.Key.down
        match char_pressed:
            case keyboard.Key.enter:
                selectedOption = options[indexSelected]
                return False
            case keyboard.Key.down:
                if indexSelected < len(options)-1:
                    indexSelected += 1
                    redraw()
            case keyboard.Key.up:
                if indexSelected > 0:
                    indexSelected -= 1
                    redraw()

    with keyboard.Listener(
        on_press=on_press) as listener:
        listener.join()

    return selectedOption

def scrollText(msg:str, speed:float=0.05, pause_chars:List[str]=[], pause_duration:float=0.25) -> None:
    '''
    A function that scroll prints out text\n
    ---
    Arguments:
    * msg - The message to scroll print
    * speed - the time between each char being printed
    * pause_chars - list of chars to pause for a longer period of time at - optional
    * pause_duration - how long to pause at each pause char - optional
    ---
    Return type: None
    '''

    msg = str(msg)

    if any(len(char) != 1 for char in pause_chars): raise ValueError("pause_chars must all have length 1")

    if len(pause_chars) == 0:
        for char in msg:
            sys.stdout.flush()
            print(char, end="")
            time.sleep(speed)
    else:
        for char in msg:
            sys.stdout.flush()
            print(char, end="")
            if char in pause_chars:
                time.sleep(pause_duration)
            else:
                time.sleep(speed)

if __name__ == "__main__":
    print("Random shit")
    random_options = [''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) for x in range(5)]
    choice = dropdownMenu("Select an Option", random_options)
    print(choice)