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
tk.Label(frame1, width=17, text="Get Working Directory", anchor='e').grid(row=0, column=0, padx=5, pady=5)

# dropbox for the structural components
data = ["Columns", "Beams", "Trusses", "Slabs"]
clicked6 = tk.StringVar()
clicked6.set(data[0])  # use variables as list
drop = tk.OptionMenu(frame1, clicked6, *data)
drop.config(width=12)
drop.grid(row=4, column=1, padx=5, pady=5)
tk.Label(frame1, width=20, text="Structural Components", anchor='e').grid(row=4, column=0, padx=5, pady=5)

choose = tk.StringVar()
choose.set("Yes")
option = tk.OptionMenu(frame1, choose, "Yes", "No")
option.config(width=5)
option.grid(row=4, column=3, padx=5, pady=5)
question = tk.Label(frame1, width=20, text="Devices to be installed", anchor='e').grid(row=4, column=2, padx=5, pady=5)

####################### Default Parameters

fdsPr = "fds2ascii << EOF"  # to call fds2ascii
bndf = 3  # data from BNDF file, it should be 2 for slice data
SF = 1  # for all data
domain = "y"  # all data to with in a range "n" for all data
Var = 1  # change it according to the quantity required (Var represents the variable of the interest )
EOF = "EOF"  # end of the command
i = 1  # it gives index to the output files from fds2ascii if indexing is continuous

###################---Entries Basic

smv = tk.Entry(frame1, width=5)   # this is the file name of the FDS file, do not add .smv
smv.grid(row=1, column=1)
smv.insert(tk.END, "FDS")
tk.Label(frame1, width=15, text="SMV File Name", anchor='e').grid(row=1, column=0)

maxT = tk.Entry(frame1, width=5)
maxT.grid(row=1, column=3)
maxT.insert(tk.END, "300")
tk.Label(frame1, width=15, text="Time of Simulation", anchor='e').grid(row=1, column=2)

mesh = tk.Entry(frame1, width=5)
mesh.grid(row=2, column=1)
mesh.insert(tk.END, "0.1")
tk.Label(frame1, width=15, text="Mesh Size in FDS", anchor='e').grid(row=2, column=0)

BFI = tk.Entry(frame1, width=5)
BFI.grid(row=2, column=3)
BFI.insert(tk.END, "1")
tk.Label(frame1, width=20, text="Mesh Index*", anchor='e').grid(row=2, column=2)

x = tk.Entry(frame1, width=5)
x.grid(row=3, column=1)
x.insert(tk.END, "0")
tk.Label(frame1, width=10, text="Initial Time", anchor='e').grid(row=3, column=0)

y = tk.Entry(frame1, width=5)
y.grid(row=3, column=3)
y.insert(tk.END, "10")
tk.Label(frame1, width=20, text="Time Interval", anchor='e').grid(row=3, column=2)

########################### Entries for Columns

frame2 = tk.LabelFrame(window4, text="Columns Entries", padx=5, pady=5, relief=tk.SUNKEN)
frame2.grid(row=1, column=0, sticky="nsew")

x1 = tk.Entry(frame2, width=5)
x1.grid(row=0, column=1)
x1.insert(tk.END, "0")
tk.Label(frame2, width=10, text="X Coordinate", anchor='e').grid(row=0, column=0)

y1 = tk.Entry(frame2, width=5)
y1.grid(row=0, column=3)
y1.insert(tk.END, "0")
tk.Label(frame2, width=10, text="Y Coordinate", anchor='e').grid(row=0, column=2)

intZ = tk.Entry(frame2, width=5)
intZ.grid(row=0, column=5)
intZ.insert(tk.END, "0.5")
tk.Label(frame2, width=10, text="Initial Z", anchor='e').grid(row=0, column=4)

z_ran = tk.Entry(frame2, width=5)
z_ran.grid(row=2, column=1)
z_ran.insert(tk.END, "3")
tk.Label(frame2, width=10, text="Total Height", anchor='e').grid(row=2, column=0)

z_inc = tk.Entry(frame2, width=5)
z_inc.grid(row=2, column=3)
z_inc.insert(tk.END, "1")
tk.Label(frame2, width=10, text="Increment", anchor='e').grid(row=2, column=2)

