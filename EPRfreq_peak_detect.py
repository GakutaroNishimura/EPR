import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def fun(x, p0, a, m, s):
    return p0 - a*np.exp(-0.5*(x-m)**2/s**2)

#def peak_fit()
path_36to55 = "./peak/36-55/"
path_56to61 = "./peak/56-61/"

"""
df36 = pd.read_csv("./WaveData/scope_36.csv", names = ["time", "signal", "sync"], skiprows = 2)
df37 = pd.read_csv("./WaveData/scope_37.csv", names = ["time", "signal", "sync"], skiprows = 2)
df38 = pd.read_csv("./WaveData/scope_38.csv", names = ["time", "signal", "sync"], skiprows = 2)
df39 = pd.read_csv("./WaveData/scope_39.csv", names = ["time", "signal", "sync"], skiprows = 2)
df40 = pd.read_csv("./WaveData/scope_40.csv", names = ["time", "signal", "sync"], skiprows = 2)
df41 = pd.read_csv("./WaveData/scope_41.csv", names = ["time", "signal", "sync"], skiprows = 2)
df42 = pd.read_csv("./WaveData/scope_42.csv", names = ["time", "signal", "sync"], skiprows = 2)
df43 = pd.read_csv("./WaveData/scope_43.csv", names = ["time", "signal", "sync"], skiprows = 2)
df44 = pd.read_csv("./WaveData/scope_44.csv", names = ["time", "signal", "sync"], skiprows = 2)
df45 = pd.read_csv("./WaveData/scope_45.csv", names = ["time", "signal", "sync"], skiprows = 2)
df46 = pd.read_csv("./WaveData/scope_46.csv", names = ["time", "signal", "sync"], skiprows = 2)
df47 = pd.read_csv("./WaveData/scope_47.csv", names = ["time", "signal", "sync"], skiprows = 2)
df48 = pd.read_csv("./WaveData/scope_48.csv", names = ["time", "signal", "sync"], skiprows = 2)
df49 = pd.read_csv("./WaveData/scope_49.csv", names = ["time", "signal", "sync"], skiprows = 2)
df50 = pd.read_csv("./WaveData/scope_50.csv", names = ["time", "signal", "sync"], skiprows = 2)
df51 = pd.read_csv("./WaveData/scope_51.csv", names = ["time", "signal", "sync"], skiprows = 2)
df52 = pd.read_csv("./WaveData/scope_52.csv", names = ["time", "signal", "sync"], skiprows = 2)
df53 = pd.read_csv("./WaveData/scope_53.csv", names = ["time", "signal", "sync"], skiprows = 2)
df54 = pd.read_csv("./WaveData/scope_54.csv", names = ["time", "signal", "sync"], skiprows = 2)
df55 = pd.read_csv("./WaveData/scope_55.csv", names = ["time", "signal", "sync"], skiprows = 2)
"""

df56 = pd.read_csv("./WaveData/scope_56.csv", names = ["time", "signal", "sync"], skiprows = 2)
df57 = pd.read_csv("./WaveData/scope_57.csv", names = ["time", "signal", "sync"], skiprows = 2)
df58 = pd.read_csv("./WaveData/scope_58.csv", names = ["time", "signal", "sync"], skiprows = 2)
df59 = pd.read_csv("./WaveData/scope_59.csv", names = ["time", "signal", "sync"], skiprows = 2)
df60 = pd.read_csv("./WaveData/scope_60.csv", names = ["time", "signal", "sync"], skiprows = 2)
df61 = pd.read_csv("./WaveData/scope_61.csv", names = ["time", "signal", "sync"], skiprows = 2)

"""
df_bf = [df36, df37, df38, df39, df40, df41, df42, df43, df44, df45]
df_af = [df46, df47, df48, df49, df50, df51, df52, df53, df54, df55]
"""

df_bf = [df56, df57, df58]
df_af = [df59, df60, df61]

peak_bf = []
peak_af = []
peak_ideal_bf = []
peak_ideal_af = []
EPR_freq_list = []
EPR_freq_list_bf = []
EPR_freq_list_af = []

F_mod = 1000 #[Hz]
F_dev = 700 #[kHz]
F_0 = 7225 #[kHz]
Npeak = 2
Fit_Range = 0.0001

