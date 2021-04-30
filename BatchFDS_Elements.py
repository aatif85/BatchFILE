try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
import os
import csv
import pandas as pd
import numpy as np

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


def createFolder(directory):  # creating folders in the directory
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating Directory.' + directory)


windowXBF = tk.Tk()    # main Window
windowXBF.title("Batch File Maker")
windowXBF.geometry("1100x700")

window4 = VerticalScrolledFrame(windowXBF, width=100, borderwidth=2, relief=tk.SUNKEN, background="light gray")
window4.pack(fill=tk.BOTH, expand=True)

# this is a frame for the entries of files and options for the user to chose the devices
frame1 = tk.LabelFrame(window4, text="Basic Inputs", relief=tk.SUNKEN)
frame1.grid(row=0, column=0, sticky="nsew")

batchfile = "Batchfile.txt"
osFile = 'OpenSees.txt'  # script file for OpenSEES HT
ELEMENT_SET2 = 'Elementset2.txt'  # element file containing boundary file names
ELEMENT_SET_COL = 'ElementFiles/Col_elementset.txt'  # makes element for columns
ELEMENT_SET_BEAM = 'ElementFiles/Beam_elementset.txt'  # makes element for beam
ELEMENT_SET_Truss = 'ElementFiles/Truss_elementset.txt'  # makes element for Truss
onlyColEle = 'ElementFiles/Column_elementLoad.txt'  # makes element loads for columns
onlyBeamEle = 'ElementFiles/Beam_elementLoad.txt'   # makes element loads for beam
onlySlabEle = 'ElementFiles/Slab_elementLoad.txt'   # makes element loads for slab
onlyTrussEle = 'ElementFiles/truss1_elementLoad.txt'  # makes element loads for truss
finalTrussEle = 'ElementFiles/truss_elementLoadFinal.txt'   # makes element loads for truss after removing duplicate
Final_EleSET2 = 'Final_EleSet.txt'   # makes final file containing updated files


def location():  # Directory Location
    get = filedialog.askdirectory()
    os.chdir(get)


tk.Button(frame1, text="Directory", command=location, width=8, height=1).grid(row=0, column=1)
tk.Label(frame1, width=17, text="Get Working Directory", anchor='e').grid(row=0, column=0, padx=5, pady=5)



# this is a frame for the entries for OpenSEES
OSFrame = tk.LabelFrame(window4, text="OpenSEES Inputs", padx=5, pady=5)   # it was OSFrame
OSFrame.grid(row=0, column=2, sticky="nsew")

materialSelect = ["CarbonSteelEC3", "ConcreteEC2"]
selectMat = tk.StringVar()
selectMat.set(materialSelect[0])  # use variables as list
matDrop = tk.OptionMenu(OSFrame, selectMat, *materialSelect)
matDrop.config(width=10)
matDrop.grid(row=2, column=1, padx=5, pady=5)
tk.Label(OSFrame, width=15, text="Material", anchor='e').grid(row=2, column=0, padx=5, pady=5)

matTag = tk.Entry(OSFrame, width=5)
matTag.grid(row=2, column=3)
matTag.insert(tk.END, "1")
tk.Label(OSFrame, width=15, text="Tag for Material", anchor='e').grid(row=2, column=2)


def addMaterial():  # adding materials
    with open(osFile, 'a') as fileOS:
        fileOS.writelines("HTMaterial {0} {1};\n\n".format(selectMat.get(), matTag.get()))


tk.Button(OSFrame, text="Add Material", command=addMaterial, width=10, height=1).grid(row=2, column=4, padx=5, pady=5)

htConstants = tk.Entry(OSFrame, width=10)
htConstants.grid(row=3, column=1)
htConstants.insert(tk.END, "25 293.15 0.85 0.85")
tk.Label(OSFrame, width=15, text="HT Constants", anchor='e').grid(row=3, column=0)

htConstTag = tk.Entry(OSFrame, width=5)
htConstTag.grid(row=3, column=3)
htConstTag.insert(tk.END, "2")
tk.Label(OSFrame, width=15, text="Tag for HT Constants", anchor='e').grid(row=3, column=2)


def addHTConstants():  # adding constants for convection and radiation
    with open(osFile, 'a') as fileOS:
        fileOS.writelines("HTConstants {0} {1};\n\n".format(htConstTag.get(), htConstants.get()))


tk.Button(OSFrame, text="Add Constants", command=addHTConstants, width=10, height=1).grid(row=3, column=4)

pChange = tk.Entry(OSFrame, width=10)
pChange.grid(row=4, column=1)
pChange.insert(tk.END, "0")
tk.Label(OSFrame, width=15, text="Phase Change", anchor='e').grid(row=4, column=0)

fireModelType = tk.Entry(OSFrame, width=10)   # it was fModel
fireModelType.grid(row=5, column=1)
fireModelType.insert(tk.END, "1")
tk.Label(OSFrame, width=15, text="Fire Model Type", anchor='e').grid(row=5, column=0)

fdsFileName = tk.Entry(OSFrame, width=5)  # Boundary Condition ...it was fMBfile
fdsFileName.grid(row=5, column=3)
fdsFileName.insert(tk.END, "AST")
tk.Label(OSFrame, width=15, text="Input Boundary File", anchor='e').grid(row=5, column=2)

hfFaces = tk.Entry(OSFrame, width=10)    # it was hffaces
hfFaces.grid(row=6, column=1)
hfFaces.insert(tk.END, "1 5 7 9 12")
tk.Label(OSFrame, width=15, text="Faces for Heat Flux", anchor='e').grid(row=6, column=0)

modelHT_Tag = tk.Entry(OSFrame, width=10)   # it was htConst
modelHT_Tag.grid(row=7, column=1)
modelHT_Tag.insert(tk.END, "1")
tk.Label(OSFrame, width=16, text="Model HT Const. Tag", anchor='e').grid(row=7, column=0)

modelMatTag = tk.Entry(OSFrame, width=5)  # it was matT
modelMatTag.grid(row=7, column=3)
modelMatTag.insert(tk.END, "1")
tk.Label(OSFrame, width=15, text="Section Material Tag", anchor='e').grid(row=7, column=2)

nodeSetType = ["Faces", "User Defined"]
selectNodeSet = tk.StringVar()                 # this was clickedNS
selectNodeSet.set(nodeSetType[0])  # use variables as list
NS_Drop = tk.OptionMenu(OSFrame, selectNodeSet, *nodeSetType)
NS_Drop.config(width=5)
NS_Drop.grid(row=8, column=1, padx=5, pady=5)
tk.Label(OSFrame, width=15, text="Node Sets Location", anchor='e').grid(row=8, column=0, padx=5, pady=5)

Nodeset = tk.Entry(OSFrame, width=10)   # it was fNodeset
Nodeset.grid(row=8, column=2)
Nodeset.insert(tk.END, "1 4 5")

locDepth = ["2", "5", "9"]
deptLocation = tk.StringVar()                 # this was clickedNS
deptLocation.set(locDepth[1])  # use variables as list
loc_Drop = tk.OptionMenu(OSFrame, deptLocation, *locDepth)
loc_Drop.config(width=5)
loc_Drop.grid(row=8, column=4, padx=5, pady=5)
tk.Label(OSFrame, width=15, text="Number of Points", anchor='e').grid(row=8, column=3, padx=3, pady=5)

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
tk.Label(frame1, width=12, text="SMV File Name", anchor='e').grid(row=1, column=0)

maxT = tk.Entry(frame1, width=5)
maxT.grid(row=1, column=3)
maxT.insert(tk.END, "300")
tk.Label(frame1, width=20, text="Time of Simulation", anchor='e').grid(row=1, column=2)

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

units = tk.StringVar()
units.set("m")
unitsOption = tk.OptionMenu(frame1, units, "m", "mm")
unitsOption.config(width=5)
unitsOption.grid(row=4, column=1, padx=5, pady=5)
tk.Label(frame1, width=15, text="Units", anchor='e').grid(row=4, column=0, padx=5, pady=5)