IOR1 = tk.Entry(frame2, width=5)
IOR1.grid(row=2, column=5)
IOR1.insert(tk.END, "1")
tk.Label(frame2, width=15, text="Orientation(IOR)", anchor='e').grid(row=2, column=4)

########################### Beams

beamFrame = tk.LabelFrame(window4, text="Beams Entries", padx=5, pady=5, relief=tk.SUNKEN)
beamFrame.grid(row=2, column=0, sticky="nsew")

directionLengthBEAM = ["X", "Y"]
incrementDirectionBEAM = tk.StringVar()  # it was clickedEnt
incrementDirectionBEAM.set(directionLengthBEAM[0])  # use variables as list
incrementBeamDrop = tk.OptionMenu(beamFrame, incrementDirectionBEAM, *directionLengthBEAM)
incrementBeamDrop.config(width=5)
incrementBeamDrop.grid(row=0, column=1, padx=5, pady=5)
tk.Label(beamFrame, width=15, text="Initial Inc. Dir.", anchor='e').grid(row=0, column=0)


x_Beam = tk.Entry(beamFrame, width=5)
x_Beam.grid(row=1, column=1)
x_Beam.insert(tk.END, "0")
tk.Label(beamFrame, width=15, text="Value of X", anchor='e').grid(row=1, column=0)

y_Beam = tk.Entry(beamFrame, width=5)
y_Beam.grid(row=1, column=3)
y_Beam.insert(tk.END, "0")
tk.Label(beamFrame, width=15, text="Value of Y", anchor='e').grid(row=1, column=2)

z_Beam = tk.Entry(beamFrame, width=5)
z_Beam.grid(row=1, column=5)
z_Beam.insert(tk.END, "3400")
tk.Label(beamFrame, width=15, text="Value of Z", anchor='e').grid(row=1, column=4)

x_LenBeam = tk.Entry(beamFrame, width=5)
x_LenBeam.grid(row=2, column=1)
x_LenBeam.insert(tk.END, "5")
tk.Label(beamFrame, width=15, text="Length in X", anchor='e').grid(row=2, column=0)

y_LenBeam = tk.Entry(beamFrame, width=5)
y_LenBeam.grid(row=2, column=3)
y_LenBeam.insert(tk.END, "5")
tk.Label(beamFrame, width=15, text="Length in Y", anchor='e').grid(row=2, column=2)

incX_Beam = tk.Entry(beamFrame, width=5)
incX_Beam.grid(row=2, column=5)
incX_Beam.insert(tk.END, "5000")
tk.Label(beamFrame, width=15, text="Increment in X", anchor='e').grid(row=2, column=4)

incY_Beam = tk.Entry(beamFrame, width=5)
incY_Beam.grid(row=3, column=1)
incY_Beam.insert(tk.END, "5000")
tk.Label(beamFrame, width=15, text="Increment in Y", anchor='e').grid(row=3, column=0)

ior_Beam = tk.Entry(beamFrame, width=5)
ior_Beam.grid(row=3, column=3)
ior_Beam.insert(tk.END, "-3")
tk.Label(beamFrame, width=15, text="Orientation", anchor='e').grid(row=3, column=2)

########################### Trusses

frameTruss = tk.LabelFrame(window4, text="Truss Entries", padx=5, pady=5, relief=tk.SUNKEN)
frameTruss.grid(row=3, column=0, sticky="nsew")

directionLengthTRUSS = ["X", "Y"]
incrementDirectionTRUSS = tk.StringVar()  # it was clickedEnt
incrementDirectionTRUSS.set(directionLengthTRUSS[0])  # use variables as list
incrementDrop = tk.OptionMenu(frameTruss, incrementDirectionTRUSS, *directionLengthTRUSS)
incrementDrop.config(width=5)
incrementDrop.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frameTruss, width=15, text="Initial Inc. Dir.", anchor='e').grid(row=0, column=0)

xTruss = tk.Entry(frameTruss, width=5)
xTruss.grid(row=1, column=1)
xTruss.insert(tk.END, "0")
tk.Label(frameTruss, width=15, text="Value of X", anchor='e').grid(row=1, column=0)

