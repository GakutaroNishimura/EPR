import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ROOT
import time
import glob
import statistics as stat
import os
import sys

argvs = sys.argv  
argc = len(argvs) 

peak = []
f_shift_list = []
Noise = 7.037*10**(-6)       # noise for df100-df168 [V]
#Noise = 4.369*10**(-5)       # noise for df169-df317 [V]

f_file = 120
l_file = 129

file_path = [] #データのpathをしまうlist.""で囲まれた文字列のリストになる.
for i in range(f_file, l_file+1):
    path = glob.glob("./WaveData/scope_%d.csv"% i)
    file_path.append(path[0])


dir_path = "./peak/%d-%d/pol2/"%(f_file, l_file)

os.makedirs(dir_path, exist_ok=True)

#range and FG setting for the data 100 to 129
bf_xmin = 0.115*10**(-3)
bf_xmax = 0.13*10**(-3)
af_xmin = 0.118*10**(-3)
af_xmax = 0.133*10**(-3)
F_mod = 4001
F_dev = 500*10**3



"""
#range for the data 130 to 168
bf_xmin = -0.135*10**(-3)
bf_xmax = -0.121*10**(-3)
af_xmin = -0.135*10**(-3)
af_xmax = -0.117*10**(-3)
F_mod = 4001
F_dev = 500*10**3
"""

#range for the data 178 to 183
#bf_xmin = 0.11*10**(-3)
#bf_xmax = 0.14*10**(-3)
#af_xmin = 0.1*10**(-3)
#af_xmax = 0.13*10**(-3)

#range for the data 184 to 189
#bf_xmin = 0.12*10**(-3)
#bf_xmax = 0.141*10**(-3)
#af_xmin = 0.115*10**(-3)
#af_xmax = 0.137*10**(-3)
#F_mod = 4001
#F_dev = 300*10**3

#range for the data 190 to 202
#bf_xmin = 0.135*10**(-3)
#bf_xmax = 0.152*10**(-3)
#af_xmin = 0.128*10**(-3)
#af_xmax = 0.145*10**(-3)
#F_mod = 4001
#F_dev = 300*10**3

#range for the data 203 to 208
#bf_xmin = 0.132*10**(-3)
#bf_xmax = 0.149*10**(-3)
#af_xmin = 0.127*10**(-3)
#af_xmax = 0.145*10**(-3)
#F_mod = 4001
#F_dev = 300*10**3

#range for the data 209 to 214
#bf_xmin = 0.1*10**(-3)
#bf_xmax = 0.13*10**(-3)
#af_xmin = 0.095*10**(-3)
#af_xmax = 0.125*10**(-3)

#range for the data 215 to 218
#bf_xmin = 0.11*10**(-3)
#bf_xmax = 0.135*10**(-3)
#af_xmin = 0.105*10**(-3)
#af_xmax = 0.13*10**(-3)


Nshift = int(len(file_path)/2)

for i in range(Nshift):
    df_bf = pd.read_csv(file_path[2*i], names = ["time", "signal", "sync"], skiprows=3)
    df_af = pd.read_csv(file_path[2*i+1], names = ["time", "signal", "sync"], skiprows=3)

    c = ROOT.TCanvas("c", "title", 800, 1200)
    c.Divide(1,2)

    c.cd(1)
    gr_bf = ROOT.TGraphErrors(len(df_bf.time), np.array(df_bf.time), np.array(df_bf.signal), np.array([0.0 for i in range(len(df_bf.time))]), np.array([Noise for i in range(len(df_bf.time))]))

    bf_fit = ROOT.TF1("f", "pol2", bf_xmin, bf_xmax)
    gr_bf.Fit(bf_fit, "QR")
    #min = bf_fit.GetMinimumX(bf_xmin, bf_xmax)
    #print(min)
    par = [bf_fit.GetParameter(k) for k in range(bf_fit.GetNpar())]
    x0 = -par[1]/(2*par[2])
    peak.append(x0)
    #peak.append(min)
    #print(peak)
    gr_bf.Draw("AP")
    ROOT.gStyle.SetOptFit(1)
    c.SetGridx()
    c.SetGridy()
    c.Draw("P")
    gr_bf.Draw("P")
    c.Update()

    c.cd(2)

    gr_af = ROOT.TGraphErrors(len(df_af.time), np.array(df_af.time), np.array(df_af.signal), np.array([0.0 for i in range(len(df_bf.time))]), np.array([Noise for i in range(len(df_bf.time))]))
    af_fit = ROOT.TF1("f", "pol2", af_xmin, af_xmax)
    gr_af.Fit(af_fit, "QR")
    #min = af_fit.GetMinimumX(af_xmin, af_xmax)
    #print(min)
    par = [af_fit.GetParameter(k) for k in range(af_fit.GetNpar())]
    x0 = -par[1]/(2*par[2])
    peak.append(x0)
    #peak.append(min)
    #print(peak)
    gr_af.Draw("AP")
    ROOT.gStyle.SetOptFit(1)
    c.SetGridx()
    c.SetGridy()
    c.Draw("P")
    gr_af.Draw("P")
    c.Update()
    
    time.sleep(1000)

    c.SaveAs(dir_path + str(2*i) + "-" + str(2*i+1) + ".png")

    t_shift = peak[2*i+1]-peak[2*i]
    if t_shift < 0:
        t_shift = -t_shift
    f_shift = t_shift*F_mod*F_dev
    f_shift_list.append(f_shift)
    
    if argc == 2:
        f=open(dir_path + argvs[1],"a")
        f.write("%f\n" %(f_shift))
        f.close()
    #print("delta_t = " + str(delta_t))
    #print("delta_f = " + str(delta_f))

if argc == 2:
    f=open(dir_path + argvs[1],"a")
    f.write("%f %f\n" %(stat.mean(f_shift_list), stat.stdev(f_shift_list)))
    f.close()
#print(f_shift_list)

c = ROOT.TCanvas("c", "title", 800, 600)
gr = ROOT.TGraph(Nshift, np.linspace(1, Nshift, Nshift), np.array(f_shift_list))
gr.SetMarkerStyle(3)
gr.SetMarkerSize(1)
gr.GetXaxis().CenterTitle(True)
gr.GetXaxis().SetTitle("number of measurment")
gr.GetYaxis().CenterTitle(True)
gr.GetYaxis().SetTitle("EPR freq. shift [Hz]")
gr.GetYaxis().SetRangeUser(0, 7000)
#ROOT.gStyle.SetOptFit(1)
gr.Draw("AP")
#c1 = ROOT.gROOT.FindObject("c1")
c.Draw("same")
c.SaveAs(dir_path + "EPR_Freq_Shift.png")
time.sleep(1000)
print(stat.mean(f_shift_list))
print(stat.stdev(f_shift_list))
