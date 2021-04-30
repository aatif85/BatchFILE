try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
import os


class VerticalScrolledFrame:

    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        bg = kwargs.pop('bg', kwargs.pop('background', None))
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = tk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height, bg=bg)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['yscrollcommand'] = self.vsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview

        self.inner = tk.Frame(self.canvas, bg=bg)
        # pack the inner Frame into the Canvas with the top left corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    # noinspection PyUnusedLocal
    def _on_frame_configure(self, event=None):
        x1, y1, xCan, yCan = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        self.canvas.config(scrollregion=(0, 0, xCan, max(yCan, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

###################################################################

windowXBF = tk.Tk()    # main Window
windowXBF.title("Batch File Maker")
windowXBF.geometry("700x600")

window4 = VerticalScrolledFrame(windowXBF, width=100, borderwidth=2, relief=tk.SUNKEN, background="light gray")
window4.pack(fill=tk.BOTH, expand=True)

# this is a frame for the entries of files and options for the user to chose the devices
frame1 = tk.LabelFrame(window4, text="Basic Inputs", relief=tk.SUNKEN)
frame1.grid(row=0, column=0, sticky="nsew")


def location():  # Directory Location
    get = filedialog.askdirectory()
    os.chdir(get)


tk.Button(frame1, text="Directory", command=location, width=8, height=1).grid(row=0, column=1)
tk.Label(frame1, width=15, text="Get Working Directory", anchor='e').grid(row=0, column=0, padx=5, pady=5)

dirData = ["X", "Y", "Z"]
movDir = tk.StringVar()
movDir.set(dirData[0])  # use variables as list
drop = tk.OptionMenu(frame1, movDir, *dirData)
drop.config(width=8)
drop.grid(row=3, column=1, padx=5, pady=5)
tk.Label(frame1, width=15, text="Moving Direction", anchor='e').grid(row=3, column=0, padx=5, pady=5)

choose = tk.StringVar()
choose.set("Yes")
option = tk.OptionMenu(frame1, choose, "Yes", "No")
option.config(width=5)
option.grid(row=0, column=3, padx=5, pady=5)
question = tk.Label(frame1, width=20, text="Devices to be installed", anchor='e').grid(row=0, column=2, padx=5, pady=5)

meshDir = tk.StringVar()
meshDir.set("4")
meshDirOption = tk.OptionMenu(frame1, meshDir, "4", "8")
meshDirOption.config(width=5)
meshDirOption.grid(row=3, column=3, padx=5, pady=5)
tk.Label(frame1, width=20, text="Mesh Domains", anchor='e').grid(row=3, column=2, padx=5, pady=5)

####################### Default Parameters

fdsPr = "fds2ascii << EOF"  # to call fds2ascii
plt3d = 1  # data from plt3d file, it should be 2 for slice data
SF = 1  # for all data
domain = "y"  # all data to with in a range "n" for all data
Var = 1  # change it according to the quantity required (Var represents the variable of the interest )
EOF = "EOF"  # end of the command
i = 1  # it gives index to the output files from fds2ascii if indexing is continuous


###################---Entries Basic

smv = tk.Entry(frame1, width=8)   # this is the file name of the FDS file, do not add .smv
smv.grid(row=1, column=1)
smv.insert(tk.END, "Validation_BNDF")
tk.Label(frame1, width=15, text="SMV File Name", anchor='e').grid(row=1, column=0)

maxT = tk.Entry(frame1, width=5)
maxT.grid(row=1, column=3)
maxT.insert(tk.END, "300")
tk.Label(frame1, width=20, text="Time of Simulation", anchor='e').grid(row=1, column=2)

BFI = tk.Entry(frame1, width=8)
BFI.grid(row=2, column=1)
BFI.insert(tk.END, "1")
tk.Label(frame1, width=15, text="Mesh Index*", anchor='e').grid(row=2, column=0)

timInt = tk.Entry(frame1, width=5)
timInt.grid(row=2, column=3)
timInt.insert(tk.END, "10")
tk.Label(frame1, width=20, text="Time Interval", anchor='e').grid(row=2, column=2)

########################### Entries for Columns

frame2 = tk.LabelFrame(window4, text="Coordinates Entries", padx=5, pady=5, relief=tk.SUNKEN)
frame2.grid(row=1, column=0, sticky="nsew")

x1 = tk.Entry(frame2, width=5)
x1.grid(row=0, column=1)
x1.insert(tk.END, "0")
tk.Label(frame2, width=10, text="X Coordinate", anchor='e').grid(row=0, column=0)

y1 = tk.Entry(frame2, width=5)
y1.grid(row=0, column=3)
y1.insert(tk.END, "0")
tk.Label(frame2, width=10, text="Y Coordinate", anchor='e').grid(row=0, column=2)

z1 = tk.Entry(frame2, width=5)
z1.grid(row=0, column=5)
z1.insert(tk.END, "0.5")
tk.Label(frame2, width=10, text="Z Coordinate", anchor='e').grid(row=0, column=4)

totLen = tk.Entry(frame2, width=5)
totLen.grid(row=2, column=1)
totLen.insert(tk.END, "3")
tk.Label(frame2, width=10, text="Total Length", anchor='e').grid(row=2, column=0)

inc = tk.Entry(frame2, width=5)
inc.grid(row=2, column=3)
inc.insert(tk.END, "1")
tk.Label(frame2, width=10, text="Increment", anchor='e').grid(row=2, column=2)

#########################################---END OF ENTRIES---#####################################################


def output():    # main function to generate batch file
    batchfile = "Batchfile.txt"

    def batchFile(iX1, iX2, jY1, jY2, kZ1, kZ2):
        with open(batchfile, 'a') as fb1:
            fb1.writelines("{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n{9}\n{10}\n".format(fdsPr, smv.get(), plt3d, SF, "y",
                                                                                             iX1, iX2, jY1, jY2, kZ1, kZ2))
        global i
        t = 0
        dt = int(timInt.get())
        mIndex = int(BFI.get())
        while t < int(maxT.get()):
            if meshDir.get() == "4":
                with open(batchfile, 'a') as fb1:
                    out = "test{}.csv".format(i)  # file name which will come after the program run in FDS2ASCII
                    fb1.writelines("{0}\n{1}\n".format(mIndex, out))
                    t += dt
                    i += 1
                    mIndex += 4

            if meshDir.get() == "8":
                with open(batchfile, 'a') as fb1:
                    out = "test{}.csv".format(i)  # file name which will come after the program run in FDS2ASCII
                    fb1.writelines("{0}\n{1}\n".format(mIndex, out))
                    t += dt
                    i += 1
                    mIndex += 8

        with open(batchfile, 'a') as fb1:
            fb1.writelines("EOF\n".format())

    Length = float(totLen.get()) + 0.0005
    increment = float(inc.get())
    if movDir.get() == "X":
        initialX = float(x1.get())
        while initialX <= Length:
            xN = initialX + 0.0005
            yN = float(y1.get()) + 0.0005
            zN = float(z1.get()) + 0.0005
            batchFile(initialX, xN, float(y1.get()), yN, float(z1.get()), zN)
            initialX += increment

    if movDir.get() == "Y":
        initialY = float(y1.get())
        while initialY <= Length:
            xN = float(x1.get()) + 0.0005
            yN = initialY + 0.0005
            zN = float(z1.get()) + 0.0005
            batchFile(float(x1.get()), xN, initialY, yN, float(z1.get()), zN)
            initialY += increment

    if movDir.get() == "Z":
        initialZ = float(x1.get())
        while initialZ <= Length:
            xN = float(x1.get()) + 0.0005
            yN = float(y1.get()) + 0.0005
            zN = initialZ + 0.0005
            batchFile(float(x1.get()), xN, float(y1.get()), yN, initialZ, zN)
            initialZ += increment


File_Generation = tk.Button(window4, text="Generate Batch File", command=output, width=15, height=1) \
    .grid(row=5, column=0, padx=5, pady=5)

infoFrame = tk.LabelFrame(window4, text="Information", relief=tk.SUNKEN)
infoFrame.grid(row=8, column=0, sticky="nsew")

tk.Label(infoFrame, width=50, text="Run in Terminal (Linux or MacOX or GitBash in Windows),use (chmod +x BatchFile.command)", anchor='w') \
    .grid(row=15, column=0, columnspan=4, padx=5, pady=5)
tk.Label(infoFrame, width=40, text=" and in the next line run the batch file with ", anchor='w') \
    .grid(row=16, column=0, columnspan=4, padx=5, pady=5)
tk.Label(infoFrame, width=40, text="./Batchfile.command ", anchor='w') \
    .grid(row=17, column=0, columnspan=4, padx=5, pady=5)


window4.mainloop()
