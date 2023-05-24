import ROOT
#from ROOT import TMath
import pandas as pd
import numpy as np
import statistics as stat
import time
import glob


#path = "./peak/56-61/"
#dir_path = "./peak/36-55/test/"
dir_path = "./peak/"
#dir_path = "../../../mnt/c/Users/owner/python/research/wsl/EPR/peak/36-55/test/"
#dir_path = "../../../mnt/c/Users/owner/python/research/wsl/EPR/peak/56-61/error/"

#Save figure or not
Save = "Save"

#df = pd.read_csv("./WaveData/scope_61.csv", names = ["time", "signal", "sync"], skiprows=2)
df = pd.read_csv("./WaveData/scope_120.csv", names = ["time", "signal", "sync"], skiprows = 2, skipfooter=1, engine="python")


peak = []
peak_e = []
peak_ideal = []
EPR_freq_list = []
EPR_freq_list_e = []

F_mod = 1000    # modulation freq [Hz]
F_dev = 700     # deviation freq. [kHz]
F_0 = 7225      # 変調磁場の中心周波数 [kHz]
Npeak = 2      # 一回で取得するピークの数
Fit_Range = 0.0001*3      # ピークをフィットするときの横軸の幅
canvasWidth = 600
canvasHeight = 300

# noise_fit.pyで得た、sweep磁場がないときのsignalのノイズ.
# averageの回数で大きさが変わる.
Noise = 0.0001097      # noise for df56-df61 [V]
#Noise = 0.0003883       # noise for df36-df55 [V]


# 前ピークを一個ずつフィット.
Fit_center = 0.000533512052921227-Npeak/2/F_mod
# create a TGraph with the data
#gr = ROOT.TGraphErrors(len(df.time), np.array(df.time), np.array(df.signal), np.array([0.0 for i in range(len(df.time))]), np.array([Noise for i in range(len(df.time))]))
gr = ROOT.TGraph(len(df.time), np.array(df.time), np.array(df.signal))
# set the fit function and the fit range
"""
def func1(x, p0, a, mean, sigma):
    return p0-a*TMath.Gaus(x, mean, sigma)
def func2(x, mean, sigma):
    return 1+TMath.Erf((x-mean)/sigma)
f1 = ROOT.TF1("func1", func1, Fit_center-Fit_Range, Fit_center+Fit_Range)
f2 = ROOT.TF1("func2", func2, Fit_center-Fit_Range, Fit_center+Fit_Range)
f = ROOT.TF1("fit_func", "func1(x, [0], [1], [2], [3])*func2(x, [4], [5])", Fit_center-Fit_Range, Fit_center+Fit_Range)
# set initial parameter values for the fit
f.SetParameters(0, 0.003, Fit_center, 6*10**(-5), Fit_center, 6*10**(-5))
# perform the fit
gr.Fit(f, "QR")
# get the fitted parameters
par = [f.GetParameter(k) for k in range(f.GetNpar())]
par_e = [f.GetParError(k) for k in range(f.GetNpar())]
peak.append(par[2])
peak_e.append(par_e[2])
"""
if Save == "Save":
    # create a TGraph with the fitted function
    #gr_fit = ROOT.TGraph(1000, np.linspace(Fit_center-Fit_Range, Fit_center+Fit_Range, 1000), np.array([f.Eval(x, *par[1:]) for x in np.linspace(Fit_center-Fit_Range, Fit_center+Fit_Range, 1000)]))
    gr.SetMarkerStyle(1)
    gr.SetMarkerSize(2)
    gr.SetName("a")
    gr.GetXaxis().CenterTitle(True)
    gr.GetXaxis().SetTitle("time [s]")
    gr.GetYaxis().CenterTitle(True)
    gr.GetYaxis().SetTitle("voltage [V]")
    gr.SetMarkerStyle(7)
    gr.Draw("APL")
    #gr_fit.Draw("same")
    #gr_fit.SetLineColor(2)
    ROOT.gStyle.SetOptFit(1)    #グラフに統計ボックスを表示.
    c1 = ROOT.gROOT.FindObject("c1")
    c1.Draw("same")
    time.sleep(10000)
    #c1.SaveAs(dir_path + "test.pdf")
    c1.SaveAs(dir_path + "test.png")
