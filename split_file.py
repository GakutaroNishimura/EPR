import pandas as pd
import sys

signal_path = "./EPRsignal/"
file_path = "signal20230428_6_1.txt"
file_path2 = "signal20230428_6_2.txt"
file_path3 = "signal20230428_6_3.txt"

df = pd.read_table("./EPRsignal/signal20230428_6.txt", names=["time", "signal", "sync"], sep=" ")

for i in range(0, 2000000):
    time = df.time[i]
    signal = df.signal[i]
    sync = df.sync[i]
    f=open(signal_path + file_path ,"a")
    #f.write("%d-%d-%d-%d-%d %f %f %f\n" %(date.month,date.day,date.hour,date.minute,date.second, FreqEPRCorrected, FreqEPR, VCurrentMean))
    #f.write("%f %f %f %f\n" %(time.time()-itime, FreqEPRCorrected, FreqEPR, VCurrentMean))
    f.write("%f %f %f\n" %(time, signal, sync))
    #f.write("%d-%d-%d-%d-%d %f %f\n" %(date.month,date.day,date.hour,date.minute,date.second, VCurrent, VInteg))
    #f.write("%d-%d-%d-%d-%d %f\n" %(date.month,date.day,date.hour,date.minute,date.second, Lockin/Vpp))
    f.close()
    if i%100000 == 0:
        print(i)

for i in range(2000000, 4000000):
    time = df.time[i]
    signal = df.signal[i]
    sync = df.sync[i]
    f=open(signal_path + file_path2 ,"a")
    #f.write("%d-%d-%d-%d-%d %f %f %f\n" %(date.month,date.day,date.hour,date.minute,date.second, FreqEPRCorrected, FreqEPR, VCurrentMean))
    #f.write("%f %f %f %f\n" %(time.time()-itime, FreqEPRCorrected, FreqEPR, VCurrentMean))
    f.write("%f %f %f\n" %(time, signal, sync))
    #f.write("%d-%d-%d-%d-%d %f %f\n" %(date.month,date.day,date.hour,date.minute,date.second, VCurrent, VInteg))
    #f.write("%d-%d-%d-%d-%d %f\n" %(date.month,date.day,date.hour,date.minute,date.second, Lockin/Vpp))
    f.close()
    if i%100000 == 0:
        print(i)

for i in range(4000000, 6771499):
    time = df.time[i]
    signal = df.signal[i]
    sync = df.sync[i]
    f=open(signal_path + file_path3 ,"a")
    #f.write("%d-%d-%d-%d-%d %f %f %f\n" %(date.month,date.day,date.hour,date.minute,date.second, FreqEPRCorrected, FreqEPR, VCurrentMean))
    #f.write("%f %f %f %f\n" %(time.time()-itime, FreqEPRCorrected, FreqEPR, VCurrentMean))
    f.write("%f %f %f\n" %(time, signal, sync))
    #f.write("%d-%d-%d-%d-%d %f %f\n" %(date.month,date.day,date.hour,date.minute,date.second, VCurrent, VInteg))
    #f.write("%d-%d-%d-%d-%d %f\n" %(date.month,date.day,date.hour,date.minute,date.second, Lockin/Vpp))
    f.close()
    if i%100000 == 0:
        print(i)