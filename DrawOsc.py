import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_table("./EPRsignal/signal20230428_1.txt", names=["time", "signal", "sync"], sep=" ")
df_freq = pd.read_table("./FreqValue/FreqValue20230428_1.txt", names=["f_0", "f_1", "num"], sep=" ")

dfF = df_freq.f_0

set = 2

Start = 960*set
DataN = 960*(set+1)-1
signal_noise = 0.000246
delta = 0.0000004

#plt.plot(df.time[Start:DataN], df.signal[Start:DataN])
#plt.plot(df.time[Start:DataN], df.sync[Start:DataN]*3*10**(-3))
#plt.show()

Lockindf = (df.signal[Start:DataN] + delta)*(df.sync[Start:DataN] + delta)
LockindfError = signal_noise*df.sync[Start:DataN]
LockindfError = LockindfError**2

#print(df.signal[960*2-1])

#+0.002023+0.002023
Lockin = Lockindf.sum()
Lockin = Lockin/(0.001871 + delta)
factor=abs(Lockin)
LockinError = np.sqrt(LockindfError.sum())/(0.001871)

Henka=Lockin*15
#Henka=Lockin*factor
HenkaError = LockinError*15
#HenkaError = np.sqrt(2)*factor*LockinError
DeltaF = dfF[set+1]-dfF[set]

"""
if(Henka<0):
    Henka=Henka/4


if(abs(Henka)>1e4):
    Henka=Henka/100
    HenkaError=HenkaError/100

if(abs(Henka)>1e3):
    Henka=Henka/10
    HenkaError=HenkaError/10
"""

#Henka = Henka/DeltaF

# Henka = Lockin
# HenkaError = LockinError*15

# print(Henka)
# print(HenkaError)

print("Lockin = %f" %Lockin)
print("LockinError = %f" %LockinError)

print("Henka = %f" %Henka)
print("HenkaError = %f" %HenkaError)

print("DeltaF = %f" %DeltaF)
print(Henka/DeltaF)