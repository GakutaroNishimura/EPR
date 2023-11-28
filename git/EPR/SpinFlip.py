#======================================================================
#  Calculation of neutron spin rotation
#  ver.1.0:     2019            T.Okudaira  (AFPNMR_FS/NMR_FS.py)
#  ver.2.0:     2022            S.Takahashi (AFPNMRGUI/NMR_FS_forGUI.py)
#  ver.3.0:     2022            S.Takahashi (AFPNMRGUI_ver3/NMR_FS_forGUI.py)
#  ver.4.0:     2023/03/28      S.Takada    (AFPNMR/SpinFlip.py)
#======================================================================

# 何しているかわからないのであとでコメントを書く

import pyvisa as visa
from array import array
import time
import datetime
import csv
import math
import struct
import sys
import os
import pandas as pd
import Config as conf
import FileInfo

rm = visa.ResourceManager()
FG = rm.open_resource(conf.FGName)
Osc = rm.open_resource(conf.OscName)
Osc.timeout = conf.OscTimeout

def InitialSetFG():
    FG.write(":SOURce1:Frequency:Mode Sweep")
    FG.write(":SOURce1:SWEep:Mode Gated")
    FG.write(":Source1:Function:Shape %s" % conf.Function)
    FG.write(":SOURce1:BURSt:NCYCles %f" % conf.NPulse)
    FG.write(":SOURce1:FREQuency %f" % (conf.RFFrequency))
    FG.write(":TRIGger1:BUR:SOURce External")
    #FG.write("SOURce1:FUNCtion:USER %i" % conf.FGMemory)  # read memory
    FG.write(":Source1:Voltage %f" % conf.FGVoltage)
    
    
    
def InitialSetOsc():
    Osc.write(":RUN")
    Osc.write(":SYSTem:PRECision ON")
    Osc.write(":DISPlay:CLEar")    

    #Osc.write(":TIMebase:RANGe %f" % (conf.NPulse**conf.NSpinFlip))    # ウィンドウの水平方向のフルスケール
    #Osc.write(":TIMebase:DELay %f" % (conf.ModulationTime*conf.NSpinFlip/2.)) # たぶん原点から半分ずらしてるけど何故か正
    Osc.write(":TIMebase:RANGe %f" % (conf.OscTimeRange))    # ウィンドウの水平方向のフルスケール
    Osc.write(":TIMebase:DELay %f" % (conf.OscTimeDelay)) # たぶん原点から半分ずらしてるけど何故か正
    # Osc.write(":TRIGger:SWEep Normal")
    # Osc.write(":TRIGger:SWEep Auto")
    Osc.write(":TRIGger:Source Channel%d" % (conf.OscChTrigger))                 # Trigger(FGのSync out)を入れるチャンネル
    Osc.write(":TRIGger:LEVel %f" % (conf.OscTriggerLevel))                          # トリガーレベル
    if (conf.OscMode == "N"):                                                         # Normal mode
        Osc.write(":ACQuire:TYPE Normal")
    if (conf.OscMode == "A"):                                                         # Average mode
        Osc.write(":ACQuire:TYPE Average")
        Osc.write(":MTESt:AVERage:COUNt %d" % (conf.OscAverage))
    Osc.write(":ACQuire:COMPlete 100")
    Osc.write(":WAVeform:FORMat BYTE")
    # Osc.write(":WAVeform:FORMat ASCII")
    Osc.write(":WAVeform:POINts:MODE MAXimum")
    Osc.write(":WAVeform:POINts %d" % (conf.OscDataPoint))
    # print(Osc.query(":WAVeform:POINts:MODE?"))
    # print(Osc.query(":WAVeform:POINts?"))

    Osc.write(":STOP")
    Osc.write(":RUN")
    Osc.write(":TRIGger:SWEep Normal")
    Osc.write(":DIGitize")