# fit the peak(dipp) using the gaussian function
## fit range should be changed
for j in range(len(df_bf)):
#for j in range(1):
    for i in range(Npeak):
        par, cov = curve_fit(fun, df_bf[j].time, df_bf[j].signal, p0 = (0, 0.003, 0.0005471147644754069-Npeak/2/F_mod+i/F_mod, 6*10**(-5)))
        x = np.linspace(0.0005471147644754069-Npeak/2/F_mod+i/F_mod-Fit_Range, 0.0005471147644754069-Npeak/2/F_mod+i/F_mod+Fit_Range, 1000)
        y = fun(x, par[0], par[1], par[2], par[3])
        if i == 0:
            plt.plot(df_bf[j].time, df_bf[j].signal, ".", markersize = 1)
            plt.locator_params(axis="x", nbins=5)
            #plt.locator_params(axis="y", nbins=5)
            plt.grid()
            y_min = min(y)
            min_index = np.argmin(y)
            x_min = x[min_index]
            print(x_min)
        plt.plot(x, y)
        peak_bf.append(par[2])
        if i == Npeak-1:
            plt.savefig(path_56to61 + "bf" + str(j) + ".pdf")
            plt.savefig(path_56to61 + "bf" + str(j) + ".png")
    
    plt.close()
    
for j in range(len(df_af)):
#for j in range(1):
    for i in range(Npeak):
        par, cov = curve_fit(fun, df_af[j].time, df_af[j].signal, p0 = (0, 0.004, 0.0005427619600890558-Npeak/2/F_mod+i/F_mod, 6*10**(-5)))
        x = np.linspace(0.0005427619600890558-Npeak/2/F_mod+i/F_mod-Fit_Range, 0.0005427619600890558-Npeak/2/F_mod+i/F_mod+Fit_Range, 1000)
        y = fun(x, par[0], par[1], par[2], par[3])
        if i == 0:
            plt.plot(df_af[j].time, df_af[j].signal, ".", markersize = 1)
            plt.locator_params(axis="x", nbins=5)
            #plt.locator_params(axis="y", nbins=5)
            plt.grid()
        plt.plot(x, y)
        peak_af.append(par[2])
        if i == Npeak-1:
            plt.savefig(path_56to61 + "af" + str(j) + ".pdf")
            plt.savefig(path_56to61 + "af" + str(j) + ".png")
    #print(par)
    plt.close()
    
    
#calculate the ideal time(frequency) of the peaks assuming all the peaks are equidistant
k = 0
for j in range(len(df_bf)):
    p_zenhan = peak_bf[k : k+int(Npeak/2)+1]
    p_kouhan = peak_bf[k+int(Npeak/2)+1 : k+Npeak]
    for i in range(0, int(Npeak/2)+1):
        p = peak_bf[int(Npeak/2)+2*j*int(Npeak/2)] -Npeak/2/F_mod + i/F_mod
        peak_ideal_bf.append(p)
        k += 1

    for i in range(1, int(Npeak/2)):
        p = peak_bf[int(Npeak/2)+2*j*int(Npeak/2)] + i/F_mod
        peak_ideal_bf.append(p)
        k += 1

        
for j in range(len(df_af)):
    p_zenhan = peak_af[k : k+int(Npeak/2)+1]
    p_kouhan = peak_af[k+int(Npeak/2)+1 : k+Npeak]
    for i in range(0, int(Npeak/2+1)):
        p = peak_af[int(Npeak/2)+2*j*int(Npeak/2)] -Npeak/2/F_mod + i/F_mod
        peak_ideal_af.append(p)
        k += 1

    for i in range(1, int(Npeak/2)):
        p = peak_af[int(Npeak/2)+2*j*int(Npeak/2)] + i/F_mod
        peak_ideal_af.append(p)
        k += 1
        
        
#calculate the misallignment between ideal time and measured time of peaks
peak_dev_bf = [peak_bf[i]-peak_ideal_bf[i] for i in range(len(peak_bf))]
peak_dev_af = [peak_af[i]-peak_ideal_af[i] for i in range(len(peak_af))]


#convert a time of a peak to the frequency of the peak
f_dev_bf = [F_mod*F_dev*i for i in peak_dev_bf]
f_dev_af = [F_mod*F_dev*i for i in peak_dev_af]
f_dev = f_dev_bf + f_dev_af


#calculate the EPR freq. of all peaks
for i in range(len(df_bf)):
    iEPR_freq = F_dev*F_mod*peak_bf[int(Npeak/2)+2*i*int(Npeak/2)]+F_0-F_dev/2
    for j in f_dev_bf[Npeak*i:Npeak*i+Npeak]:
        EPR_freq_bf = iEPR_freq+j
        EPR_freq_list_bf.append(EPR_freq_bf)
    
for i in range(len(df_af)):
    iEPR_freq = F_dev*F_mod*peak_af[int(Npeak/2)+2*i*int(Npeak/2)]+F_0-F_dev/2
    for j in f_dev_af[Npeak*i:Npeak*i+Npeak]:
        EPR_freq_af = iEPR_freq+j
        EPR_freq_list_af.append(EPR_freq_af)
    
EPR_freq_list = EPR_freq_list_bf + EPR_freq_list_af


plt.plot(np.linspace(1, (len(df_bf)+len(df_af))*Npeak, (len(df_bf)+len(df_af))*Npeak), EPR_freq_list, ".")
plt.show()