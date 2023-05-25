import pyvisa as visa #import visa causes an error "module 'visa' has no attribute 'ResourceManager'"
import ROOT
from array import array
import time
import datetime
import csv
import math
import sys
import numpy as np
import statistics as stat

argvs = sys.argv  
argc = len(argvs) 

rm = visa.ResourceManager()

#Parameters
FG2=rm.open_resource("USB0::0x0D4A::0x000D::9217876::INSTR")#Noda-san's FG
FG=rm.open_resource("USB0::0x0D4A::0x000D::9122074::INSTR")#Harada-san's FG
#Osc = rm.open_resource("USB0::2391::5989::MY50070140::INSTR")
Osc = rm.open_resource("USB0::0x0957::0x1798::MY61410321::INSTR")#New Keysight Oscillo  
#Meter = rm.open_resource("GPIB0::16::INSTR")
#Osc = rm.open_resource("USB0::0x0957::0x1765::MY50070140::INSTR")

Osc.timeout = 1000000          #time out time (ms)
Threthold=0.05              #Volt
ChSignal=1                  #channel of the signal input
#ChRF=2                      #channel of the RF input from the function generator
ChSync=3                    #channel of the sync out from the function generator
ChTrigger=ChSync
ChMonitor=2


#ModulationFunc="TRIangle"
ModulationFunc="PRAMP"
#ModulationFunc="SIN"
Function="SIN"
#ModulationFreq=60       #Hz Modulation frequency
ModulationFreq=1001       #Hz Modulation frequency
#iFreq= 7334000             #Hz Initial central value of the frequency
#iFreq= 7270000
#iFreq= 7348600       #10/18
#iFreq= 7385000
#iFreq= 7225000
#iFreq= 7405000 #120度
#iFreq= 7242000
iFreq= 7300000
#iFreq= 7418000 #110度
#iFreq= 7427000 #100度
#iFreq= 7453000 #
#iFreq= 7358000 
#iFreq= 7334600             #Hz Initial central value of the frequency
iDeltaFreq=1e6*0.7 #iFreq*0.03  #Hz Initial amplitude of the deviation 
#iDeltaFreq=1e6*0.5
Voltage=20           #Volt
N_wave=3

Query_delay = 0
SleepTime=1
NAverage=1500
Nmeasure = 10000

# noise_fit.pyで得た、sweep磁場がないときのsignalのノイズ.
# averageの回数で大きさが変わる.
#Noise = 0.0001097      # noise for df56-df61 [V]
Noise = 0.0003883       # noise for df36-df55 [V]

F_mod = ModulationFreq    # modulation freq [Hz]
F_dev = iDeltaFreq     # deviation freq. [kHz]
F_0 = iFreq/10**3      # 変調磁場の中心周波数 [kHz]
Npeak = 10      # 一回で取得するピークの数
Fit_Range = 0.0001      # ピークをフィットするときの横軸の幅
canvasWidth = 600
canvasHeight = 300

SF_Func="SIN"
SF_ModulationFreq=2       #Hz Modulation frequency
StartFreq=10e3
StopFreq=200e3
SF_Voltage=18.           #Volt


Osc.write(":RUN")
Osc.write(":TRIGger:SWEep AUTO")
Osc.write(":RUN")
Osc.write(":ACQuire:TYPE Normal")
TOrigin=float(Osc.query("WAVeform:XORigin?"))
TReference=float(Osc.query("WAVeform:XREFerence?"))
TIncrement=float(Osc.query("WAVeform:XINCrement?"))

#Meter.write(":Current:DC:NPLCycles 10") #integration time of multimeter

def InitialSetFM():
    FG.write(":Source1:FM:State ON")
    FG.write(":Source1:FM:Source Internal")
    FG.write(":Source1:Function:Shape %s" %Function)
    FG.write(":Source1:FM:Internal:Function:Shape %s" %ModulationFunc)
    FG.write(":Source1:Voltage %f" %Voltage)
    FG.write(":Source1:FM:Internal:Frequency %fHZ" %(ModulationFreq))
    FG.write(":Source1:Frequency %fHZ" %(iFreq))
    FG.write(":Source1:FM:Deviation %fHZ" %(iDeltaFreq))


def InitialSetFlipFM():
    FG2.write(":SOURce1:Frequency:Mode Sweep")
    FG2.write(":SOURce1:SWEep:MODE Gated")
    FG2.write(":TRIGger1:SWEep:SOURce External")
    FG2.write(":Source1:Function:Shape %s" %SF_Func)
    FG2.write("SOURce1:SWEep:TIME %f" %(1/SF_ModulationFreq))
    FG2.write(":SOURce1:FREQuency:STARt %f" %(StartFreq))
    FG2.write(":SOURce1:FREQuency:Stop %f" %(StopFreq))
    FG2.write(":Source1:Voltage %f" %SF_Voltage)
    FG2.write(":OUTPut:STATe ON")


