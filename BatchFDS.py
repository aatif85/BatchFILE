try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
import os

window4 = tk.Tk()
window4.title("Batch File Maker")
window4.geometry("1100x600")
# this is a frame for the entries of files and options for the user to chose the devices
frame1 = tk.LabelFrame(window4, text="Basic Inputs", relief=tk.SUNKEN)
frame1.grid(row=0, column=0, sticky="nsew")


def location():  # Directory Location
    get = filedialog.askdirectory()
    os.chdir(get)


tk.Button(frame1, text="Directory", command=location, width=15, height=1).grid(row=0, column=1)
tk.Label(frame1, width=20, text="Get Working Directory", anchor='e').grid(row=0, column=0, padx=5, pady=5)

# dropbox for the structural components
data = ["Columns", "Longitudinal Beams", "Transverse Beams", "Slabs"]
clicked6 = tk.StringVar()
clicked6.set(data[0])  # use variables as list
drop = tk.OptionMenu(frame1, clicked6, *data)
drop.config(width=12)
drop.grid(row=3, column=5, padx=5, pady=5)
tk.Label(frame1, width=20, text="Structural Components", anchor='e').grid(row=3, column=4, padx=5, pady=5)

choose = tk.StringVar()
choose.set("Yes")
option = tk.OptionMenu(frame1, choose, "Yes", "No")
option.config(width=12)
option.grid(row=3, column=3, padx=5, pady=5)
question = tk.Label(frame1, width=20, text="Devices to be installed", anchor='e').grid(row=3, column=2, padx=5, pady=5)

####################### Default Parameters

fdsPr = "fds2ascii << EOF"  # to call fds2ascii
bndf = 3  # data from BNDF file, it should be 2 for slice data
SF = 1  # for all data
domain = "y"  # all data to with in a range "n" for all data
Var = 1  # change it according to the quantity required (Var represents the variable of the interest )
EOF = "EOF"  # end of the command
i = 1  # it gives index to the output files from fds2ascii if indexing is continuous

###################---Entries Basic

smv = tk.Entry(frame1, width=15)   # this is the file name of the FDS file, do not add .smv
smv.grid(row=1, column=1)
smv.insert(tk.END, "FDS")
tk.Label(frame1, width=20, text="SMV File Name", anchor='e').grid(row=1, column=0)

maxT = tk.Entry(frame1, width=15)
maxT.grid(row=1, column=3)
maxT.insert(tk.END, "300")
tk.Label(frame1, width=20, text="Time of Simulation", anchor='e').grid(row=1, column=2)

mesh = tk.Entry(frame1, width=15)
mesh.grid(row=1, column=5)
mesh.insert(tk.END, "0.1")
tk.Label(frame1, width=20, text="Mesh Size in FDS", anchor='e').grid(row=1, column=4)

BFI = tk.Entry(frame1, width=15)
BFI.grid(row=2, column=1)
BFI.insert(tk.END, "1")
tk.Label(frame1, width=20, text="Mesh Index*", anchor='e').grid(row=2, column=0)

x = tk.Entry(frame1, width=15)
x.grid(row=2, column=3)
x.insert(tk.END, "0")
tk.Label(frame1, width=15, text="Initial Time", anchor='e').grid(row=2, column=2)

y = tk.Entry(frame1, width=15)
y.grid(row=2, column=5)
y.insert(tk.END, "10")
tk.Label(frame1, width=20, text="Time Interval", anchor='e').grid(row=2, column=4)

########################### Entries for Columns

frame2 = tk.LabelFrame(window4, text="Columns Entries", padx=5, pady=5, relief=tk.SUNKEN)
frame2.grid(row=1, column=0, sticky="nsew")

x1 = tk.Entry(frame2, width=15)
x1.grid(row=0, column=1)
x1.insert(tk.END, "0")
tk.Label(frame2, width=15, text="X Coordinate", anchor='e').grid(row=0, column=0)

y1 = tk.Entry(frame2, width=15)
y1.grid(row=0, column=3)
y1.insert(tk.END, "0")
tk.Label(frame2, width=15, text="Y Coordinate", anchor='e').grid(row=0, column=2)

intZ = tk.Entry(frame2, width=15)
intZ.grid(row=0, column=5)
intZ.insert(tk.END, "0.5")
tk.Label(frame2, width=15, text="Initial Z", anchor='e').grid(row=0, column=4)

z_ran = tk.Entry(frame2, width=15)
z_ran.grid(row=2, column=1)
z_ran.insert(tk.END, "3")
tk.Label(frame2, width=15, text="Total Height", anchor='e').grid(row=2, column=0)