def SpinFlip():
    FG.write("OUTPut:STATe ON")   
    # Send time of Trigger
    t = datetime.datetime.now()
    date_1 = str(t)[:-3]    
    FG.write("*TRG")    
    # End time of Trigger
    t = datetime.datetime.now()
    date_2 = str(t)[:-3]    
    Osc.write(":WAVeform:SOURce CHANnel2")
    Oscdata = Osc.query_binary_values(":WAVeform:DATA?", datatype='B')
    FG.write("OUTPut:STATe OFF")

    return Oscdata, date_1, date_2


def GetOscInformation():
    TOrigin = float(Osc.query("WAVeform:XORigin?"))
    TReference = float(Osc.query("WAVeform:XREFerence?"))
    TIncrement = float(Osc.query("WAVeform:XINCrement?"))
    #    print(TOrigin, TReference, TIncrement)
    
    VOrigin = float(Osc.query("WAVeform:YORigin?")) # 縦軸の原点
    VReference = float(Osc.query("WAVeform:YREFerence?")) # Offset?
    VIncrement = float(Osc.query("WAVeform:YINCrement?")) # 1bitが何Vか
    #    print(VOrigin, VReference, VIncrement)
    
    return TOrigin, TReference, TIncrement, VOrigin, VReference, VIncrement

"""
def InitialSetOsc2(NorA):
    # Osc.write(":TIMebase:RANGe 10")
    Osc.write(":TIMebase:RANGe 10e-3")
    # Osc.write(":TRIGger:SWEep Normal")
    # Osc.write(":TRIGger:SWEep Auto")
    # Osc.write(":TRIGger:Source Channel%d" %(OscChTrigger))
    # Osc.write(":TRIGger:LEVel %f" %(Threthold))
    if (NorA == "N"):
        Osc.write(":ACQuire:TYPE Normal")
    if (NorA == "A"):
        Osc.write(":ACQuire:TYPE Average")
        Osc.write(":MTESt:AVERage:COUNt %d" % (conf.OscAverage))
    Osc.write(":ACQuire:COMPlete 100")
    Osc.write(":WAVeform:FORMat BYTE")
    # Osc.write(":WAVeform:FORMat WORD")
    # Osc.write(":WAVeform:FORMat ASCII")
    # Osc.write(":WAVeform:POINts:MODE MAXimum")
    Osc.write(":WAVeform:POINts:MODE MAXimum")
    Osc.write(":WAVeform:POINts %d" % (conf.OscDataPoint))
    print(Osc.query(":WAVeform:POINts:MODE?"))
    print(Osc.query(":WAVeform:POINts?"))


def CloseDevices(FG, Osc):
    FG.close()
    Osc.close()


def GetSaveFileFormat(Osc):
    print(Osc.query("Save:Filename?"))
    print(Osc.query(":SAVE:WAVeform:FORMat?"))
    print(Osc.query(":SAVE:WAVeform:Length?"))
    print(Osc.query(":SAVE:WAVeform:SEGMented?"))


def SetOscFormat(channel, Osc):
    # Osc.write(":RUN")
    # Osc.write(":TRIGger:SWEep AUTO")
    Osc.write(":TIMebase:RANGe %f" % (ModulationTime*4))
    Osc.write(":TRIGger:SWEep Normal")
    Osc.write(":ACQuire:TYPE Normal")
    # Osc.write(":ACQuire:TYPE Average")
    Osc.write(":MTESt:AVERage:COUNt 64")
    Osc.write(":ACQuire:COMPlete 100")
    # Osc.write(":DIGitize CHANnel%d" %(channel))
    Osc.write(":WAVeform:SOURce CHANnel%d" % (channel))
    Osc.write(":WAVeform:FORMat BYTE")
    Osc.write(":WAVeform:FORMat ASCII")
    Osc.write(":WAVeform:POINts:MODE MAXimum")
    Osc.write(":WAVeform:POINts 1000")


def GetEPRFreq(Freq, DeltaFreq, Osc):
    Osc.write(":RUN")
    # Osc.write(":STOP")
    # Osc.write(":DIGitize CHANnel")
    Osc.write(":DIGitize CHANnel1")
    # Osc.write(":DIGitize CHANnel2")

    SetOscFormat(1)
    value = Osc.query(":WAVeform:DATA?")
    V = value.split(",")
    V[0] = V[0][10:]
    V = list(map(float, V))
    NPoint = len(V)

    Time = [(i-TReference)*TIncrement+TOrigin for i in range(NPoint)]

    return V, Time, NPoint
"""