def InitialSetOsc(NorA):
    Osc.write(":TIMebase:RANGe %f" %(1./ModulationFreq*N_wave))
    Osc.write(":TRIGger:SWEep Normal")
    Osc.write(":TRIGger:LEVel 0.0")
    Osc.write(":TRIGger:Source Channel%d" %(ChTrigger))
    """
    if(NorA=="N"): Osc.write(":ACQuire:TYPE Normal")
    if(NorA=="A"):
        Osc.write(":ACQuire:TYPE Average")
        Osc.write(":MTESt:AVERage:COUNt %d" %(Avecount))
    """
    Osc.write(":ACQuire:COMPlete 100")
    Osc.write(":WAVeform:FORMat BYTE") #set the data transmission mode for waveform data points
    Osc.write(":WAVeform:FORMat ASCII")
    Osc.write(":WAVeform:POINts:MODE MAXimum")
    Osc.write(":WAVeform:POINts 1000")

    
def AverageSetOsc(NorA, Avecount):
    if(NorA=="N"): Osc.write(":ACQuire:TYPE Normal")
    if(NorA=="A"):
        Osc.write(":ACQuire:TYPE Average")
        Osc.write(":MTESt:AVERage:COUNt %d" %(Avecount))
        #print("writeしたよ")


def SetFM(Freq,Deltafreq):
    FG.write(":Source1:Frequency %fHZ" %(Freq))
    FG.write(":Source1:FM:Deviation %fHZ" %(Deltafreq))


def CloseDevices():
    FG.close()
    Osc.close()


def GetEPRFreqFit():
    peak = []
    peak_e = []
    peak_ideal = []
    EPR_freq_list = []

    AverageSetOsc("A", NAverage)
    Osc.write(":WAVeform:SOURce CHANnel%d"%(ChSignal))  
    value = Osc.query(":WAVeform:DATA?")
    V=value.split(",")
    V[0]=V[0][10:]
    V=list(map(float, V))
    NPoint=len(V)

    """
    #オシロの中でsignalをmonitorで割り算し、その値を得る.
    AverageSetOsc("A", NAverage)
    Osc.write(":WAVeform:SOURce MATH")  
    value = Osc.query(":WAVeform:DATA?")
    V=value.split(",")
    V[0]=V[0][10:]
    V=list(map(float, V))
    NPoint=len(V)
    """

    AverageSetOsc("N", 0)
    Osc.write(":WAVeform:SOURce CHANnel%d"%(ChSync))
    value2=Osc.query(":WAVeform:DATA?")
    VSync=value2.split(",")
    VSync[0]=VSync[0][10:]
    VSync=list(map(float, VSync))

    # 得た電圧の情報をテキストファイルに書き込む.
    if argc == 3:
        f=open(argvs[2],"a")
        for i in range(NPoint):
            f.write("%f %f\n" %(V[i], VSync[i]))
        f.close()

    VCurrent=1#Meter.query(":Measure:Current?")  
    VCurrent=float(VCurrent)
    
    Time=[(i-TReference)*TIncrement+TOrigin for i in range(NPoint)]

    for i in range(Npeak):
        Fit_center = 0.000533512052921227-Npeak/2/F_mod+i/F_mod
        # create a TGraph with the data
        gr = ROOT.TGraphErrors(NPoint, np.array(Time), np.array(V), np.array([0.0 for i in range(NPoint)]), np.array([Noise for i in range(NPoint)]))
        # set the fit function and the fit range
        f = ROOT.TF1("f", "[0]-gaus(x, [1], [2], [3])", Fit_center-Fit_Range, Fit_center+Fit_Range)
        # set initial parameter values for the fit
        f.SetParameters(0, 0.003, Fit_center, 6*10**(-5))
        # perform the fit
        gr.Fit(f, "QR")
        # get the fitted parameters
        par = [f.GetParameter(k) for k in range(f.GetNpar())]
        par_e = [f.GetParError(k) for k in range(f.GetNpar())]
        peak.append(par[2])
        peak_e.append(par_e[2])

    for i in range(0, Npeak+1):
        p = peak[int(Npeak/2)] -Npeak/2/F_mod + i/F_mod
        peak_ideal.append(p)

    peak_dev = [peak[i]-peak_ideal[i] for i in range(len(peak))]

    f_dev = [F_mod*F_dev*i for i in peak_dev]

    f_e = [F_mod*F_dev*i for i in peak_e]

    iEPR_freq = F_dev*F_mod*peak[int(Npeak/2)]+F_0-F_dev/2

    for i in f_dev:
        EPR_freq = iEPR_freq+i
        EPR_freq_list.append(EPR_freq)
    
    ERP_freq_mean = stat.mean(EPR_freq_list)
    EPR_freq_error = np.sqrt(sum([i**2 for i in f_e]))

    f=open(argvs[1],"a")
    f.write("%f %f\n" %(ERP_freq_mean, EPR_freq_error))
    f.close()


if __name__ == "__main__":
    print(rm.list_resources())
    MODE="Lockin" #"PeakDetect"
    
    InitialSetFM()
    InitialSetFlipFM()
    #InitialSetOsc("N",64)
    InitialSetOsc("A")
    Vpp=0
    #for i in range(20): Vpp=Vpp+float(Osc.query(":Measure:VPP? Channel1"))
    #Vpp=Vpp/20
    Vpp=1
    
    FreqEPR=iFreq
    VCurrenti=0
    CurrentCorrection=1
    VCurrentMean=0
    VCurrentCount=15
    VCurrentList=[0 for i in range(VCurrentCount)]
    itime = time.time()
    FG.write("OUTPut:STATe ON")

    for i in range(Nmeasure):
        if i == int(Nmeasure/2)-1:
            FG2.write("*TRG")
            time.sleep(1./SF_ModulationFreq)

        GetEPRFreqFit()

