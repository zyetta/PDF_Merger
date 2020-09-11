import glob
import tkinter as tk
import webbrowser
from functools import partial
from tkinter import filedialog
from PyPDF2 import PdfFileMerger
import os
from operator import itemgetter


# Golobal Parameters
EXT = {
    "PDF": "pdf",
}
EXTENSION = "pdf"
des_file_dir = r"C:/Users"
src_file_dir = r"C:/Users"
found_files = ""
text_variable = []
# --------------------------------------------------------------------------------------
#   Description: Scans for all files of a certain extension in a certain directory
#
#   src:        Source Files directory
#   ext:        Extension of files to scan
#
#   return:     Array of files w/ extensions
# --------------------------------------------------------------------------------------


def scan_files():
    global found_files, src_file_dir, EXTENSION, scan_lab
    found_files = glob.glob(src_file_dir + "/*." + str(EXTENSION))
    scan_lab["text"] = str(len(found_files)) + " File(s) Found"
    if(len(found_files) <= 0):
        scan_lab["fg"] = "red"
    else:
        scan_lab["fg"] = "black"

# --------------------------------------------------------------------------------------
#   Description: Selects a file directoy
#
#   return:     Returns character string of directory to be processed
# --------------------------------------------------------------------------------------


def slc_dir(type):
    global des_file_dir, src_file_dir, des_file_dir, src_lab, des_lab, merge_status
    merge_status["text"] = "Ready To Merge"
    merge_status["fg"] = "blue"
    hold = filedialog.askdirectory()
    if((type == 1) & (hold != "")):
        des_file_dir = hold
        des_lab["text"] = des_file_dir
    elif((type == 0) & (hold != "")):
        src_file_dir = hold
        src_lab["text"] = src_file_dir
    else:
        merge_status["text"] = "An Error Occured with the Selection"
        merge_status["fg"] = "red"


# --------------------------------------------------------------------------------------
#   Description: Selects a file extension with the modification of a global parameter
#
#   return:
# --------------------------------------------------------------------------------------


def slc_ext():
    global EXTENSION
    EXTENSION = str(hold_var.get())
    fname_lab["text"] = "." + str(EXTENSION)
    merge_status["text"] = "Ready To Merge"
    merge_status["fg"] = "blue"


def callback(url):
    webbrowser.open_new(url)


def merge_pdfs():
    global EXTENSION, des_file_dir, src_file_dir, des_file_dir, src_lab, des_lab, merge_status, file_name, found_files

    if found_files:
        try:
            # ---------PDF MERGER-----------------
            merger = PdfFileMerger()
            for f in found_files:
                merger.append(f)
            fn = str(file_name.get())
            if(not fn):
                file_name_hold = "/merged"
            else:
                file_name_hold = "/" + fn
            i = 1

            while(os.path.isfile(des_file_dir + file_name_hold + ".pdf")):
                if(file_name == ""):
                    file_name_hold = "/merged_" + str(i)
                else:
                    file_name_hold = "/" + fn + "_" + str(i)
                i += 1

            merger.write(des_file_dir + file_name_hold + ".pdf")
            merger.close()

            print("PDF Merged to:\t\t\t" + file_name_hold + ".pdf")
            merge_status["text"] = "Success - " + \
                str(len(found_files)) + " Files Merged to " + \
                str(file_name_hold) + ".pdf"
            merge_status["foreground"] = "green"
        except Exception as e:
            print(e)
            merge_status["text"] = e
            merge_status["foreground"] = "red"
    else:
        merge_status["text"] = "No " + str(EXTENSION) + "'s  Found"
        merge_status["foreground"] = "red"
        print("No PDF's Found")


def rearrange_files():
    global found_files, text_variable
    newWindow = tk.Toplevel(window)
    newWindow.title("Rearrange")

    j = 0
    text_variable = []
    for i in range(len(found_files)):
        text_variable.append(tk.IntVar(master=newWindow, value=(j+1), name=str(j)))
        j += 1

    tk.Label(master=newWindow, text="Found Files", fg="black").grid(
        column=0, row=0, sticky="w", padx=pad_x*2, pady=pad_y*2)
    file_item = tk.Frame(master=newWindow)
    j = 0
    for i in found_files:
        spin_box = tk.Spinbox(master=file_item, from_=1,
                              to=100, increment=1, textvariable=text_variable[j])
        spin_box.grid(column=0, row=j, sticky="w", padx=pad_x*2, pady=pad_y*2)
        tk.Label(master=file_item, text=i, fg="black").grid(
            column=1, row=j, sticky="w", padx=pad_x*2, pady=pad_y*2)
        j += 1
    file_item.grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky="w")

    tk.Button(master=newWindow, text="Save",
                         width=10, height=1, fg="black", command=partial(save_order, newWindow)).grid(row=2, column=0, padx=pad_x, pady=pad_y, sticky="w")

def save_order(a):
    global found_files
    j = 0
    final = []
    buffer = []
    for i in text_variable:
        buffer.append([i.get(), found_files[j]])
        j+=1
    buffer = sorted(buffer, key=itemgetter(0))
    
    for i in range(len(buffer)):
        final.append(buffer[i][1])
    found_files = final
    a.destroy()