z_inc = tk.Entry(frame2, width=15)
z_inc.grid(row=2, column=3)
z_inc.insert(tk.END, "1")
tk.Label(frame2, width=15, text="Increment", anchor='e').grid(row=2, column=2)

IOR1 = tk.Entry(frame2, width=15)
IOR1.grid(row=2, column=5)
IOR1.insert(tk.END, "1")
tk.Label(frame2, width=15, text="Orientation(IOR)", anchor='e').grid(row=2, column=4)

########################### Entries for Longitudinal Beams

frame3 = tk.LabelFrame(window4, text="Longitudinal Beams Entries", padx=5, pady=5, relief=tk.SUNKEN)
frame3.grid(row=2, column=0, sticky="nsew")

x2 = tk.Entry(frame3, width=15)
x2.grid(row=0, column=1)
x2.insert(tk.END, "0")
tk.Label(frame3, width=15, text="X Coordinate", anchor='e').grid(row=0, column=0)

y2 = tk.Entry(frame3, width=15)
y2.grid(row=0, column=3)
y2.insert(tk.END, "0.5")
tk.Label(frame3, width=15, text="Initial Y", anchor='e').grid(row=0, column=2)

z2 = tk.Entry(frame3, width=15)
z2.grid(row=0, column=5)
z2.insert(tk.END, "0")
tk.Label(frame3, width=15, text="Z Coordinate", anchor='e').grid(row=0, column=4)

y_ran = tk.Entry(frame3, width=15)
y_ran.grid(row=2, column=1)
y_ran.insert(tk.END, "3")
tk.Label(frame3, width=15, text="Total Length", anchor='e').grid(row=2, column=0)

y_inc = tk.Entry(frame3, width=15)
y_inc.grid(row=2, column=3)
y_inc.insert(tk.END, "1")
tk.Label(frame3, width=15, text="Increment", anchor='e').grid(row=2, column=2)

IOR2 = tk.Entry(frame3, width=15)
IOR2.grid(row=2, column=5)
IOR2.insert(tk.END, "1")
tk.Label(frame3, width=15, text="Orientation(IOR)", anchor='e').grid(row=2, column=4)

########################### Transverse Beams

frame4 = tk.LabelFrame(window4, text="Transverse Beams Entries", padx=5, pady=5, relief=tk.SUNKEN)
frame4.grid(row=3, column=0, sticky="nsew")

x3 = tk.Entry(frame4, width=15)
x3.grid(row=0, column=1)
x3.insert(tk.END, "0.5")
tk.Label(frame4, width=15, text="Initial X", anchor='e').grid(row=0, column=0)

y3 = tk.Entry(frame4, width=15)
y3.grid(row=0, column=3)
y3.insert(tk.END, "0")
tk.Label(frame4, width=15, text="Y Coordinate", anchor='e').grid(row=0, column=2)

z3 = tk.Entry(frame4, width=15)
z3.grid(row=0, column=5)
z3.insert(tk.END, "0")
tk.Label(frame4, width=15, text="Z Coordinate", anchor='e').grid(row=0, column=4)

x_ran = tk.Entry(frame4, width=15)
x_ran.grid(row=2, column=1)
x_ran.insert(tk.END, "3")
tk.Label(frame4, width=15, text="Total Length", anchor='e').grid(row=2, column=0)

x_inc = tk.Entry(frame4, width=15)
x_inc.grid(row=2, column=3)
x_inc.insert(tk.END, "1")
tk.Label(frame4, width=15, text="Increment", anchor='e').grid(row=2, column=2)

IOR3 = tk.Entry(frame4, width=15)
IOR3.grid(row=2, column=5)
IOR3.insert(tk.END, "1")
tk.Label(frame4, width=15, text="Orientation(IOR)", anchor='e').grid(row=2, column=4)

########################### Entries for Slabs

frame5 = tk.LabelFrame(window4, text="Slab Entries", padx=5, pady=5, relief=tk.SUNKEN)
frame5.grid(row=4, column=0, sticky="nsew")

x4 = tk.Entry(frame5, width=15)
x4.grid(row=0, column=1)
x4.insert(tk.END, "0")
tk.Label(frame5, width=15, text="X Coordinate", anchor='e').grid(row=0, column=0)

y4 = tk.Entry(frame5, width=15)
y4.grid(row=0, column=3)
y4.insert(tk.END, "0.5")
tk.Label(frame5, width=15, text="Initial Y", anchor='e').grid(row=0, column=2)

