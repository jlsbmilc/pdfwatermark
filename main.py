import os
import tkinter as tk
import PyPDF2
from tkinter import Tk
from tkinter import filedialog
from time import sleep


def choose_file():
    dir_root = Tk()
    dir_root.withdraw()
    chosen_file = filedialog.askopenfilename()
    if chosen_file == "":
        print("No file chosen.")
        sleep(5)
        print("Do you want to quit? Type y/n.")
        choice = input(">")
        if choice.lower() == "y":
            quit()
        else:
            return choose_file()
    else:
        print(f"You chose a following file: {chosen_file}")
        sleep(5)
        return chosen_file
