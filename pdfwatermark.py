import os
import tkinter as tk
from PyPDF2 import PdfFileWriter, PdfFileReader
from tkinter import Tk
from tkinter import filedialog
from time import sleep
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def choose_file():
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
        sleep(2)
        chosen_file = chosen_file.replace("/","\\\\")
        print(f"You chose a following file: {chosen_file}")
        return chosen_file


def transfer_date():
    user_transfer = input("Please input the transfer date in ISO format \"YYYY-MM-DD\". If you don't want to put the date, press RETURN.\n>")
    if user_transfer != "":
        return user_transfer
        

def create_watermark(used_path,user_string):
    chosen_date = transfer_date()
    if chosen_date:
        string_full = user_string+f", Data Przelewu: {chosen_date}"
    else:
        string_full = user_string
    outpath = os.path.join(used_path,"watermark.pdf")
    c = canvas.Canvas(outpath,bottomup=0)
    textobj = c.beginText(50,50)
    textobj.setFillColor(colors.black)
    textobj.textLine(string_full)

    c.drawText(textobj)
    c.save()
    return outpath

def add_watermark():
    user_file = choose_file()
    file_name = os.path.basename(user_file).replace(".pdf","")
    working_path = os.path.dirname(user_file)
    out_file_name = file_name+"_modified.pdf"
    output = os.path.join(working_path,out_file_name)
    print(f"Used output path: {output}")
    watermark = create_watermark(working_path,file_name)
    sleep(2)
    with open(watermark, "rb") as f:
        watermark_obj = PdfFileReader(f)
        watermark_page = watermark_obj.getPage(0)

        input_pdf = user_file
        pdf_reader = PdfFileReader(open(input_pdf,"rb"))
        print(f"Source file to be modified: {input_pdf}")
        sleep(2)
        pdf_writer = PdfFileWriter()

        # Watermark all the pages
        for page in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page)
            page.mergePage(watermark_page)
            pdf_writer.addPage(page)

        with open(output, 'wb') as out:
            pdf_writer.write(out)

    os.remove(watermark)    

if __name__ == 'main':
    add_watermark()

add_watermark()