z4 = tk.Entry(frame5, width=15)
z4.grid(row=0, column=5)
z4.insert(tk.END, "0")
tk.Label(frame5, width=15, text="Z Coordinate", anchor='e').grid(row=0, column=4)

s_ran = tk.Entry(frame5, width=15)
s_ran.grid(row=2, column=1)
s_ran.insert(tk.END, "3")
tk.Label(frame5, width=15, text="Length oF the Slab", anchor='e').grid(row=2, column=0)

s_inc = tk.Entry(frame5, width=15)
s_inc.grid(row=2, column=3)
s_inc.insert(tk.END, "1")
tk.Label(frame5, width=15, text="Increment", anchor='e').grid(row=2, column=2)

IOR4 = tk.Entry(frame5, width=15)
IOR4.grid(row=2, column=5)
IOR4.insert(tk.END, "1")
tk.Label(frame5, width=15, text="Orientation(IOR)", anchor='e').grid(row=2, column=4)

#########################################---END OF ENTRIES---#####################################################


def output():    # main function to generate batch file
    batchfile = "Batchfile.txt"

    def batchFile(iX1, iX2, jY1, jY2, kZ1, kZ2, orientation):
        global i
        t = int(x.get())
        dt = int(y.get())
        while t < int(maxT.get()):
            with open(batchfile, 'a') as fb1:
                t1 = t
                t2 = t1 + dt
                out = "test{}.csv".format(i)  # file name which will come after the program run in FDS2ASCII
                fb1.writelines("{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n{9}\n{10}\n{11}\n{12}\n{13}"
                               "\n{14}\n{15}\n{16}\n{17}\n".format(fdsPr, smv.get(), bndf, SF, domain, iX1, iX2,
                                                                   jY1, jY2, kZ1, kZ2, t1, t2,
                                                                   orientation, Var, int(BFI.get()), out, EOF))
                t += dt
                i += 1

    if choose.get() == "Yes":
        if clicked6.get() == "Columns":
            k = float(intZ.get())
            while k <= float(y_ran.get()):
                xN = float(x1.get()) + float(mesh.get())/2
                yN = float(y1.get()) + float(mesh.get())/2
                zN = k + float(mesh.get())/2
                batchFile(float(x1.get()), xN, float(y1.get()), yN, k, zN, IOR1.get())
                k += float(z_inc.get())

        if clicked6.get() == "Longitudinal Beams":
            k2 = float(y2.get())
            while k2 <= float(y_ran.get()):
                xN = float(x2.get()) + float(mesh.get())/2
                yN = k2 + float(mesh.get())/2
                zN = float(z2.get()) + float(mesh.get())/2
                batchFile(float(x1.get()), xN, k2, yN, float(z2.get()), zN, IOR2.get())
                k2 += float(y_inc.get())

        if clicked6.get() == "Transverse Beams":
            k3 = float(x3.get())
            while k3 <= float(x_ran.get()):
                xN = k3 + float(mesh.get())/2
                yN = float(y3.get()) + float(mesh.get())/2
                zN = float(z3.get()) + float(mesh.get())/2
                batchFile(k3, xN, float(y3.get()), yN, float(z3.get()), zN, IOR3.get())
                k3 += float(x_inc.get())

        if clicked6.get() == "Slabs":
            k4 = float(y4.get())
            while k4 <= float(s_ran.get()):
                xN = float(x4.get()) + float(mesh.get())/2
                yN = k4 + float(mesh.get())/2
                zN = float(z4.get()) + float(mesh.get())/2
                batchFile(float(x4.get()), xN, k4, yN, float(z4.get()), zN, IOR4.get())
                k4 += float(s_inc.get())


File_Generation = tk.Button(window4, text="Generate Batch File", command=output, width=15, height=1)\
    .grid(row=5, column=0, padx=5, pady=5)
# this is a frame for the entries of files and options for the user to chose the devices
infoFrame = tk.LabelFrame(window4, text="Information", relief=tk.SUNKEN)
infoFrame.grid(row=8, column=0, sticky="nsew")

information = tk.Label(infoFrame, width=140, text="Run in Terminal (Linux or MacOX), "
                                                  "use (chmod +x BatchFile.command ) (name of command line) "
                                                  "and in the next "
                                                  "line run the batch file with "
                                                  "(.\BatchFile.command))", anchor='w') \
    .grid(row=15, column=0, columnspan=4, padx=5, pady=5)

window4.mainloop()
