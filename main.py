#======================
# Setup
#======================
import csv
import os.path
import re
import tkinter as tk

from tkinter import ttk, filedialog, messagebox

imports  = dict()
imports['csv'] = []
exports  = dict()
configure = dict()
generate = dict()
headings = []

window = tk.Tk()
window.title("Email Generator")
window.config(background="#ebebeb")


#======================
# Functions
#======================
# Get file, contents optional
def getFile(file_type, file_extention, contents):
    template_location =  filedialog.askopenfilename(initialdir = "~/", title = "Select file", filetypes = ((file_type, file_extention), ("all files", "*.*")))

    if (contents):
        with open(template_location , 'r') as file:
            return file.read()
    else:
        return template_location


# Import files
def importHtml():
    imports['html_template'] = getFile("HTML files", "*.html", True)


def importCsv():
    imports['csv'] = dict()
    data = csv.reader(open(getFile("CSV files", "*.csv", False), 'r'))

    for rowKey, row in enumerate(data):
        # Heading Row
        if (len(headings) == 0):
            for heading in row:
                headings.append(heading)
                configure['filename_append_combo']['values'] = headings
                configure['filename_append_combo'].current(0)
            continue

        # Data Rows
        imports['csv'][rowKey] = dict()
        for key, value in enumerate(row):
            imports['csv'][rowKey][headings[key]] = value

        generate['count'].config(text=str(len(imports['csv'])) + " files")


# Export directory
def exportLocation():
    exports['directory'] = filedialog.askdirectory()
    exports['label'].config(text=exports['directory'])


# Preview filename
def previewFilename():
    configure['filename_example'].config(text=configure['filename'].get() + "{" + configure['filename_append'].get() + "}.html")


# Generate and export files
def generateFiles():
    if (imports['html_template'] is None):
        messagebox.showerror("Error", "No HTML imported")
        return

    if (len(imports['csv']) == 0):
        messagebox.showerror("Error", "No CSV imported")
        return

    if (exports['directory'] is None):
        messagebox.showerror("Error", "No export location set")
        return
        
    if (len(imports['csv'])):
        fileCount = 0

        for row in imports['csv']:
            template = imports['html_template'];

            for key in imports['csv'][row]:
                template = template.replace("{"+ key +"}", imports['csv'][row][key])

            try:
                # File name
                file = exports['directory'] + '/' + configure['filename'].get() + imports['csv'][row][configure['filename_append'].get()]

                # Add number if file exists
                i = 0
                while os.path.exists(file):
                    i += 1
                    file = file + "-" + str(i)

                # Create File
                file = open(file + ".html", "w+")
                file.write(template)
                file.close()

                fileCount += 1
            except Exception as error:
                messagebox.showerror("Error", "Error: " + str(error))

        messagebox.showinfo("Complete!", str(fileCount) + "/" + str(len(imports['csv'])) + " files created!")


#======================
# GUI
#======================
# Import Frame
imports['frame'] = ttk.LabelFrame(window, text="Import Files")
imports['frame'].grid(column=0, row=0, padx=10, pady=10, sticky='we')

imports['html_button'] = ttk.Button(imports['frame'], text="Import HTML", command=importHtml).grid(column=0, row=0, sticky='w')
imports['csv_button'] = ttk.Button(imports['frame'], text="Import CSV", command=importCsv).grid(column=1, row=0, sticky='w')


# Export Location Frame
exports['frame'] = ttk.LabelFrame(window, text="Export Location")
exports['frame'].grid(column=0, row=1, padx=10, pady=10, sticky='we')

exports['button'] = ttk.Button(exports['frame'], text="Open Directory", command=exportLocation).grid(column=0, row=0, sticky='w')

exports['label'] = ttk.Label(exports['frame'], text="...")
exports['label'].grid(column=0, row=1, padx="2", sticky='w')


# Configure Export Frame
configure['frame'] = ttk.LabelFrame(window, text="Configure Export")
configure['frame'].grid(column=0, row=2, padx=10, pady=10, sticky='we')

configure['filename_input_label'] = ttk.Label(configure['frame'], text="Enter a filename:")
configure['filename_input_label'].grid(column=0, row=0, padx="2", sticky='w')

configure['filename'] = tk.StringVar()
configure['filename_input'] = ttk.Entry(configure['frame'], textvariable=configure['filename'])
configure['filename_input'].grid(column=0, row=1, sticky='w')

configure['filename_append_label'] = ttk.Label(configure['frame'], text="Select a heading:")
configure['filename_append_label'].grid(column=1, row=0, padx="2", sticky='w')

configure['filename_append'] = tk.StringVar()
configure['filename_append_combo'] = ttk.Combobox(configure['frame'], textvariable=configure['filename_append'])
configure['filename_append_combo']['values'] = headings
configure['filename_append_combo'].grid(column=1, row=1, sticky='w')\

configure['filename_example'] = ttk.Label(configure['frame'], text="")
configure['filename_example'].grid(column=0, row=2, padx="2", sticky='w')

configure['button'] = ttk.Button(configure['frame'], text="Preview", command=previewFilename).grid(column=0, row=3, sticky='w')


#  Export Frame
generate['frame'] = ttk.LabelFrame(window, text="Export Files")
generate['frame'].grid(column=0, row=3, padx=10, pady=10, sticky='we')

generate['button'] = ttk.Button(generate['frame'], text="Generate Files", command=generateFiles).grid(column=0, row=0, sticky='w')

generate['count'] = ttk.Label(generate['frame'], text=str(len(imports['csv'])) + " files")
generate['count'].grid(column=1, row=0, sticky='e')

#--------------------------------------------
# Main Loop
#--------------------------------------------
window.mainloop()