yTruss = tk.Entry(frameTruss, width=5)
yTruss.grid(row=1, column=3)
yTruss.insert(tk.END, "0")
tk.Label(frameTruss, width=15, text="Value of Y", anchor='e').grid(row=1, column=2)

lLimitTruss = tk.Entry(frameTruss, width=5)
lLimitTruss.grid(row=1, column=5)
lLimitTruss.insert(tk.END, "3400")
tk.Label(frameTruss, width=15, text="Lower Height", anchor='e').grid(row=1, column=4)

uLimitTruss = tk.Entry(frameTruss, width=5)
uLimitTruss.grid(row=2, column=1)
uLimitTruss.insert(tk.END, "3800")
tk.Label(frameTruss, width=15, text="Upper Height", anchor='e').grid(row=2, column=0)

incXTruss = tk.Entry(frameTruss, width=5)
incXTruss.grid(row=2, column=3)
incXTruss.insert(tk.END, "5000")
tk.Label(frameTruss, width=15, text="Increment in X", anchor='e').grid(row=2, column=2)

incYTruss = tk.Entry(frameTruss, width=5)
incYTruss.grid(row=2, column=5)
incYTruss.insert(tk.END, "5000")
tk.Label(frameTruss, width=15, text="Increment in Y", anchor='e').grid(row=2, column=4)

X_lenTruss = tk.Entry(frameTruss, width=5)
X_lenTruss.grid(row=3, column=1)
X_lenTruss.insert(tk.END, "5")
tk.Label(frameTruss, width=15, text="Length in X", anchor='e').grid(row=3, column=0)

Y_lenTruss = tk.Entry(frameTruss, width=5)
Y_lenTruss.grid(row=3, column=3)
Y_lenTruss.insert(tk.END, "5")
tk.Label(frameTruss, width=15, text="Length in Y", anchor='e').grid(row=3, column=2)

iorTruss = tk.Entry(frameTruss, width=5)
iorTruss.grid(row=3, column=5)
iorTruss.insert(tk.END, "-3")
tk.Label(frameTruss, width=15, text="Orientation", anchor='e').grid(row=3, column=4)

########################### Entries for Slabs

slabFrame = tk.LabelFrame(window4, text="Slab Entries", padx=5, pady=5, relief=tk.SUNKEN)
slabFrame.grid(row=4, column=0, sticky="nsew")

directionLengthSLB = ["X", "Y"]
incrementDirectionSLB = tk.StringVar()  # it was clickedEnt
incrementDirectionSLB .set(directionLengthSLB[0])  # use variables as list
incrementDrop = tk.OptionMenu(slabFrame, incrementDirectionSLB, *directionLengthSLB)
incrementDrop.config(width=5)
incrementDrop.grid(row=0, column=1, padx=5, pady=5)
tk.Label(slabFrame, width=15, text="Initial Inc. Dir.", anchor='e').grid(row=0, column=0)

y_slab = tk.Entry(slabFrame, width=5)
y_slab.grid(row=1, column=1)
y_slab.insert(tk.END, "0")
tk.Label(slabFrame, width=15, text="Value of Y", anchor='e').grid(row=1, column=0)

z_slab = tk.Entry(slabFrame, width=5)
z_slab.grid(row=1, column=3)
z_slab.insert(tk.END, "3800")
tk.Label(slabFrame, width=15, text="Value of Z", anchor='e').grid(row=1, column=2)

xInt_slab = tk.Entry(slabFrame, width=5)
xInt_slab.grid(row=1, column=5)
xInt_slab.insert(tk.END, "0")
tk.Label(slabFrame, width=15, text="Initial Value of X", anchor='e').grid(row=1, column=4)

xLen_slab = tk.Entry(slabFrame, width=5)
xLen_slab.grid(row=2, column=1)
xLen_slab.insert(tk.END, "5")
tk.Label(slabFrame, width=15, text="Length Along the Slab", anchor='e').grid(row=2, column=0)