def DataOutputToBinaryFile(Oscdata, BinaryFileName, OscInformation):
    ####
    # Variables in this program
    NPointLockin = 0
    VLockin = []
    TimeLockin = []
    VLockintemp = 0
    NPoint = 0
    VMax = 0
    MaxT = 0
    NMean = 1000
    with open(BinaryFileName, mode='wb') as f:
        for iInfo in range(len(OscInformation)):
            f.write(struct.pack("f", OscInformation[iInfo]))
        """
        f.write(struct.pack("f", TOrigin))
        f.write(struct.pack("f", TReference))
        f.write(struct.pack("f", TIncrement))
        f.write(struct.pack("f", VOrigin))
        f.write(struct.pack("f", VReference))
        f.write(struct.pack("f", VIncrement))
        """
        for iData in Oscdata:
            f.write(struct.pack("B", iData))
            # f.write(struct.pack("B",value2[j]))
            """
            VLockintemp=VLockintemp+((value[j]-VReference)*VIncrement+VOrigin)*((value[j]-VReference)*VIncrement+VOrigin)
            if(j%NMean==0 and j!=0):
                VLockin.append((VLockintemp/NMean))
                TimeLockin.append((j-TReference)*TIncrement+TOrigin)
                if(VLockintemp/NMean>VMax):
                    VMax=VLockintemp/NMean
                    MaxT=(j-TReference)*TIncrement+TOrigin
                NPointLockin=NPointLockin+1
            VLockintemp=0
            """
    
def DataOutputToParameterFile():
    NowTime = datetime.datetime.now()
    DataDictionary = dict(Time=[NowTime],
                          TimeInterval=[conf.TimeInterval],
                          Voltage=[conf.FGVoltage],
                          FunctionGenerator=[conf.FGName],
                          Oscilloscope=[conf.OscName],
                          FreqRange=[conf.FreqRange])
    df = pd.DataFrame(data=DataDictionary)
    
    # output
    header = FileInfo.addHeader(conf.FileNameParameter)
    df.to_csv(conf.FileNameParameter, mode="a", index=False, header=header)
    
            
def main(BinaryFileName):    
    # Check FG Setting
    #print("Pulse Time : ", conf.ModulationTime, " Memory Number : ", conf.FGMemory)

    ###############################
    # Initialization
    print("Initialization of Oscilloscope")
    InitialSetOsc()
    print("Initialization of Function Generator ")
    InitialSetFG()

    ###############################
    # Spin flip
    print("Flip!")
    Oscdata, date_1, date_2 = SpinFlip()
    
    ####
    # Get Osc Information (Origin, Reference, Increment) -> XYScale in Lockin.py    
    OscInformation = GetOscInformation()
    print("TOrigin: {0}, TReference: {1}, TIncrement: {2}".format(OscInformation[0], OscInformation[1], OscInformation[2]))
    print("VOrigin: {0}, VReference: {1}, VIncrement: {2}".format(OscInformation[3], OscInformation[4], OscInformation[5]))
    
    # Start time to write file
    t = datetime.datetime.now()
    date_3 = str(t)[:-3]
    f_log = open(conf.FileNameLog, 'a')
    
    # Write log
    date_line = "TRG IN: "+date_1+' TRG END :' + \
        date_2+' FILE WRITE START '+date_3+'\n'
    f_log.write(date_line)
    f_log.close()
    
    # time of Output
    d_today = datetime.datetime.now()
    str(d_today.strftime('%H%M'))
    
    # Data Output
    DataOutputToBinaryFile(Oscdata, BinaryFileName, OscInformation)
    DataOutputToParameterFile()
    
if __name__ == "__main__":
    os.makedirs(conf.DataPath, exist_ok=True)
    FileNo = FileInfo.GetMaxFileNumber() + 1
    BinaryFileName = conf.DataPath + str(FileNo).zfill(4) + ".bin"
    main(BinaryFileName)