makeOpenSEES = tk.StringVar()  # to chose if entities to be created
makeOpenSEES.set("Yes")
OS_Option = tk.OptionMenu(frame1, makeOpenSEES, "Yes", "No")
OS_Option.config(width=5)
OS_Option.grid(row=4, column=3, padx=5, pady=5)
tk.Label(frame1, width=15, text="Creating Entities", anchor='e').grid(row=4, column=2, padx=5, pady=5)

elementSetGen = tk.StringVar()
elementSetGen.set("Yes")
ESetOption = tk.OptionMenu(frame1, elementSetGen, "Yes", "No")
ESetOption.config(width=5)
ESetOption.grid(row=5, column=1, padx=5, pady=5)
tk.Label(frame1, width=10, text="Element Sets", anchor='e').grid(row=5, column=0, padx=5, pady=5)

entityType = ["Isection", "Block", "Brick"]
selectEntity = tk.StringVar()  # it was clickedEnt
selectEntity.set(entityType[0])  # use variables as list
EntityDrop = tk.OptionMenu(frame1, selectEntity, *entityType)
EntityDrop.config(width=10)
EntityDrop.grid(row=5, column=3, padx=5, pady=5)
tk.Label(frame1, width=15, text="Section Entity", anchor='e').grid(row=5, column=2, padx=5, pady=5)

dimAnalysis = tk.StringVar()  # to chose if entities to be created
dimAnalysis.set("2D")
dimOption = tk.OptionMenu(frame1, dimAnalysis, "2D", "3D")
dimOption.config(width=10)
dimOption.grid(row=6, column=1, padx=5, pady=5)
tk.Label(frame1, width=15, text="HT Analysis", anchor='e').grid(row=6, column=0, padx=5, pady=5)

# dropbox for the structural components
data = ["Columns", "Beams", "Trusses", "Slabs"]
clicked6 = tk.StringVar()
clicked6.set(data[0])  # use variables as list
drop = tk.OptionMenu(frame1, clicked6, *data)
drop.config(width=13)
drop.grid(row=7, column=1, padx=5, pady=5)
tk.Label(frame1, width=15, text="Structural Components", anchor='e').grid(row=7, column=0, padx=5, pady=5)

choose = tk.StringVar()
choose.set("Yes")
option = tk.OptionMenu(frame1, choose, "Yes", "No")
option.config(width=5)
option.grid(row=6, column=3, padx=5, pady=5)
question = tk.Label(frame1, width=20, text="Devices to be installed", anchor='e').grid(row=6, column=2, padx=5, pady=5)

########################### Entries for Columns

frame2 = tk.LabelFrame(window4, text="Columns Entries", padx=5, pady=5, relief=tk.SUNKEN)
frame2.grid(row=1, column=0, sticky="nsew")

x_Column = tk.Entry(frame2, width=5)
x_Column.grid(row=0, column=1)
x_Column.insert(tk.END, "0")
tk.Label(frame2, width=10, text="X Coordinate", anchor='e').grid(row=0, column=0)

y_Column = tk.Entry(frame2, width=5)
y_Column.grid(row=0, column=3)
y_Column.insert(tk.END, "0")
tk.Label(frame2, width=10, text="Y Coordinate", anchor='e').grid(row=0, column=2)

z_Column = tk.Entry(frame2, width=5)
z_Column.grid(row=0, column=5)
z_Column.insert(tk.END, "0.5")
tk.Label(frame2, width=10, text="Initial Z", anchor='e').grid(row=0, column=4)

columnHeight = tk.Entry(frame2, width=5)
columnHeight.grid(row=2, column=1)
columnHeight.insert(tk.END, "3")
tk.Label(frame2, width=10, text="Total Height", anchor='e').grid(row=2, column=0)

inc_Column = tk.Entry(frame2, width=5)
inc_Column.grid(row=2, column=3)
inc_Column.insert(tk.END, "1")
tk.Label(frame2, width=10, text="Increment", anchor='e').grid(row=2, column=2)

inc_Column = tk.Entry(frame2, width=5)
inc_Column.grid(row=2, column=5)
inc_Column.insert(tk.END, "1")
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


################################################------OpenSEES File Entries-------#####################################
##### I section Entries

iSectionFrame = tk.LabelFrame(window4, text="I Section Entities", padx=5, pady=5)
iSectionFrame.grid(row=1, column=2, sticky="nsew")

cX_iSec = tk.Entry(iSectionFrame, width=5)
cX_iSec.grid(row=0, column=1)
cX_iSec.insert(tk.END, "0")
tk.Label(iSectionFrame, width=20, text="Centroid of X", anchor='e').grid(row=0, column=0)

cY_iSec = tk.Entry(iSectionFrame, width=5)
cY_iSec.grid(row=0, column=3)
cY_iSec.insert(tk.END, "0")
tk.Label(iSectionFrame, width=20, text="Centroid of Y", anchor='e').grid(row=0, column=2)

flangeWidth = tk.Entry(iSectionFrame, width=5)
flangeWidth.grid(row=1, column=1)
flangeWidth.insert(tk.END, "0.4")
tk.Label(iSectionFrame, width=20, text="Width of Flange", anchor='e').grid(row=1, column=0)

beamHeight = tk.Entry(iSectionFrame, width=5)
beamHeight.grid(row=1, column=3)
beamHeight.insert(tk.END, "0.4")
tk.Label(iSectionFrame, width=20, text="Height of Beam", anchor='e').grid(row=1, column=2)

webThickness = tk.Entry(iSectionFrame, width=5)
webThickness.grid(row=2, column=1)
webThickness.insert(tk.END, "0.008")
tk.Label(iSectionFrame, width=20, text="Web Thickness", anchor='e').grid(row=2, column=0)

flangeThickness = tk.Entry(iSectionFrame, width=5)
flangeThickness.grid(row=2, column=3)
flangeThickness.insert(tk.END, "0.01")
tk.Label(iSectionFrame, width=20, text="Flange Thickness", anchor='e').grid(row=2, column=2)

meshFlangeWidth = tk.Entry(iSectionFrame, width=5)
meshFlangeWidth.grid(row=3, column=1)
meshFlangeWidth.insert(tk.END, "0.04")
tk.Label(iSectionFrame, width=20, text="Mesh flange width", anchor='e').grid(row=3, column=0)

meshFlangeThickness = tk.Entry(iSectionFrame, width=5)
meshFlangeThickness.grid(row=3, column=3)
meshFlangeThickness.insert(tk.END, "0.002")
tk.Label(iSectionFrame, width=20, text="Mesh flange thickness", anchor='e').grid(row=3, column=2)

meshWebThickness = tk.Entry(iSectionFrame, width=5)
meshWebThickness.grid(row=4, column=1)
meshWebThickness.insert(tk.END, "0.002")
tk.Label(iSectionFrame, width=20, text="Mesh web thickness", anchor='e').grid(row=4, column=0)

meshWebHeight = tk.Entry(iSectionFrame, width=5)
meshWebHeight.grid(row=4, column=3)
meshWebHeight.insert(tk.END, "0.04")
tk.Label(iSectionFrame, width=20, text="Mesh web height", anchor='e').grid(row=4, column=2)

##### Block Entries

blockFrame = tk.LabelFrame(window4, text="Block Entities", padx=5, pady=5)
blockFrame.grid(row=2, column=2, sticky="nsew")

cX_Block = tk.Entry(blockFrame, width=5)
cX_Block.grid(row=1, column=1)
cX_Block.insert(tk.END, "0")
tk.Label(blockFrame, width=20, text="Centroid of X", anchor='e').grid(row=1, column=0)

cY_Block = tk.Entry(blockFrame, width=5)
cY_Block.grid(row=1, column=3)
cY_Block.insert(tk.END, "0")
tk.Label(blockFrame, width=20, text="Centroid of Y", anchor='e').grid(row=1, column=2)

widthBlock = tk.Entry(blockFrame, width=5)
widthBlock.grid(row=2, column=1)
widthBlock.insert(tk.END, ".4")
tk.Label(blockFrame, width=20, text="Width of Block", anchor='e').grid(row=2, column=0)

depthBlock = tk.Entry(blockFrame, width=5)
depthBlock.grid(row=2, column=3)
depthBlock.insert(tk.END, ".4")
tk.Label(blockFrame, width=20, text="Depth of Block", anchor='e').grid(row=2, column=2)

