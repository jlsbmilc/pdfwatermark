import os
import tkinter as tk
from PyPDF2 import PdfFileWriter, PdfFileReader
from tkinter import Tk
from tkinter import filedialog
from time import sleep
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import re


def choose_file():

    """
    Creates a GUI enabling the user to choose a file to be watermarked.
    Returns a path.
    """
    dir_root = Tk()
    dir_root.withdraw()
    chosen_file = filedialog.askopenfilename()
    if chosen_file == "":
        print("No file chosen.")
        sleep(2)
        print("Do you want to quit? Type y/n.")
        choice = input(">")
        if choice.lower() == "y":
            quit()
        else:
            return choose_file()
    else:
        return chosen_file


def validate_isodate(date_string):
    """
    Function validates if a string parsed as argument is a valid ISO date format.
    Returns a boolean.
    """
    regex = r'^([0-9]{4})-?(1[0-2]|0[1-9])-?(3[01]|0[1-9]|[12][0-9])$'

    if re.compile(regex).match(date_string) is None:
        return False
    else:
        return True


def transfer_date():
    """
    Function adds an optional argument from the user - transfer date.
    Returns a string formatted as ISO date.
    """
    user_input = input("Please input the transfer date in ISO format \"YYYY-MM-DD\". If you don't want to put the date, press RETURN.\n>")

    if user_input != "":
        date_format_correct = validate_isodate(user_input)

        if date_format_correct:
            return user_input
        
        else:
            print("Incorrect input. Try again.")
            transfer_date()


def create_watermark(used_path,user_string):
    """
    Creates a watermark pdf file containing  optional info from the user.
    Later created watermark is merged with original pdf file.
    """
    chosen_date = transfer_date()
    if chosen_date:
        watermark_text = user_string+f", Data Przelewu: {chosen_date}"
    else:
        watermark_text = user_string
    outpath = os.path.join(used_path,"watermark.pdf")
    c = canvas.Canvas(outpath,bottomup=0)
    
    #Setting right border for A4 canvas, which is 595.35 points.
    #15 points of margin deducted from the total width.
    canvas_width = 595.35-15
    textwidth = c.stringWidth(watermark_text)
    #Text starting point is chosen for the string to fit the page
    text_start_position_x = canvas_width - textwidth

    textobj = c.beginText(text_start_position_x,20)
    textobj.setFillColor(colors.black)
    textobj.textLine(watermark_text)
    c.drawText(textobj)
    c.save()
    return outpath


def add_watermark():
    """
    Function opens the file chosen by the user,
    iterates through all pages of it and merges each page with watermark file.
    After merging completion it removes the watermark file and saves a copy
    of modified file.
    """
    user_file = choose_file()
    file_name = os.path.basename(user_file).replace(".pdf","")
    working_path = os.path.dirname(user_file)
    out_file_name = file_name+"_modified.pdf"
    output = os.path.join(working_path,out_file_name)
    watermark = create_watermark(working_path,file_name)
    with open(watermark, "rb") as f:
        watermark_obj = PdfFileReader(f)
        watermark_page = watermark_obj.getPage(0)

        input_pdf = user_file
        pdf_reader = PdfFileReader(open(input_pdf,"rb"))
        pdf_writer = PdfFileWriter()

        # Watermark all the pages
        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)

        with open(output, 'wb') as out:
            pdf_writer.write(out)

#remove a temporary watermark file
    os.remove(watermark)    


def main():

    keep_running = True

    while keep_running:
        add_watermark()
        incorrect_input = True
        user_response = input("Do you want to modify another file? y/n\n>")
        while incorrect_input:
            if user_response.lower() == "y":
                incorrect_input = False
                keep_running = True
            elif user_response.lower() == "n":
                incorrect_input = False
                keep_running = False
            else:
                print("Wrong input. Type y or n and press ENTER.")
                user_response = input(">")

    print("Program ended execution. Good bye.")
    sleep(2)


if __name__ == '__main__':
    main()