# --------------------------------------------------------------------------------------
#   GUI User Interface
# --------------------------------------------------------------------------------------
pad_x = 5
pad_y = 3

if __name__ == "__main__":
    window = tk.Tk()
    window.title("PDF Merger")
    window.resizable(width=0, height=0)

    # -----------------------------Source-----------------------------

    src_frm = tk.Frame(master=window)
    src_dir = tk.Button(master=src_frm, text="Source Files",
                        width=10, height=1, fg="black", command=partial(slc_dir, 0))
    src_lab = tk.Label(master=src_frm, text=str(src_file_dir), fg="black")
    src_dir.grid(row=0, column=0, sticky="e")
    src_lab.grid(row=0, column=1, sticky="w")

    src_frm.grid(row=0, column=0, padx=pad_x, pady=pad_y, sticky="w")

    # -----------------------------Destination------------------------

    des_frm = tk.Frame(master=window)
    des_dir = tk.Button(master=des_frm, text="Destination",
                        width=10, height=1, fg="black", command=partial(slc_dir, 1))
    des_lab = tk.Label(master=des_frm, text=str(des_file_dir), fg="black")
    des_dir.grid(row=0, column=0, sticky="e")
    des_lab.grid(row=0, column=1, sticky="w")
    des_frm.grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky="w")

    # -----------------------------Extension--------------------------
    ext_frm = tk.Frame(master=window)
    hold_var = tk.StringVar(window, "pdf")
    ext_lab_frm = tk.LabelFrame(master=ext_frm, text="Select Extension")

    i = 0

    for (a, b) in EXT.items():
        tk.Radiobutton(master=ext_lab_frm, text=a, variable=hold_var, value=b, command=slc_ext).grid(
            row=int(i/4 + 1), column=i % 4, sticky="w")
        i += 1

    ext_lab_frm.grid(row=0, column=0, padx=pad_x, pady=pad_y)
    ext_frm.grid(row=2, column=0, padx=pad_x, pady=pad_y, sticky="ew")

    # -----------------------------File Name--------------------------
    file_name = tk.StringVar()
    fn_frm = tk.Frame(master=window)

    fn_lab_frm = tk.LabelFrame(
        master=fn_frm, text="Filename (Leave blank for Default)")

    tk.Entry(master=fn_lab_frm, width=15, textvariable=file_name).grid(
        column=0, row=0, sticky="w", padx=pad_x*2, pady=pad_y*2)

    fname_lab = tk.Label(master=fn_lab_frm, text="." +
                         str(EXTENSION), fg="black")
    fname_lab.grid(column=1, row=0, sticky="w", padx=pad_x*2, pady=pad_y*2)

    fn_lab_frm.grid(row=0, column=0, padx=pad_x, pady=pad_y)
    fn_frm.grid(row=3, column=0, padx=pad_x, pady=pad_y, sticky="ew")

    # -----------------------------Scan Files-------------------------------
    scn_frm = tk.Frame(master=window)

    scn_lab_frm = tk.LabelFrame(
        master=scn_frm, text="File Management")

    scan_but = tk.Button(master=scn_lab_frm, text="Scan for Files",
                         width=10, height=1, fg="black", command=scan_files)
    scan_but.grid(column=0, row=0, sticky="w", padx=pad_x, pady=pad_y)

    scan_lab = tk.Label(master=scn_lab_frm, text="0 File(s) Found",
                        anchor="e", justify=tk.LEFT)
    scan_lab.grid(column=1, row=0, sticky="e", padx=pad_x, pady=pad_y)

    scan_order = tk.Button(master=scn_lab_frm, text="Rearrange",
                           width=10, height=1, fg="black", command=rearrange_files)

    scan_order.grid(column=0, row=0, sticky="w", padx=pad_x, pady=pad_y)
    scan_order.grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky="ew")
    scn_lab_frm.grid(row=0, column=0, padx=pad_x, pady=pad_y, sticky="ew")
    scn_frm.grid(row=4, column=0, padx=pad_x, pady=pad_y, sticky="ew")

    # -----------------------------Merge-------------------------------
    merge_frm = tk.Frame(master=window)

    merg_but = tk.Button(master=merge_frm, text="Merge",
                         width=10, height=1, fg="black", command=merge_pdfs)
    merg_but.grid(column=0, row=0, sticky="w", padx=pad_x, pady=pad_y)

    merge_status = tk.Label(master=merge_frm, text="Hello World",
                            anchor="e", justify=tk.LEFT)
    merge_status.grid(column=1, row=0, sticky="e", padx=pad_x, pady=pad_y)

    aknow = tk.Label(merge_frm, text='By: Zyetta',
                     anchor="n", foreground="blue")
    aknow.bind("<Button-1>", lambda e: callback("https://github.com/zyetta"))
    aknow.grid(row=1, column=0, sticky=tk.W+tk.E)
    merge_frm.grid(row=5, column=0, padx=pad_x, pady=pad_y, sticky="sw")

    window.mainloop()
