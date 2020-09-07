
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfFileMerger        # merge_pdfs
import glob                             # merge_pdfs
from datetime import date, datetime     # merge_pdfs
import os                               # merge_pdfs
import webbrowser


def select_source():
    global pdf_source, lb, src_lab
    lb["text"] = "Ready to Merge"
    lb["foreground"] = "blue"
    pdf_source = filedialog.askdirectory()
    src_lab["text"] = str(pdf_source)


def select_destination():
    global pdf_destination, lb, des_lab
    pdf_destination = filedialog.askdirectory()
    des_lab["text"] = str(pdf_destination)
    lb["text"] = "Ready to Merge"
    lb["foreground"] = "blue"


def callback(url):
    webbrowser.open_new(url)




def scan_files():
    global f
    f = glob.glob(pdf_source + "/*.pdf")
    
def merge_pdfs():
    global pdf_destination, pdf_source, lb, f
    scan_files()
    if f:
        try:
            # ---------PDF MERGER-----------------
            merger = PdfFileMerger()
            for pdf in f:
                merger.append(pdf)

            file_name = "/merged"
            counter = 1
            while(os.path.isfile(pdf_destination + file_name + ".pdf")):
                file_name = "/merged_" + str(counter)
                counter += 1
                
            merger.write(pdf_destination + file_name + ".pdf")
            merger.close()

            print("PDF Merged to:\t\t\t" + pdf_destination + file_name + ".pdf")
            lb["text"] = "Success"
            lb["foreground"] = "green"
        except Exception as e:
            print(e)
    else:
        lb["text"] = "No PDF's Found"
        lb["foreground"] = "red"
        print("No PDF's Found")



if __name__ == '__main__':
    app = tk.Tk()
    app.title("PDF Merger")
    app.geometry("600x100")
    app.resizable(width=0, height=0)
    app.grid_columnconfigure((0, 1), weight=1)
    selected = tk.IntVar()

    pdf_source = "/"
    pdf_destination = "/"

    lb = tk.Label(app, text='Ready to Merge', foreground="blue", anchor="n")
    lb.grid(row=4, column=0, sticky=tk.W+tk.E)
    lb2 = tk.Label(app, text='By: Zyetta', anchor="n", foreground="lightblue")
    lb2.bind("<Button-1>", lambda e: callback("https://github.com/zyetta"))

    lb2.grid(row=4, column=1, sticky=tk.W+tk.E)

    # --------------Source-------------------
    src_lab = tk.Label(app, text=pdf_source, anchor="n")
    src_slc = tk.Button(app, text="PDF Location", command=select_source)

    # --------------Destination--------------
    des_lab = tk.Label(app, text=pdf_destination, anchor="n")
    des_slc = tk.Button(app, text="PDF Destination",
                        command=select_destination)

    # --------------Destination--------------
    pdf_mrg = tk.Button(app, text="Merge PDFs", command=merge_pdfs)

    src_slc.grid(row=0, column=0, sticky="ew")
    src_lab.grid(row=0, column=1)

    des_slc.grid(row=1, column=0, sticky="ew")
    des_lab.grid(row=1, column=1)

    pdf_mrg.grid(row=2, column=0, sticky="ew")

    app.mainloop()