meshWidBlock = tk.Entry(blockFrame, width=5)
meshWidBlock.grid(row=3, column=1)
meshWidBlock.insert(tk.END, "0.04")
tk.Label(blockFrame, width=20, text="Mesh along Width ", anchor='e').grid(row=3, column=0)

meshDepthBlock = tk.Entry(blockFrame, width=5)
meshDepthBlock.grid(row=3, column=3)
meshDepthBlock.insert(tk.END, "0.02")
tk.Label(blockFrame, width=20, text="Mesh along Depth", anchor='e').grid(row=3, column=2)

#########################################---END OF ENTRIES---#####################################################

j1 = 1  # counter for entities
j2 = 1  # counter for mesh
j3 = 1  # counter for node set
jNS = 1  # counter for new node set
j4 = 1  # counter for fire model
j5 = 1  # counter for heat flux
j6 = 1  # counter for recorder
j7 = 1  # counter for nodeset when User defined location is chosen
entCol = 1  # counter for entity of column
entBeam = 1  # counter for entity of beam
entTruss = 1  # counter for entity of  truss
entSlab = 1  # counter for entity of  slab
iEle = 1  # counter for the BC elements
jEle = 1  # counter for shell elements, so used for slabs in OpenSEES

##############################---Function for batchFile


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


### functions for OpesSEES entities


def iEntity(intValue, maxL, increment, centroidX, centroidY, flangeWid, flangeHeight, webThick, flangeThick):
    global j1
    while intValue < maxL:  # entities
        with open(osFile, 'a') as fileOS:
            fileOS.writelines("HTEntity \t Isection \t {0}   \t {1} \t {2} \t {3} \t {4} \t {5} "
                              "\t {6};\n".format(j1, centroidX, centroidY, flangeWid, flangeHeight, webThick,
                                                 flangeThick))
            j1 += 1
            intValue += increment
    with open(osFile, 'a') as fileOS:
        fileOS.writelines("\n")


def mesh(intValue2, maxL2, increment2, phaseChange, meshFlangeW, meshFlangeT, meshWebT, meshWidth, materialTag):
    global j2
    while intValue2 < maxL2:  # creating mesh
        with open(osFile, 'a') as fileOS:
            fileOS.writelines("HTMesh \t {0}  \t {0}  \t {6} \t -phaseChange \t {1} \t -MeshCtrls \t {2} \t {3} \t "
                              "{4} \t {5}\n".format(j2, phaseChange, meshFlangeW, meshFlangeT, meshWebT,
                                                    meshWidth, materialTag))
            j2 += 1
            intValue2 += increment2
    with open(osFile, 'a') as fileOS:
        fileOS.writelines("\nHTMeshAll;\n\n")


def nodeSETFaces(intValue3, maxL3, increment3, faces):
    global j3
    while intValue3 < maxL3:  # creating Node Set
        with open(osFile, 'a') as fileOS:
            fileOS.writelines("HTNodeSet \t {0}  \t -Entity \t {0}  \t -face \t {1}\n".format(j3, faces))
        j3 += 1
        intValue3 += increment3

    with open(osFile, 'a') as fileOS:
        fileOS.writelines("\n")


