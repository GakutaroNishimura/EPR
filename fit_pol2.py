import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ROOT
import time
import glob
import statistics as stat

peak = []
delta_f_list = []
Noise = 7.037*10**(-6)       # noise for df100-df168 [V]

#f_file = 100
#l_file = 119
f_file = 120
l_file = 129
file_path = [] #データのpathをしまうlist.""で囲まれた文字列のリストになる.
for i in range(f_file, l_file+1):
    path = glob.glob("./WaveData/scope_%d.csv"% i)
    file_path.append(path[0])

#dir_path = "./peak/100-119/"
dir_path = "./peak/120-129/pol2/"

Nshift = int(len(file_path)/2)

for i in range(Nshift):
    df_bf = pd.read_csv(file_path[2*i], names = ["time", "signal", "sync"], skiprows=2)
    df_af = pd.read_csv(file_path[2*i+1], names = ["time", "signal", "sync"], skiprows=2)

    c = ROOT.TCanvas("c", "title", 800, 1200)
    c.Divide(1,2)

    c.cd(1)
    gr_bf = ROOT.TGraphErrors(len(df_bf.time), np.array(df_bf.time), np.array(df_bf.signal), np.array([0.0 for i in range(len(df_bf.time))]), np.array([Noise for i in range(len(df_bf.time))]))

    bf_fit = ROOT.TF1("f", "pol2", 0.115*10**(-3), 0.13*10**(-3))
    gr_bf.Fit(bf_fit, "QR")
    min = bf_fit.GetMinimumX(0.115*10**(-3), 0.13*10**(-3))
    #print(min)
    par = [bf_fit.GetParameter(k) for k in range(bf_fit.GetNpar())]
    x0 = -par[1]/(2*par[2])
    peak.append(x0)
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
    af_fit = ROOT.TF1("f", "pol2", 0.118*10**(-3), 0.133*10**(-3))
    gr_af.Fit(af_fit, "QR")
    min = af_fit.GetMinimumX(0.118*10**(-3), 0.133*10**(-3))
    #print(min)
    par = [af_fit.GetParameter(k) for k in range(af_fit.GetNpar())]
    x0 = -par[1]/(2*par[2])
    peak.append(x0)
    #print(peak)
    gr_af.Draw("AP")
    ROOT.gStyle.SetOptFit(1)
    c.SetGridx()
    c.SetGridy()
    c.Draw("P")
    gr_af.Draw("P")
    c.Update()

    #time.sleep(1000)

    c.SaveAs(dir_path + str(2*i) + "-" + str(2*i+1) + ".png")

    delta_t = peak[2*i+1]-peak[2*i]
    F_mod = 4001
    F_dev = 500*10**3
    delta_f = delta_t*F_mod*F_dev
    delta_f_list.append(delta_f)
    #print("delta_t = " + str(delta_t))
    #print("delta_f = " + str(delta_f))

print(delta_f_list)

c = ROOT.TCanvas("c", "title", 800, 600)
gr = ROOT.TGraph(Nshift, np.linspace(1, Nshift, Nshift), np.array(delta_f_list))
gr.SetMarkerStyle(3)
gr.SetMarkerSize(1)
gr.GetXaxis().CenterTitle(True)
gr.GetXaxis().SetTitle("number of measurment")
gr.GetYaxis().CenterTitle(True)
gr.GetYaxis().SetTitle("EPR freq. shift [Hz]")
#ROOT.gStyle.SetOptFit(1)
gr.Draw("AP")
#c1 = ROOT.gROOT.FindObject("c1")
c.Draw("same")
c.SaveAs(dir_path + "EPR_Freq_Shift.png")
print(stat.mean(delta_f_list))
print(stat.stdev(delta_f_list))
