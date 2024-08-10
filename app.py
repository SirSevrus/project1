import os
from libs.saveNotes import create
from datetime import datetime as dt

def createPdf():
    # Get the directory path from user input
    dirPath = input("Enter path of directory where the images are present >>> ")
    
    # Replace backslashes with forward slashes
    dirPath = dirPath.replace("\\", "/")
    
    # Print subjects list
    print("[1] Physics\n[2] Maths\n[3] Chemistry\n[4] English\n[5] Computer Science\n[6] Biology\n[7] Other")
    
    # Get the subject from user input
    subject = input('Enter Subject >')
    
    # Get the current date and format it
    date = dt.now().strftime("%d%m%Y")
    
    # Create the file name based on subject and date
    fileName = subject + date +'.pdf'
    
    # Example function call (make sure to adjust parameters as needed)
    create(fileName, dirPath)

createPdf()
