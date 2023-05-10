import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ROOT
import time
import glob

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
dir_path = "./peak/120-129/normal_cdf/"

Nshift = int(len(file_path)/2)

for i in range(Nshift):
    df_bf = pd.read_csv(file_path[2*i], names = ["time", "signal", "sync"], skiprows=2, skipfooter=1, engine="python")
    df_af = pd.read_csv(file_path[2*i+1], names = ["time", "signal", "sync"], skiprows=2, skipfooter=1, engine="python")

    c = ROOT.TCanvas("c", "title", 800, 1200)
    c.Divide(1,2)
    if i == 2:
        c.cd(1)
        gr_bf = ROOT.TGraphErrors(len(df_bf.time), np.array(df_bf.time), np.array(df_bf.signal), np.array([0.0 for i in range(len(df_bf.time))]), np.array([Noise for i in range(len(df_bf.time))]))

        bf_fit = ROOT.TF1("f", "[3] - gaus(x,[0],[1],[2])*ROOT::Math::normal_cdf(x, [4], [5])", 0.113*10**(-3), 0.131*10**(-3))
        #bf_fit.SetParameters(0.006587, 1.247*10**(-4), 1.826*10**(-5), 0.005733, 1, -1)
        bf_fit.SetParameters(0.008505, 1.23*10**(-4), 1.97*10**(-5), 0.008189, 0.002095, -1.338)
        gr_bf.Fit(bf_fit, "QR")
        min = bf_fit.GetMinimumX(0.115*10**(-3), 0.131*10**(-3))
        #print(min)
        #par = [bf_fit.GetParameter(k) for k in range(bf_fit.GetNpar())]
        #par_e = [bf_fit.GetParError(k) for k in range(bf_fit.GetNpar())]
        #print(par_e)
        #x0 = -par[1]/(2*par[2])
        peak.append(min)
        #print(peak)
        gr_bf.SetMarkerStyle(7)
        gr_bf.SetMarkerSize(4)
        gr_bf.Draw("AP")
        ROOT.gStyle.SetOptFit(1)
        c.SetGridx()
        c.SetGridy()
        c.Draw("P")
        gr_bf.Draw("P")
        c.Update()

        c.cd(2)
        gr_af = ROOT.TGraphErrors(len(df_af.time), np.array(df_af.time), np.array(df_af.signal), np.array([0.0 for i in range(len(df_af.time))]), np.array([Noise for i in range(len(df_af.time))]))
        af_fit = ROOT.TF1("f", "[3] - gaus(x,[0],[1],[2])*ROOT::Math::normal_cdf(x, [4], [5])", 0.115*10**(-3), 0.133*10**(-3))
        #af_fit.SetParameters(0.006587, 1.247*10**(-4), 1.826*10**(-5), 0.005733, 1, -1)
        af_fit.SetParameters(0.008505, 1.27*10**(-4), 1.97*10**(-5), 0.008189, 0.002795, -3.27)
        gr_af.Fit(af_fit, "QR")
        min = af_fit.GetMinimumX(0.118*10**(-3), 0.133*10**(-3))
        peak.append(min)
        #print(peak)
        gr_af.SetMarkerStyle(7)
        gr_af.SetMarkerSize(4)
        gr_af.Draw("AP")
        ROOT.gStyle.SetOptFit(1)
        c.SetGridx()
        c.SetGridy()
        c.Draw("P")
        gr_af.Draw("P")
        c.Update()

        #time.sleep(10000)
        c.SaveAs(dir_path + str(2*i) + "-" + str(2*i+1) + ".png")

        delta_t = peak[2*i+1]-peak[2*i]
        F_mod = 4001
        F_dev = 500*10**3
        delta_f = delta_t*F_mod*F_dev
        delta_f_list.append(delta_f)
        #print("delta_t = " + str(delta_t))
        #print("delta_f = " + str(delta_f))

    else:
        c.cd(1)
        gr_bf = ROOT.TGraphErrors(len(df_bf.time), np.array(df_bf.time), np.array(df_bf.signal), np.array([0.0 for i in range(len(df_bf.time))]), np.array([Noise for i in range(len(df_bf.time))]))

        #bf_fit = ROOT.TF1("f", "[3] - gaus(x,[0],[1],[2])*ROOT::Math::normal_cdf(x, [4], [5])", 0.113*10**(-3), 0.131*10**(-3))
        bf_fit = ROOT.TF1("f", "[3] - gaus(x,[0],[1],[2])*ROOT::Math::normal_cdf(x, [4], [5])", 0.116*10**(-3), 0.131*10**(-3))
        #bf_fit.SetParameters(0.006587, 1.247*10**(-4), 1.826*10**(-5), 0.005733, 1, -1)
        bf_fit.SetParameters(0.01, 1.24*10**(-4), 1.97*10**(-5), 0.008189, 0.002095, -1.338)
        gr_bf.Fit(bf_fit, "QR")
        min = bf_fit.GetMinimumX(0.115*10**(-3), 0.131*10**(-3))
        #print(min)
        #par = [bf_fit.GetParameter(k) for k in range(bf_fit.GetNpar())]
        #par_e = [bf_fit.GetParError(k) for k in range(bf_fit.GetNpar())]
        #print(par_e)
        #x0 = -par[1]/(2*par[2])
        peak.append(min)
        #print(peak)
        gr_bf.SetMarkerStyle(7)
        gr_bf.SetMarkerSize(4)
        gr_bf.Draw("AP")
        ROOT.gStyle.SetOptFit(1)
        c.SetGridx()
        c.SetGridy()
        c.Draw("P")
        gr_bf.Draw("P")
        c.Update()


        c.cd(2)
        c.SetGridx()
        c.SetGridy()
        gr_af = ROOT.TGraphErrors(len(df_af.time), np.array(df_af.time), np.array(df_af.signal), np.array([0.0 for i in range(len(df_af.time))]), np.array([Noise for i in range(len(df_af.time))]))
        af_fit = ROOT.TF1("f", "[3] - gaus(x,[0],[1],[2])*ROOT::Math::normal_cdf(x, [4], [5])", 0.118*10**(-3), 0.133*10**(-3))
        #af_fit.SetParameters(0.006587, 1.247*10**(-4), 1.826*10**(-5), 0.005733, 1, -1)
        af_fit.SetParameters(0.008505, 1.278*10**(-4), 1.97*10**(-5), 0.008189, 0.002095, -1.338)
        gr_af.Fit(af_fit, "QR")
        min = af_fit.GetMinimumX(0.118*10**(-3), 0.133*10**(-3))
        peak.append(min)
        #print(peak)
        gr_af.SetMarkerStyle(7)
        gr_af.SetMarkerSize(4)
        gr_af.Draw("AP")
        ROOT.gStyle.SetOptFit(1)
        c.Draw("P")
        gr_af.Draw("P")

        c.Update()

        time.sleep(10000)
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
#time.sleep(10000)

