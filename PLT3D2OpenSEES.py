import csv
import pandas as pd
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
import os

window5 = tk.Tk()
window5.title("BNDF to OpenSEES")
window5.geometry("400x300")


# this is a frame for the entries of files and options for the user to chose the devices
frame1 = tk.LabelFrame(window5, text="Basic Inputs", padx=5, pady=5)
frame1.grid(row=0, column=0, sticky="nsew")


def createFolder(directory):  # creating folders in the directory
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating Directory.' + directory)


def location():  # define location of the current directory
    global location
    get = filedialog.askdirectory()
    os.chdir(get)


loc_button = tk.Button(frame1, text="Directory", command=location, width=15, height=1).grid(row=0, column=1, padx=10,pady=10)
getloc = tk.Label(frame1, width=20, text="Get Working Directory", anchor='e').grid(row=0, column=0, padx=5, pady=5)

sim_time = tk.Entry(frame1, width=10)
sim_time.grid(row=1, column=1)
sim_time.insert(tk.END, "300")
stLabel = tk.Label(frame1, width=20, text="Time of Simulation", anchor='e').grid(row=1, column=0)

dT = tk.Entry(frame1, width=10)
dT.grid(row=2, column=1)
dT.insert(tk.END, "10")
dTLabel = tk.Label(frame1, width=20, text="Time interval", anchor='e').grid(row=2, column=0)

no_Devc = tk.Entry(frame1, width=10)
no_Devc.grid(row=3, column=1)
no_Devc.insert(tk.END, "5")
no_DevcLabel = tk.Label(frame1, width=20, text="Number of Devices", anchor='e').grid(row=3, column=0)

TIME = []

def output():
    createFolder('./Header/')
    createFolder("./Header/Values/")
    createFolder("./Header/Values/DAT")
    createFolder("./Header/Values/DAT/OpenSEES")
    global TIME
    time = int(dT.get())
    while time <= int(sim_time.get()):
        newTime = time
        time += int(dT.get())
        TIME += [newTime]
    # make a column from the list
    outfile = open("Time.csv", 'w', newline='')
    out = csv.writer(outfile)
    out.writerows(map(lambda x: [x], TIME))
    outfile.close()
    fName = []  # making a list of all files comes from the FDS2ASCII
    iT = 1
    n = (int(sim_time.get())*int(no_Devc.get())/int(dT.get()))   # it will give the total number of files

    '''The name of the files should be the same as generated by BNDF script '''

    while iT <= n:
        file = 'test{}.csv'.format(iT)
        fName += [file]
        iT += 1

    r = 1
    while r <= n:
        for fname in fName:
            with open("Header/FDS{}.csv".format(r), 'w') as outfile:
                with open(fname) as infile:
                    next(infile)
                    next(infile)
                    csv.reader(infile, quoting=csv.QUOTE_NONNUMERIC)
                    for lines in infile:
                        outfile.writelines(lines)
            r += 1

    CSV = []  # making the list of files after removing the headers from the file
    k = 1
    while k <= n:  # for all files
        f1 = 'Header/FDS{}.csv'.format(k)
        CSV += [f1]
        k += 1

    s = 1
    t = (int(sim_time.get())*int(no_Devc.get())/int(dT.get()))

    while s <= t:
        for p1 in CSV:
            with open("Header/Values/FDS{}.csv".format(s), 'w') as out:
                wtr = csv.writer(out, delimiter=' ', quoting=csv.QUOTE_NONNUMERIC)
                with open(p1, newline='') as go:
                    thirdColumn = [line.split(',')[7] for line in go]  # keeping only the 4th column as
                    # first three columns contains the coordinates data
                    wtr.writerow(thirdColumn)
            s += 1

    #################################################################################################
    '''combining all data from the files in one file (one more inside code in needed to achieve limited 
        number of files based on  time and sample size'''

    listF = []  # list of all files after removing coordinates data
    i1 = 1

    while i1 <= n:
        file1 = 'Header/Values/FDS{}.csv'.format(i1)
        listF += [file1]
        i1 += 1

    # number of files taken in one time will depends upon simulation time and time interval
    '''Below is the list of all files, where each item has sub-list of all items at one location with total time history'''
    tt1 = int(sim_time.get())
    ti1 = int(dT.get())

    allFilesList = [listF[x:x+int(tt1/ti1)] for x in range(0, len(listF), int(tt1/ti1))]

    jB = 1
    while jB <= int(no_Devc.get()):
        for i in allFilesList:
            oneFile = "Header/Values/AST{}.csv".format(jB)
            with open(oneFile, 'w') as outf1:
                for k in i:
                    with open(k) as infile:
                        data = csv.reader(infile, quoting=csv.QUOTE_NONNUMERIC)
                        for lines in data:
                            outf1.writelines(lines)

            # making file in Time and Temperature history
            df1 = pd.read_csv("Time.csv")
            df2 = pd.read_csv("Header/Values/AST{}.csv".format(jB))

            result = pd.concat([df1, df2], axis=1, sort=False)  # join two columns
            result.to_csv("Header/Values/ASTX{}.csv".format(jB), mode='w', index=False)

            # converting files to DAT format
            inputPath = "Header/Values/ASTX{}.csv".format(jB)
            outputPath = "Header/Values/DAT/AST{}.dat".format(jB)

            with open(inputPath) as inputFile:
                with open(outputPath, 'w', newline='') as outputFile:
                    reader = csv.DictReader(inputFile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
                    writer = csv.DictWriter(outputFile, reader.fieldnames, delimiter=' ')
                    writer.writeheader()
                    writer.writerows(reader)

            jB += 1

    # adding first line at time 0
    m = 1
    while m <= int(no_Devc.get()):
        f = open('Header/Values/DAT/AST{}.dat'.format(m), 'r')
        newF = open('Header/Values/DAT/OpenSEES/AST{}.dat'.format(m), 'w')
        lines = f.readlines()  # read old content
        newF.write("0.0 20.0\n")  # write new content at the beginning
        for line in lines:  # write old content after new
            newF.write(line)
        newF.close()
        f.close()
        m += 1


crete_Button = tk.Button(window5, text="Save File", command=output, width=15, height=1).grid(row=2, column=0, padx=5, pady=5)

window5.mainloop()