incX_slab = tk.Entry(slabFrame, width=5)
incX_slab.grid(row=2, column=3)
incX_slab.insert(tk.END, "5000")
tk.Label(slabFrame, width=15, text="Increment", anchor='e').grid(row=2, column=2)

ior_slab = tk.Entry(slabFrame, width=5)
ior_slab.grid(row=2, column=5)
ior_slab.insert(tk.END, "-3")
tk.Label(slabFrame, width=15, text="Orientation", anchor='e').grid(row=2, column=4)

incY_slab = tk.Entry(slabFrame, width=5)
incY_slab.grid(row=3, column=1)
incY_slab.insert(tk.END, "5000")
tk.Label(slabFrame, width=15, text="Increment in Y", anchor='e').grid(row=3, column=0)

widthY_slab = tk.Entry(slabFrame, width=5)
widthY_slab.grid(row=3, column=3)
widthY_slab.insert(tk.END, "5")
tk.Label(slabFrame, width=15, text="Total Width of Slab", anchor='e').grid(row=3, column=2)

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
            k = float(intZ.get()) + float(z_inc.get())/2
            while k <= float(z_ran.get()):
                xN = float(x1.get()) + float(mesh.get())/2
                yN = float(y1.get()) + float(mesh.get())/2
                zN = k + float(mesh.get())/2
                batchFile(float(x1.get()), xN, float(y1.get()), yN, k, zN, IOR1.get())
                k += float(z_inc.get())

        if clicked6.get() == "Beams":
            if incrementDirectionBEAM.get() == "X":
                incrementY_Beam = float(incY_Beam.get())
                initialY = float(y_Beam.get()) + incrementY_Beam / 2
                BeamLengthY = float(y_LenBeam.get())
                while initialY <= BeamLengthY:
                    initialX_Beam = float(x_Beam.get()) + float(incX_Beam.get()) / 2
                    BeamLengthX = float(x_LenBeam.get())
                    incrementX_Beam = float(incX_Beam.get())
                    while initialX_Beam <= BeamLengthX:
                        xN = initialX_Beam + float(mesh.get())/2
                        yN = initialY + float(mesh.get())/2
                        zN = float(z_Beam.get()) + float(mesh.get())/2
                        batchFile(initialX_Beam, xN, initialY, yN, float(z_Beam.get()), zN, ior_Beam.get())
                        initialX_Beam += incrementX_Beam
                    initialY += incrementY_Beam

            if incrementDirectionBEAM.get() == "Y":
                incrementX_Beam = float(incX_Beam.get())
                initialX_Beam = float(x_Beam.get()) + incrementX_Beam / 2
                BeamLengthX = float(x_LenBeam.get())
                while initialX_Beam <= BeamLengthX:
                    incrementY_Beam = float(incY_Beam.get())
                    initialY = float(y_Beam.get()) + incrementY_Beam / 2
                    BeamLengthY = float(y_LenBeam.get())
                    while initialY <= BeamLengthY:
                        xN = initialX_Beam + float(mesh.get())/2
                        yN = initialY + float(mesh.get())/2
                        zN = float(z_Beam.get()) + float(mesh.get())/2
                        batchFile(initialX_Beam, xN, initialY, yN, float(z_Beam.get()), zN, ior_Beam.get())
                        initialY += incrementY_Beam
                    initialX_Beam += incrementX_Beam

        if clicked6.get() == "Trusses":
            if incrementDirectionTRUSS.get() == "X":
                incrementY_Truss = float(incYTruss.get())
                initialY_Truss = float(yTruss.get()) + incrementY_Truss / 2
                TrussWidth = float(Y_lenTruss.get())
                while initialY_Truss <= TrussWidth:
                    incrementX_Truss = float(incXTruss.get())
                    initialX_Truss = float(xTruss.get()) + incrementX_Truss / 2
                    TrussLength = float(X_lenTruss.get())
                    while initialX_Truss <= TrussLength:
                        xN = initialX_Truss + float(mesh.get())/2
                        yN = initialY_Truss + float(mesh.get())/2
                        zN = float(lLimitTruss.get()) + float(mesh.get())/2
                        batchFile(initialX_Truss, xN, initialY_Truss, yN, float(lLimitTruss.get()), zN, ior_Beam.get())
                        initialX_Truss += incrementX_Truss
                    initialY_Truss += incrementY_Truss

            if incrementDirectionTRUSS.get() == "Y":
                incrementX_Truss = float(incXTruss.get())
                initialX_Truss = float(xTruss.get()) + incrementX_Truss / 2
                TrussLength = float(X_lenTruss.get())
                while initialX_Truss <= TrussLength:
                    incrementY_Truss = float(incYTruss.get())
                    initialY_Truss = float(yTruss.get()) + incrementY_Truss / 2
                    TrussWidth = float(Y_lenTruss.get())
                    while initialY_Truss <= TrussWidth:
                        xN = initialX_Truss + float(mesh.get())/2
                        yN = initialY_Truss + float(mesh.get())/2
                        zN = float(lLimitTruss.get()) + float(mesh.get())/2
                        batchFile(initialX_Truss, xN, initialY_Truss, yN, float(lLimitTruss.get()), zN, ior_Beam.get())
                        initialY_Truss += incrementY_Truss
                    initialX_Truss += incrementX_Truss

        if clicked6.get() == "Slabs":
            if incrementDirectionSLB.get() == "X":
                incrementY_Slab = float(incY_slab.get())
                initialY_Slab = float(y_slab.get()) + incrementY_Slab / 2
                slabYWidth = float(widthY_slab.get())
                while initialY_Slab <= slabYWidth:
                    incrementX_SLAB = float(incX_slab.get())
                    initialX_SLAB = float(xInt_slab.get()) + incrementX_SLAB / 2
                    lengthX_SLAB = float(xLen_slab.get())
                    while initialX_SLAB <= lengthX_SLAB:
                        xN = initialX_SLAB + float(mesh.get())/2
                        yN = initialY_Slab + float(mesh.get())/2
                        zN = float(z_slab.get()) + float(mesh.get())/2
                        batchFile(initialX_SLAB, xN, initialY_Slab, yN, float(z_slab.get()), zN, ior_Beam.get())
                        initialX_SLAB += incrementX_SLAB
                    initialY_Slab += incrementY_Slab

            if incrementDirectionSLB.get() == "Y":
                incrementX_SLAB = float(incX_slab.get())
                initialX_SLAB = float(xInt_slab.get()) + incrementX_SLAB / 2
                lengthX_SLAB = float(xLen_slab.get())
                while initialX_SLAB <= lengthX_SLAB:
                    incrementY_Slab = float(incY_slab.get())
                    initialY_Slab = float(y_slab.get()) + incrementY_Slab / 2
                    slabYWidth = float(widthY_slab.get())
                    while initialY_Slab <= slabYWidth:
                        xN = initialX_SLAB + float(mesh.get())/2
                        yN = initialY_Slab + float(mesh.get())/2
                        zN = float(z_slab.get()) + float(mesh.get())/2
                        batchFile(initialX_SLAB, xN, initialY_Slab, yN, float(z_slab.get()), zN, ior_Beam.get())
                        initialY_Slab += incrementY_Slab
                    initialX_SLAB += incrementX_SLAB


File_Generation = tk.Button(window4, text="Generate Batch File", command=output, width=15, height=1)\
    .grid(row=5, column=0, padx=5, pady=5)
# this is a frame for the entries of files and options for the user to chose the devices
infoFrame = tk.LabelFrame(window4, text="Information", relief=tk.SUNKEN)
infoFrame.grid(row=8, column=0, sticky="nsew")

tk.Label(infoFrame, width=50, text="Run in Terminal (Linux or MacOX),use (chmod +x BatchFile.command)", anchor='w') \
    .grid(row=15, column=0, columnspan=4, padx=5, pady=5)
tk.Label(infoFrame, width=40, text=" and in the next line run the batch file with ", anchor='w') \
    .grid(row=16, column=0, columnspan=4, padx=5, pady=5)
tk.Label(infoFrame, width=40, text=".\Batchfile.command ", anchor='w') \
    .grid(row=17, column=0, columnspan=4, padx=5, pady=5)


window4.mainloop()
