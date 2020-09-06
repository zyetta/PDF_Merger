from PyPDF2 import PdfFileMerger
import glob
from datetime import date, datetime
import os

f = glob.glob("./to_merge/*.pdf")
FILE_TIME = str(datetime.now().strftime("%Y-%b-%d_%H-%M-%S"))

if f:
    try:
        #---------CREATING DIRECTORY---------
        os.mkdir("./merged/" + FILE_TIME)

        #---------PDF MERGER-----------------
        merger = PdfFileMerger()
        for pdf in f:
            merger.append(pdf)
        merger.write("./merged/" + FILE_TIME + "/merged.pdf")
        merger.close()
        print("PDF Merged to:\t\t\t" + "./merged/" + FILE_TIME + "/merged.pdf")

        #---------MOVING SOURCES------------
        os.rename("./to_merge", "./merged/" + FILE_TIME + "/source")
        print("Source Files Moved to:\t\t" + "./merged/" + FILE_TIME + "/source")
    except Exception as e:
        print(e)
else:
    print("No PDF's Found")
try:
    os.mkdir("./to_merge")
except:
    pass