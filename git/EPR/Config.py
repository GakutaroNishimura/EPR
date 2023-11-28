import math
import datetime
import os
import Const as const
import FileInfo

# start time
const.StartTime = datetime.datetime.now()
t = datetime.datetime.now()
year = t.year
month = t.month
day = t.day

Save_or_View = "View"
Bin_or_Float = "Float"


####################################################
# AFPNMR
# Path name
if Save_or_View == "Save":
    DirectryNameDate = "/Data/" + str(year) + "/" + str(month).zfill(2) + str(day).zfill(2)
    DataDirectryName = "/131Xe_100A_19kHz/run1/"
    DataPath         = "./" + DirectryNameDate + DataDirectryName


#DataDirectryName = "/Data/2023/0616/131Xe_234A_19kHz/run2/"
#DataDirectryName = "/Data/2023/0608/131Xe_100A_19kHz/run1/"
#DataDirectryName = "/Data/2023/0614/129Xe_069A_19kHz/run3/"
#DataDirectryName = "/Data/2023/0614/129Xe_067A_18.3kHz/run1/"
#DataDirectryName = "/Data/2023/0614/129Xe_010A_18.3kHz/run1/"
#DataDirectryName = "/Data/2023/0614/129Xe_010A_19kHz/run5/"
DataDirectryName = "/Data/2023/0724/test10/10/"

HomePath         = os.path.expanduser("~")
#DataPath         = HomePath + "/NMRProgram/AFPNMR_FS/" + DataDirectryName
#DataName         = HomePath + "/FIDNMR/" + DataDirectryName + "floatData.txt"
DataName         = HomePath + "/git/FIDNMR/" + DataDirectryName + "data.csv"
DataPath         = HomePath + "/git/FIDNMR/" + DataDirectryName
#GoogleDrivePath  = HomePath + "/マイドライブ/" + DataDirectryName

# File name
FileNamePeakValue    = DataPath + "FitValues.csv"
FileNameLog          = DataPath + "Log.txt"
FileNameParameter    = DataPath + "Parameter.csv"
FileNamePeakValuePDF = DataPath + "FitValues.pdf"

#TimeInterval         = 1800   # [sec]
TimeInterval         = 20   # [sec]
#TimeInterval         = 50      # [sec]

NumOfDataAcquisition = 30

# Option
OptOverWrite         = 0       # if Opt=1, start file number is forcibly to 1
OptOnlyLockin        = 0       # Option for only lockin    (Will be used for phase tuning)
OptOnlySpinFlip      = 0       # Option for only spin flip (Will be used at beamline experiment)
OptCopyToGoogleDrive = 0       # Option for backup to Google Drive
OptBuildRelax        = "R"     # Option for measurement type (Buildup = "B" or Relaxation = "R")

####################################################
# SpinFlip
#FGName  = "USB0::0x0D4A::0x000D::9377454::INSTR" #Goto_Cabin
#FGName="USB0::0x0D4A::0x000D::9217876::INSTR" #Noda-san's FG
FGName="USB0::0x0D4A::0x000D::9122074::INSTR" #Harada-san's FG
#FGName="USB0::0x0D4A::0x000D::9289693::INSTR" #Okudaira_sanFG
#FGName="USB0::0x0D4A::0x000D::9377454::INSTR" #Goto_Cabin
OscName = "USB0::0x0957::0x1798::MY61410321::INSTR"  # New Keysight Oscillo
#OscName="USB0::0x0957::0x1765::MY50070140::INSTR" #Agilent
#OscName="USB0::2391::5989::MY50070140::INSTR"


#-------------------
# Memory info of FG
MemorySet       = [[0, 0], [1, 1], [0.2, 2], [0.1, 3], [0.05, 4], [0.02, 5], [0.1, 6]]
Memory          = MemorySet[2]   # Memory info to be used
RFFrequency     = 19000      # Applied RF Frequency
NSpinFlip       = 1              # Not used
FGMemory        = Memory[1]      # Memory number
FGVoltage       = 18             # Output voltage [V] Ohtama, ShingoCoil
#FGVoltage       = 6              # Output voltage [V], SmallCoil, NOVACoil
#FGVoltage       = 1              # Output voltage [V]  Depol
#FGVoltage       = 11              # Output voltage [V]  FIDNMR
NPulse          = 20              #Number of applied pulse
Function        = "SIN"           #Applied Function


#-------------------
# Memory info of Osc
OscMode         = "N"            # Normal or Average
OscAverage      = 64             # Number of times of average
OscDataPoint    = 2e5            # Data points
OscTimeout      = 2000           # Timeout time [ms]
OscTriggerLevel = 1              # Trigger level [V]
OscChTrigger    = 3              # Osc channel for the sync out of the function generator
OscTimeDelay    = 0.031          # Osc time delay
OscTimeRange    = 0.050          # Osc time range. The range between OscTimeDelay and (OscTimeRange+OscTimeDelay) will be displayed.

#####################################################
# Lockin
FitRange  = [46e3, 54e3]
#FitRange = [110e3, 120e3]
#FitRange = [111e3, 119e3]
NMean     = 1000
#NMean=500
#Phase     = math.pi + (0.25*math.pi)
#Phase      = -math.pi*(1/22) + (math.pi-0.65)
Phase      = -math.pi*(24./22.) + (math.pi-0.65)
FreqRange = [40e3, 60e3]
#FreqRange = [94e3, 134e3]  # Range of frequensy sweep

GyromagneticRatioHe = 2.038e8 # value of GyromagneticRatio of He-3 = −203.789 (10^6 rad s^-1 T^-1)
FunctionBreitWigner = "[0]/sqrt(pow([1]/(2*2*{0})*{1}, 2) + pow([2]-x, 2))".format(math.pi, GyromagneticRatioHe)
FunctionBackground  = "[0]+[1]*x+[2]*x*x+[3]*x*x*x" 
# [0] : Intensity 
# [1] : Width
# [2] : Peak position
# [3]-[6]:pol3    ([0]-[3] in FunctionBackground)
# {0}, {1} : math.pi, GyromagneticRatioHe#
#InitialValueBritWignerBGX = [-3.8, 1.1e-5, (FitRange[0]+FitRange[1])*0.5,
InitialValueBritWignerBGX = [-10, 2e-5, (FitRange[0]+FitRange[1])*0.5,
                             -1e-1, 1e-5, 1e-10, 1e-14]
InitialValueBritWignerBGY = [-2, 2e-5, (FitRange[0]+FitRange[1])*0.5,
                             1e-3, 1e-5, 1e-5, 1e-5]
ParameterLimitBritWignerBG = [[-1e2, 1e2], [0, 100e-6], [FitRange[0], FitRange[1]],
                              [-1, 1], [-1e-2, 1e-2], [-1e-8, 1e-8], [-1e-10, 1e-10]]


#####################################################
# DrawGraph
FunctionBuild = "[0]*(1-exp(-x/[1]))*exp(-5.52/3600*x/76)"
InitialValueBuild   = [10e-3, 10]
ParameterLimitBuild = [[0, 100000], [0, 100]]

FunctionRelaxation = "[0]*exp(-x/[1])*exp(-5.52/3600*x/76)"
#Function = "[0]*(exp(-x/[1]))*exp(-(x+1)*2*2/23500.)"
#Function = "[0]*(exp(-x/[1]))*exp(-x*2/216)"                                                       
#Function = "[0]*(exp(-x/[1]))*exp(-x*6/4000)"
InitialValueRelax   = [50e-3, 150]
ParameterLimitRelax = [[0, 1], [0, 500]]