def nodeSETLoc(intValue3, maxL3, increment3, entityDepth):
    global j3
    global j7, jNS
    while intValue3 < maxL3:  # creating Node Set
        with open(osFile, 'a') as fileOS:
            webH = round(float(beamHeight.get()) - 2*float(flangeThickness.get()), 4)
            div1 = round((webH/4), 4)
            div2 = round(3*(webH/8), 4)
            div3 = round((webH/4), 4)
            div4 = round((webH/8), 4)
            if deptLocation.get() == "2":
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                  " -Locy -{1}\n".format(j3, entityDepth/2, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                  " -Locy {1}\n".format(j3, entityDepth/2, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -NodeSet {1} {2}\n".format(j3, j3-2, j3-1))

            if selectEntity.get() == "Isection":
                if deptLocation.get() == "5":
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy -{1}\n".format(j3, entityDepth/2, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy -{1}\n".format(j3, div1, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {1} \t -Locx 0.0  \t -Locy 0.0\n".format(j3, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy {1}\n".format(j3, div1, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy {1}\n".format(j3, entityDepth/2, j7))

                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -NodeSet {1} {2} {3} {4} "
                                      "{5}\n".format(j3, j3-5, j3-4, j3-3, j3-2, j3-1))

            if deptLocation.get() == "9":
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                  " -Locy -{1}\n".format(j3, entityDepth/2, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                  " -Locy -{1}\n".format(j3, div2, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                  " -Locy -{1}\n".format(j3, div3, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                  " -Locy -{1}\n".format(j3, div4, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {1} \t -Locx 0.0  \t -Locy 0.0\n".format(j3, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                  " -Locy {1}\n".format(j3, div4, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                  " -Locy {1}\n".format(j3, div3, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                  " -Locy {1}\n".format(j3, div2, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t "
                                  "-Locy {1}\n".format(j3, entityDepth/2, j7))
                j3 += 1
                fileOS.writelines("HTNodeSet \t {0} \t -NodeSet {1} {2} {3} {4} {5} {6} {7} {8} "
                                  "{9}\n".format(j3, j3-9, j3-8, j3-7, j6-6, j3-5, j3-4, j3-3, j3-2, j3-1))

            if selectEntity.get() == "Block":
                if deptLocation.get() == "5":
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy -{1}\n".format(j3, entityDepth/2, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy -{1}\n".format(j3, entityDepth/4, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {1} \t -Locx 0.0  \t -Locy 0.0\n".format(j3, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy {1}\n".format(j3, entityDepth/4, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy {1}\n".format(j3, entityDepth/2, j7))
                if deptLocation.get() == "9":
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy -{1}\n".format(j3, entityDepth/2, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy -{1}\n".format(j3, 3*entityDepth/8, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy -{1}\n".format(j3, entityDepth/4, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy -{1}\n".format(j3, entityDepth/8, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {1} \t -Locx 0.0  \t -Locy 0.0\n".format(j3, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy {1}\n".format(j3, entityDepth/8, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy {1}\n".format(j3, entityDepth/4, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t"
                                      " -Locy {1}\n".format(j3, 3*entityDepth/8, j7))
                    j3 += 1
                    fileOS.writelines("HTNodeSet \t {0} \t -HTEntity {2} \t -Locx 0.0  \t "
                                      "-Locy {1}\n".format(j3, entityDepth/2, j7))

        j3 += 1
        j7 += 1
        intValue3 += increment3

    with open(osFile, 'a') as fileOS:
        fileOS.writelines("\n")


def fireModel(intValue4, maxL4, increment4, fireType):
    global j4
    while intValue4 < maxL4:  # creating Fire Model
        with open(osFile, 'a') as fileOS:
            fileOS.writelines(
                "FireModel \t UserDefined \t {0}  \t -file \t AST{0}.dat -type {1};\n".format(j4, fireType))
            j4 += 1
            intValue4 += increment4
    with open(osFile, 'a') as fileOS:
        fileOS.writelines("\n")


def heatFlux(intValue5, maxL5, increment5, HFfaces, HTConstants):
    global j5
    while intValue5 < maxL5:  # creating Heat Flux  ### check this part carefully in OpenSEES File
        with open(osFile, 'a') as fileOS:
            fileOS.writelines("HTPattern \t fire \t {0}  \t model \t {0}  {{\nHeatFluxBC \t -HTEntity \t {0}"
                              "  \t -face {1} \t -type \t ConvecAndRad \t -HTConstants {2};\n}}\n"
                              .format(j5, HFfaces, HTConstants))
            j5 += 1
            intValue5 += increment5
    with open(osFile, 'a') as fileOS:
        fileOS.writelines("\n")


def htRecorder(intValue6, maxL6, increment6):
    global j6, jNS
    while intValue6 < maxL6:  # creating recorder
        with open(osFile, 'a') as fileOS:
            if selectNodeSet.get() == "Faces":
                fileOS.writelines("HTRecorder \t -file \t temp{0}.dat  \t -NodeSet \t {0};\n".format(j6))
            if selectNodeSet.get() == "User Defined":
                if deptLocation.get() == "2":
                    jNS = jNS + 2
                    fileOS.writelines("HTRecorder \t -file \t temp{0}.dat  \t -NodeSet \t {1};\n".format(j6, jNS))
                if deptLocation.get() == "5":
                    jNS = jNS + 5
                    fileOS.writelines("HTRecorder \t -file \t temp{0}.dat  \t -NodeSet \t {1};\n".format(j6, jNS))
                if deptLocation.get() == "9":
                    jNS = jNS + 9
                    fileOS.writelines("HTRecorder \t -file \t temp{0}.dat  \t -NodeSet \t {1};\n".format(j6, jNS))
        j6 += 1
        jNS += 1
        intValue6 += increment6


''' Below functions is for block entity, the Tag number will continue with '''


def blockEntity(intValue7, maxL7, increment7, blkCentroidX, blkCentroidY, widthBLK, depthBLK):
    global j1
    while intValue7 < maxL7:  # entities
        with open(osFile, 'a') as fileOS:
            fileOS.writelines("HTEntity \t Block \t {0}   \t {1} \t {2} \t {3} "
                              "\t {4};\n".format(j1, blkCentroidX, blkCentroidY, widthBLK, depthBLK))
            j1 += 1
            intValue7 += increment7
    with open(osFile, 'a') as fileOS:
        fileOS.writelines("\n")


def meshBLK(intValue8, maxL8, increment8, material2, phaseChange2, meshWBLK, meshDepth):
    global j2
    while intValue8 < maxL8:  # creating mesh
        with open(osFile, 'a') as fileOS:
            fileOS.writelines("HTMesh \t {0}  \t {0}  \t {1} \t -phaseChange \t {2} \t -MeshCtrls \t {3} \t {4};\n"
                              .format(j2, material2, phaseChange2, meshWBLK, meshDepth))
            j2 += 1
            intValue8 += increment8
    with open(osFile, 'a') as fileOS:
        fileOS.writelines("\nHTMeshAll;\n\n")


####################----Functions, frames and Entries for Element Sets


elementFrame = tk.LabelFrame(window4, text="Element Sets", padx=5, pady=5)
elementFrame.grid(row=3, column=2, sticky="nsew")

sectionBC = tk.Entry(elementFrame, width=10)
sectionBC.grid(row=3, column=1)
sectionBC.insert(tk.END, "$c1 $c2 $c3 $c4 $c5")
tk.Label(elementFrame, width=15, text="Section BC", anchor='e').grid(row=3, column=0)

sectionShell = tk.Entry(elementFrame, width=10)
sectionShell.grid(row=3, column=3)
sectionShell.insert(tk.END, "$s1 $s2 $s3 $s4 $s5")
tk.Label(elementFrame, width=15, text="Section Shell", anchor='e').grid(row=3, column=2)


def openNodesFile():  # opening the Nodes file before using it to write
    global nodesFile
    nodesFile = filedialog.askopenfilename(title="select a file", filetypes=(('All files', '*.*'),
                                                                             ('Text Files', ('*.txt', '*.dat'))))


tk.Button(elementFrame, text="Browse Nodes File", command=openNodesFile, width=15, height=1).grid(row=0, column=1)
tk.Label(elementFrame, width=16, text="Open Nodes File", anchor='e').grid(row=0, column=0, padx=5, pady=5)


def openElementFile():  # opening the beam-column element file before using it to write
    # noinspection PyGlobalUndefined
    global beamEleFile
    beamEleFile = filedialog.askopenfilename(
        title="select a file", filetypes=(('All files', '*.*'), ('Text Files', ('*.txt', '*.csv', '*.dat'))))


tk.Button(elementFrame, text="BC Element File", command=openElementFile, width=15, height=1).grid(row=1, column=1)
tk.Label(elementFrame, width=16, text="BC Element File", anchor='e').grid(row=1, column=0, padx=5, pady=5)


def openShellElementFile():  # opening SHELL file before using it to write
    global shellEleFile
    shellEleFile = filedialog.askopenfilename(
        title="select a file", filetypes=(('All files', '*.*'), ('Text Files', ('*.txt', '*.csv', '*.dat'))))


tk.Button(elementFrame, text="Shell Element File", command=openShellElementFile,
          width=15, height=1).grid(row=2, column=1)
tk.Label(elementFrame, width=15, text="Shell Element File", anchor='e').grid(row=2, column=0, padx=5, pady=5)


def nodesDict():  # creating dictionaries of nodes and nodes files
    global nodesFile
    createFolder('./ElementFiles')
    NODES_OUTPUT = 'ElementFiles/Nodes.csv'  # writing to make an CSV file
    NODES_OUTPUT2 = 'ElementFiles/Nodes2.csv'  # writing new files by Removing blank lines
    with open(nodesFile) as f1:
        stripped = (line.strip() for line in f1)
        lines = (line.replace("\t", ",").split() for line in stripped if line)
        csv.reader(f1, delimiter=',')
        with open(NODES_OUTPUT, 'w', newline='') as out_file:
            writer = csv.writer(out_file, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(lines)

    fn = open(NODES_OUTPUT2, 'w', newline='')
    nodeData = pd.read_csv(NODES_OUTPUT)
    first_column = nodeData.columns[0]
    nodeData = nodeData.drop([first_column], axis=1)
    nodeData.to_csv(fn, index=False)
    fn.close()
    '''this function reads all lines which are used to make list of all lines later to make dictionary '''

    def read_lines():
        with open(NODES_OUTPUT2) as file:
            reader = csv.reader(file)
            for row in reader:
                yield [float(jItem) for jItem in row]

    allLines = list(read_lines())
    global finalDict
    '''it makes a dictionary where first element is key and others are values '''
    finalDict = {nodes[0]: nodes[1:] for nodes in allLines}
    # convert key (node) as an integer and rounding all values to significant figures using ROUND (round) command

    global nodesDictionary
    nodesDictionary = {int(k): (round(X), round(Y), round(Z)) for k, (X, Y, Z) in finalDict.items()}


d1_button = tk.Button(elementFrame, text="Nodes Creation", command=nodesDict, width=15, height=1)
d1_button.grid(row=0, column=3, padx=10, pady=10)
tk.Label(elementFrame, width=15, text="Generate Nodes File", anchor='e').grid(row=0, column=2, padx=5, pady=5)


def bcElementDict():
    global beamEleFile
    createFolder('./ElementFiles')
    ELEMENT_OUTPUT = 'ElementFiles/Element.csv'
    ELEMENT_OUTPUT2 = 'ElementFiles/Element2.csv'
    with open(beamEleFile) as elementFile:
        strippedEle = (ele.strip() for ele in elementFile)
        elements = (ele.replace("\t", ",").split() for ele in strippedEle if
                    ele)  # be noted that elimination is "tab" here
        csv.reader(elementFile, delimiter=',')
        with open(ELEMENT_OUTPUT, 'w', newline='') as outFile:
            writer = csv.writer(outFile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(elements)

    beamColData = pd.read_csv(ELEMENT_OUTPUT)
    c1 = beamColData.columns[0]
    c2 = beamColData.columns[1]
    c6 = beamColData.columns[5]
    c7 = beamColData.columns[6]
    c8 = beamColData.columns[7]
    c9 = beamColData.columns[8]
    c10 = beamColData.columns[9]

    fn2 = open(ELEMENT_OUTPUT2, 'w', newline='')
    beamColData = beamColData.drop([c1, c2, c6, c7, c8, c9, c10], axis=1)
    beamColData.to_csv(fn2, index=False)
    fn2.close()

    def read_lines2():
        with open(ELEMENT_OUTPUT2) as file2:
            reader2 = csv.reader(file2)
            for row3 in reader2:
                yield [int(k) for k in row3]

    elementSet = list(read_lines2())
    global bcEleDictionary
    # making elements as dictionary where elements are keys and corresponding nodes are values
    bcEleDictionary = {elekey[0]: elekey[1:] for elekey in elementSet}


tk.Button(elementFrame, text="BC Elements ", command=bcElementDict, width=15, height=1).grid(row=1, column=3)
tk.Label(elementFrame, width=15, text="BC Element File", anchor='e').grid(row=1, column=2, padx=5, pady=5)


def shellElementDict():
    # noinspection PyGlobalUndefined
    global shellEleFile
    createFolder('./ElementFiles')
    SHELL_ELEMENT_OUTPUT = 'ElementFiles/Element3.csv'
    SHELL_ELEMENT_OUTPUT2 = 'ElementFiles/Element4.csv'
    with open(shellEleFile) as elementFile:
        strippedEle = (ele.strip() for ele in elementFile)
        elements = (ele.replace("\t", ",").split() for ele in strippedEle if
                    ele)  # be noted that elimination is space here
        csv.reader(elementFile, delimiter=',')
        with open(SHELL_ELEMENT_OUTPUT, 'w', newline='') as outFile:
            writer = csv.writer(outFile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerows(elements)

    shellData = pd.read_csv(SHELL_ELEMENT_OUTPUT)
    cS1 = shellData.columns[0]
    cS2 = shellData.columns[1]
    cS3 = shellData.columns[7]
    fnSE = open(SHELL_ELEMENT_OUTPUT2, 'w', newline='')
    shellData = shellData.drop([cS1, cS2, cS3], axis=1)
    shellData.to_csv(fnSE, index=False)
    fnSE.close()

    def read_lines2():
        with open(SHELL_ELEMENT_OUTPUT2) as file3:
            reader2 = csv.reader(file3)
            for row3 in reader2:
                yield [int(jSE) for jSE in row3]

    elementSet2 = list(read_lines2())
    # noinspection PyGlobalUndefined
    global shellEleDictionary
    shellEleDictionary = {elekey[0]: elekey[1:] for elekey in elementSet2}


tk.Button(elementFrame, text="Shell Element File", command=shellElementDict, width=15, height=1).grid(row=2, column=3)
tk.Label(elementFrame, width=15, text="Create Shell Elements", anchor='e').grid(row=2, column=2, padx=5, pady=5)


def nodes1():  # this method is for columns
    matchingNodes = [key for key, (X, Y, Z) in nodesDictionary.items()
                     if (X == float(x_Column.get())) and (Y == float(y_Column.get())) and
                     (lowerValColumn <= Z <= upperValColumn)]
    return matchingNodes


def nodes4():  #  this method is for Longitudinal Beam
    matchingNodes = [key for key, (X, Y, Z) in nodesDictionary.items()
                     if (beginXBeam <= X <= beginXBeam + float(incX_Beam.get()) and
                         (beginYBeam <= Y <= beginYBeam + float(incY_Beam.get())) and Z == float(z_Beam.get()))]
    return matchingNodes


def nodes7():  # this method is for Slabs
    matchingNodes = [key for key, (X, Y, Z) in nodesDictionary.items()
                     if beginXslab <= X <= beginXslab + float(incX_slab.get()) and
                     beginYSlab <= Y <= beginYSlab + float(incY_slab.get()) and Z == float(z_slab.get())]
    return matchingNodes


def nodes8():  # this is for Trusses in both X and Y direction
    matchingNodes = [key for key, (X, Y, Z) in nodesDictionary.items()
                     if beginXTruss <= X <= beginXTruss + float(incXTruss.get()) and
                     beginYTruss <= Y <= beginYTruss + float(incYTruss.get()) and
                     float(lLimitTruss.get()) <= Z <= float(uLimitTruss.get())]
    return matchingNodes


# main Output for saving all data


def output():    # main function to generate batch file
    global iEle
    global jEle
    if choose.get() == "Yes":
        if clicked6.get() == "Columns":
            k = float(z_Column.get()) + float(inc_Column.get())/2
            while k <= float(columnHeight.get()):
                xN = float(x_Column.get()) + float(mesh.get())/2
                yN = float(y_Column.get()) + float(mesh.get())/2
                zN = k + float(mesh.get())/2
                batchFile(float(x_Column.get()), xN, float(y_Column.get()), yN, k, zN, inc_Column.get())
                k += float(inc_Column.get())

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

    ##########################################-----functions for OpenSEES files

    if clicked6.get() == "Columns":
        global entCol
        initialZ = float(z_Column.get())
        heightColumn = float(columnHeight.get())
        increment_Z = float(inc_Column.get())
        with open(osFile, 'a') as f3:
            f3.writelines("\n#This is Column {0}\n\n".format(entCol))
        if selectEntity.get() == "Isection":
            iEntity(initialZ, heightColumn, increment_Z, float(cX_iSec.get()), float(cY_iSec.get()),
                    float(flangeWidth.get()), float(beamHeight.get()), float(webThickness.get()),
                    float(flangeThickness.get()))
            mesh(initialZ, heightColumn, increment_Z, int(pChange.get()), float(meshFlangeWidth.get()),
                 float(meshFlangeThickness.get()), float(meshWebThickness.get()), float(meshWebHeight.get()),
                 int(modelMatTag.get()))

        if selectEntity.get() == "Block":
            blockEntity(initialZ, heightColumn, increment_Z, float(cX_Block.get()), float(cY_Block.get()),
                        float(widthBlock.get()), float(depthBlock.get()))
            meshBLK(initialZ, heightColumn, increment_Z, modelMatTag.get(), pChange.get(),
                    float(meshWidBlock.get()), float(meshDepthBlock.get()))

        if selectNodeSet.get() == "Faces":
            nodeSETFaces(initialZ, heightColumn, increment_Z, Nodeset.get())
        if selectNodeSet.get() == "User Defined":
            if selectEntity.get() == "Isection":
                nodeSETLoc(initialZ, heightColumn, increment_Z, float(beamHeight.get()))
            if selectEntity.get() == "Block":
                nodeSETLoc(initialZ, heightColumn, increment_Z, float(depthBlock.get()))

        fireModel(initialZ, heightColumn, increment_Z, fireModelType.get())
        heatFlux(initialZ, heightColumn, increment_Z, hfFaces.get(), modelHT_Tag.get())
        htRecorder(initialZ, heightColumn, increment_Z)
        entCol += 1

    if clicked6.get() == "Beam":
        global entBeam
        if incrementDirectionBEAM.get() == "X":
            beginY_BEAM = float(y_Beam.get())
            incrementY_BEAM = float(incY_Beam.get())
            widthBEAM = float(y_LenBeam.get())
            while beginY_BEAM < widthBEAM:
                beginX_BEAM = float(x_Beam.get())
                lengthBEAM = float(x_LenBeam.get())
                incrementXBeam = float(incX_Beam.get())
                with open(osFile, 'a') as f3:
                    f3.writelines("\n#This is Beam {0}\n\n".format(entBeam))
                if selectEntity.get() == "Isection":
                    iEntity(beginX_BEAM, lengthBEAM, incrementXBeam, float(cX_iSec.get()), float(cY_iSec.get()),
                            float(flangeWidth.get()), float(beamHeight.get()), float(webThickness.get()),
                            float(flangeThickness.get()))
                    mesh(beginX_BEAM, lengthBEAM, incrementXBeam, int(pChange.get()), float(meshFlangeWidth.get()),
                         float(meshFlangeThickness.get()), float(meshWebThickness.get()), float(meshWebHeight.get()),
                         int(modelMatTag.get()))

                if selectEntity.get() == "Block":
                    blockEntity(beginX_BEAM, lengthBEAM, incrementXBeam, float(cX_Block.get()), float(cY_Block.get()),
                                float(widthBlock.get()), float(depthBlock.get()))
                    meshBLK(beginX_BEAM, lengthBEAM, incrementXBeam, modelMatTag.get(), pChange.get(),
                            float(meshWidBlock.get()), float(meshDepthBlock.get()))

                if selectNodeSet.get() == "Faces":
                    nodeSETFaces(beginX_BEAM, lengthBEAM, incrementXBeam, Nodeset.get())
                if selectNodeSet.get() == "User Defined":
                    if selectEntity.get() == "Isection":
                        nodeSETLoc(beginX_BEAM, lengthBEAM, incrementXBeam, float(beamHeight.get()))
                    if selectEntity.get() == "Block":
                        nodeSETLoc(beginX_BEAM, lengthBEAM, incrementXBeam, float(depthBlock.get()))

                fireModel(beginX_BEAM, lengthBEAM, incrementXBeam, fireModelType.get())
                heatFlux(beginX_BEAM, lengthBEAM, incrementXBeam, hfFaces.get(), modelHT_Tag.get())
                htRecorder(beginX_BEAM, lengthBEAM, incrementXBeam)
                entBeam += 1
                beginY_BEAM += incrementY_BEAM

        if incrementDirectionBEAM.get() == "Y":
            beginX_BEAM = float(x_Beam.get())
            lengthBEAM = float(x_LenBeam.get())
            incrementXBeam = float(incX_Beam.get())
            while beginX_BEAM < lengthBEAM:
                beginY_BEAM = float(y_Beam.get())
                incrementY_BEAM = float(incY_Beam.get())
                widthBEAM = float(y_LenBeam.get())
                with open(osFile, 'a') as f3:
                    f3.writelines("\n#This is Beam {0}\n\n".format(entBeam))
                if selectEntity.get() == "Isection":
                    iEntity(beginY_BEAM, widthBEAM, incrementY_BEAM, float(cX_iSec.get()), float(cY_iSec.get()),
                            float(flangeWidth.get()), float(beamHeight.get()), float(webThickness.get()),
                            float(flangeThickness.get()))
                    mesh(beginY_BEAM, widthBEAM, incrementY_BEAM, int(pChange.get()), float(meshFlangeWidth.get()),
                         float(meshFlangeThickness.get()), float(meshWebThickness.get()), float(meshWebHeight.get()),
                         int(modelMatTag.get()))

                if selectEntity.get() == "Block":
                    blockEntity(beginY_BEAM, widthBEAM, incrementY_BEAM, float(cX_Block.get()), float(cY_Block.get()),
                                float(widthBlock.get()), float(depthBlock.get()))
                    meshBLK(beginY_BEAM, widthBEAM, incrementY_BEAM, modelMatTag.get(), pChange.get(),
                            float(meshWidBlock.get()), float(meshDepthBlock.get()))

                if selectNodeSet.get() == "Faces":
                    nodeSETFaces(beginY_BEAM, widthBEAM, incrementY_BEAM, Nodeset.get())
                if selectNodeSet.get() == "User Defined":
                    if selectEntity.get() == "Isection":
                        nodeSETLoc(beginY_BEAM, widthBEAM, incrementY_BEAM, float(beamHeight.get()))
                    if selectEntity.get() == "Block":
                        nodeSETLoc(beginY_BEAM, widthBEAM, incrementY_BEAM, float(depthBlock.get()))

                fireModel(beginY_BEAM, widthBEAM, incrementY_BEAM, fireModelType.get())
                heatFlux(beginY_BEAM, widthBEAM, incrementY_BEAM, hfFaces.get(), modelHT_Tag.get())
                htRecorder(beginY_BEAM, widthBEAM, incrementY_BEAM)
                entBeam += 1
                beginX_BEAM += incrementXBeam

    if clicked6.get() == "Truss":
        global entTruss
        if incrementDirectionTRUSS.get() == "X":
            beginY_Truss = float(yTruss.get())
            incrementY_Truss = float(incYTruss.get())
            widthTruss = float(Y_lenTruss.get())
            while beginY_Truss < widthTruss:
                beginX_Truss = float(xTruss.get())
                lengthTruss = float(X_lenTruss.get())
                incrementXTruss = float(incXTruss.get())
                with open(osFile, 'a') as f3:
                    f3.writelines("\n#This is Truss {0}\n\n".format(entTruss))
                if selectEntity.get() == "Isection":
                    iEntity(beginX_Truss, lengthTruss, incrementXTruss, float(cX_iSec.get()), float(cY_iSec.get()),
                            float(flangeWidth.get()), float(beamHeight.get()), float(webThickness.get()),
                            float(flangeThickness.get()))
                    mesh(beginX_Truss, lengthTruss, incrementXTruss, int(pChange.get()), float(meshFlangeWidth.get()),
                         float(meshFlangeThickness.get()), float(meshWebThickness.get()), float(meshWebHeight.get()),
                         int(modelMatTag.get()))

                if selectEntity.get() == "Block":
                    blockEntity(beginX_Truss, lengthTruss, incrementXTruss, float(cX_Block.get()), float(cY_Block.get()),
                                float(widthBlock.get()), float(depthBlock.get()))
                    meshBLK(beginX_Truss, lengthTruss, incrementXTruss, modelMatTag.get(), pChange.get(),
                            float(meshWidBlock.get()), float(meshDepthBlock.get()))

                if selectNodeSet.get() == "Faces":
                    nodeSETFaces(beginX_Truss, lengthTruss, incrementXTruss, Nodeset.get())
                if selectNodeSet.get() == "User Defined":
                    if selectEntity.get() == "Isection":
                        nodeSETLoc(beginX_Truss, lengthTruss, incrementXTruss, float(beamHeight.get()))
                    if selectEntity.get() == "Block":
                        nodeSETLoc(beginX_Truss, lengthTruss, incrementXTruss, float(depthBlock.get()))

                fireModel(beginX_Truss, lengthTruss, incrementXTruss, fireModelType.get())
                heatFlux(beginX_Truss, lengthTruss, incrementXTruss, hfFaces.get(), modelHT_Tag.get())
                htRecorder(beginX_Truss, lengthTruss, incrementXTruss)
                entTruss += 1
                beginY_Truss += incrementY_Truss

        if incrementDirectionTRUSS.get() == "Y":
            beginX_Truss = float(xTruss.get())
            lengthTruss = float(X_lenTruss.get())
            incrementXTruss = float(incXTruss.get())
            while beginX_Truss < lengthTruss:
                beginY_Truss = float(yTruss.get())
                incrementY_Truss = float(incYTruss.get())
                widthTruss = float(Y_lenTruss.get())
                with open(osFile, 'a') as f3:
                    f3.writelines("\n#This is Truss {0}\n\n".format(entTruss))
                if selectEntity.get() == "Isection":
                    iEntity(beginY_Truss, widthTruss, incrementY_Truss, float(cX_iSec.get()), float(cY_iSec.get()),
                            float(flangeWidth.get()), float(beamHeight.get()), float(webThickness.get()),
                            float(flangeThickness.get()))
                    mesh(beginY_Truss, widthTruss, incrementY_Truss, int(pChange.get()), float(meshFlangeWidth.get()),
                         float(meshFlangeThickness.get()), float(meshWebThickness.get()), float(meshWebHeight.get()),
                         int(modelMatTag.get()))

                if selectEntity.get() == "Block":
                    blockEntity(beginY_Truss, widthTruss, incrementY_Truss, float(cX_Block.get()), float(cY_Block.get()),
                                float(widthBlock.get()), float(depthBlock.get()))
                    meshBLK(beginY_Truss, widthTruss, incrementY_Truss, modelMatTag.get(), pChange.get(),
                            float(meshWidBlock.get()), float(meshDepthBlock.get()))

                if selectNodeSet.get() == "Faces":
                    nodeSETFaces(beginY_Truss, widthTruss, incrementY_Truss, Nodeset.get())
                if selectNodeSet.get() == "User Defined":
                    if selectEntity.get() == "Isection":
                        nodeSETLoc(beginY_Truss, widthTruss, incrementY_Truss, float(beamHeight.get()))
                    if selectEntity.get() == "Block":
                        nodeSETLoc(beginY_Truss, widthTruss, incrementY_Truss, float(depthBlock.get()))

                fireModel(beginY_Truss, widthTruss, incrementY_Truss, fireModelType.get())
                heatFlux(beginY_Truss, widthTruss, incrementY_Truss, hfFaces.get(), modelHT_Tag.get())
                htRecorder(beginY_Truss, widthTruss, incrementY_Truss,)
                entTruss += 1
                beginX_Truss += incrementXTruss

    if clicked6.get() == "Slabs":
        global entSlab
        if incrementDirectionSLB.get() == "X":
            beginY_Slab = float(y_slab.get())
            incrementYSLAB = float(incY_slab.get())
            widthSLAB = float(widthY_slab.get())
            while beginY_Slab < widthSLAB:
                beginX_Slab = float(xInt_slab.get())
                lengthXSlab = float(xLen_slab.get())
                incrementXSLAB = float(incX_slab.get())
                with open(osFile, 'a') as f3:
                    f3.writelines("\n#This is Slab {0}\n\n".format(entSlab))
                if selectEntity.get() == "Block":
                    blockEntity(beginX_Slab, lengthXSlab, incrementXSLAB, float(cX_Block.get()), float(cY_Block.get()),
                                float(widthBlock.get()), float(depthBlock.get()))
                    meshBLK(beginX_Slab, lengthXSlab, incrementXSLAB, modelMatTag.get(), pChange.get(),
                            float(meshWidBlock.get()), float(meshDepthBlock.get()))

                if selectNodeSet.get() == "Faces":
                    nodeSETFaces(beginX_Slab, lengthXSlab, incrementXSLAB, Nodeset.get())
                if selectNodeSet.get() == "User Defined":
                    nodeSETLoc(beginX_Slab, lengthXSlab, incrementXSLAB, float(depthBlock.get()))

                fireModel(beginX_Slab, lengthXSlab, incrementXSLAB, fireModelType.get())
                heatFlux(beginX_Slab, lengthXSlab, incrementXSLAB, hfFaces.get(), modelHT_Tag.get())
                htRecorder(beginX_Slab, lengthXSlab, incrementXSLAB)
                entSlab += 1
                beginY_Slab += incrementYSLAB

        if incrementDirectionSLB.get() == "Y":
            beginX_Slab = float(xInt_slab.get())
            lengthXSlab = float(xLen_slab.get())
            incrementXSLAB = float(incX_slab.get())
            while beginX_Slab < lengthXSlab:
                beginY_Slab = float(y_slab.get())
                incrementYSLAB = float(incY_slab.get())
                widthSLAB = float(widthY_slab.get())
                with open(osFile, 'a') as f3:
                    f3.writelines("\n#This is Slab {0}\n\n".format(entSlab))
                if selectEntity.get() == "Block":
                    blockEntity(beginY_Slab, widthSLAB, incrementYSLAB, float(cX_Block.get()), float(cY_Block.get()),
                                float(widthBlock.get()), float(depthBlock.get()))
                    meshBLK(beginY_Slab, widthSLAB, incrementYSLAB, modelMatTag.get(), pChange.get(),
                            float(meshWidBlock.get()), float(meshDepthBlock.get()))

                if selectNodeSet.get() == "Faces":
                    nodeSETFaces(beginY_Slab, widthSLAB, incrementYSLAB, Nodeset.get())
                if selectNodeSet.get() == "User Defined":
                    nodeSETLoc(beginY_Slab, widthSLAB, incrementYSLAB, float(depthBlock.get()))

                fireModel(beginY_Slab, widthSLAB, incrementYSLAB, fireModelType.get())
                heatFlux(beginY_Slab, widthSLAB, incrementYSLAB, hfFaces.get(), modelHT_Tag.get())
                htRecorder(beginY_Slab, widthSLAB, incrementYSLAB,)
                entSlab += 1
                beginX_Slab += incrementXSLAB

    # functions to use searching algorithms for th elements

    if elementSetGen.get() == "Yes":   # here we write a file for element generation
        global jEle, ELEMENT_SET_COL, ELEMENT_SET2, ELEMENT_SET_BEAM, ELEMENT_SET_Truss
        global onlySlabEle, onlySlabEle, onlyBeamEle, onlyTrussEle

        def eleDictionaryBC(getClass):
            global elementListBC
            setX = getClass  # calling functions(methods) from the class
            fullSet = set(setX)  # all nodes are changed into a set
            elementListBC = [key for key, value in bcEleDictionary.items()
                             if set(value).issubset(fullSet)]

        def eleDictionaryShell(getClass):  # this method generate the element list which is copied in ele_set_gen method
            global elementListShell
            setX = getClass  # calling functions(methods) from the class
            fullSet = set(setX)  # all nodes are changed into a set
            elementListShell = [key for key, value in shellEleDictionary.items()
                                if set(value).issubset(fullSet)]

        def ele_set_genBeamThermal(counter, member):
            with open(ELEMENT_SET2, 'a', newline='') as EleSet2:
                EleSet2.write("\n\n#This is ElementSet{0} for {1}\n".format(counter, member))
                for iItem in range(0, len(elementListBC), 1):  # step by threes.
                    f = str(elementListBC[iItem:iItem + 1])[1:-1]  # it removes the square brackets
                    EleSet2.write('\n eleLoad -ele {0} -type -beamThermal -source "temp{1}.dat" {2}'
                                  .format(f, counter, sectionBC.get()))

        def ele_set_genShellThermal(counter, member):
            with open(ELEMENT_SET2, 'a', newline='') as EleSet2:
                EleSet2.write("\n\n#This is ElementSet{0} for {1}".format(counter, member))
                for iItem in range(0, len(elementListShell), 1):  # step by threes.
                    f = str(elementListShell[iItem:iItem + 1])[1:-1]  # it removes the square brackets
                    EleSet2.write('\n eleLoad -ele {0} -type -shellThermal -source "temp{1}.dat" {2}'
                                  .format(f, counter, sectionShell.get()))

        def ele_set_genCol(counter):   # this method generate file  and write on the file, will take 2 items in each line
            with open(ELEMENT_SET_COL, 'a', newline='') as EleSet:
                EleSet.write("\n#This is ElementSet{0} for Columns\n".format(counter))
                writer = csv.writer(EleSet)
                writer.writerow(elementListBC)

        def ele_set_genBeam(counter):   # this method generate file  and write on the file, will take 2 items in each line
            with open(ELEMENT_SET_BEAM, 'a', newline='') as EleSet:
                EleSet.write("\n#This is ElementSet{0} for Beam\n".format(counter))
                writer = csv.writer(EleSet)
                writer.writerow(elementListBC)

        def ele_set_genTruss(counter):   # this method generate file  and write on the file, will take 2 items in each line
            with open(ELEMENT_SET_Truss, 'a', newline='') as EleSet:
                EleSet.write("\n#This is ElementSet{0} for Truss\n".format(counter))
                writer = csv.writer(EleSet)
                writer.writerow(elementListBC)

        def ele_set_genBTCol(counter):
            with open(onlyColEle, 'a', newline='') as EleSet2:
                EleSet2.write("\n\n#This is ElementSet{0} for Columns\n".format(counter))
                for iItem in range(0, len(elementListBC), 1):  # step by threes.
                    f = str(elementListBC[iItem:iItem + 1])[1:-1]  # it removes the square brackets
                    EleSet2.write('\n eleLoad -ele {0} -type -beamThermal -source "temp{1}.dat" {2}'
                                  .format(f, counter, sectionBC.get()))

        def ele_set_genBTTruss(counter):
            with open(onlyTrussEle, 'a', newline='') as EleSet2:
                EleSet2.write("\n\n#This is ElementSet{0} for Truss\n".format(counter))
                for iItem in range(0, len(elementListBC), 1):  # step by threes.
                    f = str(elementListBC[iItem:iItem + 1])[1:-1]  # it removes the square brackets
                    EleSet2.write('\n eleLoad -ele {0} -type -beamThermal -source "temp{1}.dat" {2}'
                                  .format(f, counter, sectionBC.get()))

        def ele_set_genBTBeam(counter):
            with open(onlyBeamEle, 'a', newline='') as EleSet2:
                EleSet2.write("\n\n#This is ElementSet{0} for Beam\n".format(counter))
                for iItem in range(0, len(elementListBC), 1):  # step by threes.
                    f = str(elementListBC[iItem:iItem + 1])[1:-1]  # it removes the square brackets
                    EleSet2.write('\n eleLoad -ele {0} -type -beamThermal -source "temp{1}.dat" {2}'
                                  .format(f, counter, sectionBC.get()))

        def ele_set_genSTSlab(counter):
            with open(onlySlabEle, 'a', newline='') as EleSet2:
                EleSet2.write("\n\n#This is ElementSet{0} for Slab".format(counter))
                for iItem in range(0, len(elementListShell), 1):  # step by threes.
                    f = str(elementListShell[iItem:iItem + 1])[1:-1]  # it removes the square brackets
                    EleSet2.write('\n eleLoad -ele {0} -type -shellThermal -source "temp{1}.dat" {2}'
                                  .format(f, counter, sectionShell.get()))

        if clicked6.get() == "Columns":  # ----------For Columns
            global columnBegin, lowerValColumn, upperValColumn
            columnBegin = float(z_Column.get())
            while columnBegin < float(columnHeight.get()):
                lowerValColumn = columnBegin
                upperValColumn = columnBegin + float(inc_Column.get())
                eleDictionaryBC(nodes1())
                ele_set_genBeamThermal(iEle, "Columns")
                ele_set_genBTCol(iEle)
                ele_set_genCol(iEle)
                columnBegin += float(inc_Column.get())
                iEle += 1

        if clicked6.get() == "Beam":  # ----------For Truss when many truss within one region are taken
            global beginXBeam, beginYBeam
            if incrementDirectionBEAM.get() == "X":
                beginYBeam = float(y_Beam.get())
                while beginYBeam < float(y_LenBeam.get()):
                    beginXBeam = float(x_Beam.get())
                    while beginXBeam < float(x_LenBeam.get()):
                        eleDictionaryBC(nodes4())
                        ele_set_genBeamThermal(iEle, "Beam")
                        ele_set_genBeam(iEle)
                        ele_set_genBeam(iEle)
                        beginXBeam += float(incX_Beam.get())
                        jEle += 1
                        iEle += 1
                    beginYBeam += float(incY_Beam.get())

            if incrementDirectionBEAM.get() == "Y":
                beginXBeam = float(x_Beam.get())
                while beginXBeam < float(x_LenBeam.get()):
                    beginYBeam = float(y_Beam.get())
                    while beginYBeam < float(y_LenBeam.get()):
                        eleDictionaryBC(nodes4())
                        ele_set_genBeamThermal(iEle, "Beam")
                        ele_set_genBTBeam(iEle)
                        ele_set_genBeam(iEle)
                        beginYBeam += float(incY_Beam.get())
                        jEle += 1
                        iEle += 1
                    beginXBeam += float(incX_Beam.get())

        if clicked6.get() == "Truss":  # ----------For Truss when many truss within one region are taken
            global beginXTruss, beginYTruss
            if incrementDirectionTRUSS.get() == "X":
                beginYTruss = float(yTruss.get())
                while beginYTruss < float(Y_lenTruss.get()):
                    beginXTruss = float(xTruss.get())
                    while beginXTruss < float(X_lenTruss.get()):
                        eleDictionaryBC(nodes8())
                        ele_set_genBeamThermal(iEle, "Truss")
                        ele_set_genBTTruss(iEle)
                        ele_set_genTruss(iEle)
                        beginXTruss += float(incXTruss.get())
                        jEle += 1
                        iEle += 1
                    beginYTruss += float(incYTruss.get())

            if incrementDirectionTRUSS.get() == "Y":
                beginXTruss = float(xTruss.get())
                while beginXTruss < float(X_lenTruss.get()):
                    beginYTruss = float(yTruss.get())
                    while beginYTruss < float(Y_lenTruss.get()):
                        eleDictionaryBC(nodes8())
                        ele_set_genBeamThermal(iEle, "Truss")
                        ele_set_genBTTruss(iEle)
                        ele_set_genTruss(iEle)
                        beginYTruss += float(incYTruss.get())
                        jEle += 1
                        iEle += 1
                    beginXTruss += float(incXTruss.get())

        if clicked6.get() == "Slabs":  # ----------For Slabs
            global beginXslab, beginYSlab
            if incrementDirectionSLB.get() == "X":
                beginYSlab = float(y_slab.get())
                while beginYSlab < float(widthY_slab.get()):
                    beginXslab = float(xInt_slab.get())
                    while beginXslab < float(xLen_slab.get()):
                        eleDictionaryShell(nodes7())
                        ele_set_genShellThermal(iEle, "Slabs")
                        ele_set_genSTSlab(iEle)
                        beginXslab += float(incX_slab.get())
                        jEle += 1
                        iEle += 1
                    beginYSlab += float(incY_slab.get())

            if incrementDirectionSLB.get() == "Y":
                beginXslab = float(xInt_slab.get())
                while beginXslab < float(xLen_slab.get()):
                    beginYSlab = float(y_slab.get())
                    while beginYSlab < float(widthY_slab.get()):
                        eleDictionaryShell(nodes7())
                        ele_set_genShellThermal(iEle, "Slabs")
                        beginYSlab += float(incY_slab.get())
                        jEle += 1
                        iEle += 1
                    beginXslab += float(incX_slab.get())


File_Generation = tk.Button(window4, text="Generate Batch File", command=output, width=15, height=1)\
    .grid(row=5, column=2, padx=5, pady=5)


######################---Defining HT Analysis

frameHTAnalysis = tk.LabelFrame(window4, text="HT Analysis Inputs", padx=5, pady=5)
frameHTAnalysis.grid(row=4, column=2, sticky="nsew")

initialTemp = tk.Entry(frameHTAnalysis, width=10)
initialTemp.grid(row=0, column=1)
initialTemp.insert(tk.END, "293.15")
tk.Label(frameHTAnalysis, width=15, text="Initial Temperature", anchor='e').grid(row=0, column=0)

simTime = tk.Entry(frameHTAnalysis, width=10)
simTime.grid(row=0, column=3)
simTime.insert(tk.END, "200")
tk.Label(frameHTAnalysis, width=15, text="Simulation Time", anchor='e').grid(row=0, column=2)

simTimeStep = tk.Entry(frameHTAnalysis, width=10)
simTimeStep.grid(row=1, column=1)
simTimeStep.insert(tk.END, "15")
tk.Label(frameHTAnalysis, width=15, text="Time Step", anchor='e').grid(row=1, column=0)


def savingHTFile():  # it allows the user to proceed the chooses module
    with open(osFile, 'a') as fileOS:
        fileOS.writelines("\nSetInitialT {};\n".format(initialTemp.get()))
        fileOS.writelines("\nHTAnalysis HeatTransfer TempIncr 0.1 1000 2 Newton\n")
        fileOS.writelines("HTAnalyze {0} {1};\n".format(simTime.get(), simTimeStep.get()))
        fileOS.writelines("wipe;\n\n")


tk.Button(frameHTAnalysis, text="Save HT File", command=savingHTFile, width=10, height=1).grid(row=1, column=3)


def elementLoad():
    global onlyTrussEle, finalTrussEle, ELEMENT_SET_COL, ELEMENT_SET_Truss
    lines = np.loadtxt(ELEMENT_SET_COL, comments="#", delimiter=",", unpack=False)
    a1 = np.array(lines)
    lines2 = np.loadtxt(ELEMENT_SET_Truss, comments="#", delimiter=",", unpack=False)
    a2 = np.array(lines2)
    y = np.intersect1d(a1, a2)
    myList = [int(x) for x in y]
    dupItems = list(map(str, myList))
    print(myList)

    def should_remove_line(line, stop_words):
        return any([word in line for word in stop_words])

    with open(onlyTrussEle) as f, open(finalTrussEle, "w") as working:
        for line in f:
            if not should_remove_line(line, dupItems):
                working.write(line)

    eleFileList = [onlyColEle, onlyBeamEle, finalTrussEle, onlySlabEle]

    with open(Final_EleSET2, 'w') as finalFile:
        for fname in eleFileList:
            try:
                open(fname, 'r')
            except IOError:
                open(fname, 'w')
            with open(fname) as infile:
                for line in infile:
                    finalFile.write(line)


tk.Button(window4, text="Update Ele. Load", command=elementLoad, width=15, height=1).grid(row=8, column=2, padx=5, pady=5)


# this is a frame for the entries of files and options for the user to chose the devices
infoFrame = tk.LabelFrame(window4, text="Information", relief=tk.SUNKEN)
infoFrame.grid(row=8, column=0, sticky="nsew")

tk.Label(infoFrame, width=50, text="Run in Terminal (Linux or MacOX),use (chmod +x BatchFile.command)", anchor='w') \
    .grid(row=15, column=0, columnspan=4, padx=5, pady=5)
tk.Label(infoFrame, width=40, text=" and in the next line run the batch file with ", anchor='w') \
    .grid(row=16, column=0, columnspan=4, padx=5, pady=5)
tk.Label(infoFrame, width=40, text=".\Batchfile.command", anchor='w') \
    .grid(row=17, column=0, columnspan=4, padx=5, pady=5)


window4.mainloop()
