
import os


def createFolder(directory):  # creating folders in the directory
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating Directory.' + directory)


createFolder('./Batchfile')  # give any folder name

fdsPr = "fds2ascii << EOF"  # to call fds2ascii
fdsFile = "Validation_BNDF"
plt3d = 1  # data from plt3d file, it should be 2 for slice data
SF = 1  # for all data
domain = "y"  # all data to with in a range "n" for all data
Var = 1  # change it according to the quantity required (Var represents the variable of the interest )
EOF = "EOF"  # end of the command
i = 1  # it gives index to the output files from fds2ascii if indexing is continuous
maxT = 300
timInt = 10
t = 0
Xmin = 0  # minimum value of FDS Domain
Xmax = 30  # minimum value of FDS Domain
Ymin = 0  # minimum value of FDS Domain
Ymax = 30  # minimum value of FDS Domain
Zmin = 0  # minimum value of FDS Domain
Zmax = 4  # minimum value of FDS Domain

DevNo = int(input("Device Number\n"))
X = float(input("Provide X coordinate\n"))
Y = float(input("Provide Y coordinate\n"))
Z = float(input("Provide Z coordinate\n"))
mIndex = 1

batchfile = "Batchfile/Batchfile.txt"

if Xmin <= X <= float(Xmax/2) and Ymin <= Y <= float(Ymax/2) and Zmin <= Z <= float(Zmax/2):
    mIndex = 1
if Xmin <= X <= float(Xmax/2) and Ymin <= Y <= float(Ymax/2) and float(Zmax/2) < Z <= Zmax:
    mIndex = 2
if Xmin <= X <= float(Xmax/2) and float(Ymax/2) <= Y <= Ymax and Zmin <= Z <= float(Zmax/2):
    mIndex = 3
if Xmin <= X <= float(Xmax/2) and float(Ymax/2) <= Y <= Ymax and float(Zmax/2) < Z <= Zmax:
    mIndex = 4
if float(Xmax/2) <= X <= Xmax/2 and Ymin <= Y <= float(Ymax/2) and Zmin <= Z <= float(Zmax/2):
    mIndex = 5
if float(Xmax/2) <= X <= Xmax/2 and Ymin <= Y <= float(Ymax/2) and float(Zmax/2) < Z <= Zmax:
    mIndex = 6
if float(Xmax/2) <= X <= Xmax/2 and float(Ymax/2) <= Y <= Ymax and Zmin <= Z <= float(Zmax/2):
    mIndex = 7
if float(Xmax/2) <= X <= Xmax/2 and float(Ymax/2) <= Y <= Ymax and float(Zmax/2) < Z <= Zmax:
    mIndex = 8

X2 = X + 0.0005
Y2 = Y + 0.0005
Z2 = Z + 0.0005

with open(batchfile, 'a') as fb1:
    fb1.writelines("{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n{9}\n{10}\n".format(fdsPr, fdsFile, plt3d, SF, "y", X, X2, Y, Y2, Z, Z2))

dt = timInt
while t < maxT:
    with open(batchfile, 'a') as fb1:
        out = "Dev{0}_{1}.csv".format(DevNo, i)  # file name which will come after the program run in FDS2ASCII
        fb1.writelines("{0}\n{1}\n".format(mIndex, out))
        t += dt
        i += 1
        mIndex += 8

with open(batchfile, 'a') as fb1:
    fb1.writelines("EOF\n".format())
