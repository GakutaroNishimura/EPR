import pandas as pd
import numpy as np
import ROOT
import time

#df_noise = pd.read_csv("./WaveData/scope_67.csv", names = ["time", "signal", "monitor", "sync", "math"], skiprows = 2)
#df_noise = pd.read_csv("./WaveData/scope_66.csv", names = ["time", "signal", "monitor", "sync", "math"], skiprows = 2)
df_noise = pd.read_csv("./WaveData/scope_160.csv", names = ["time", "signal", "sync"], skiprows = 3)



#path = "./peak/56-61/"
#path = "./peak/36-55/"
path = "./peak/100-119/"
#gr = ROOT.TGraph(len(df_noise.time), np.array(df_noise.time), np.array(df_noise.signal))
#gr.Draw("AP")
#time.sleep(1000)
c1 = ROOT.TCanvas("c1","My Canvas",1600,900)
c2 = ROOT.TCanvas("c2","My Canvas",1600,900)

#range for scope_67.csv
#x_min, x_max, y_min, y_max = -0.0012, 0.0012, 0.0014, 0.0023
#range for scope_66.csv
#x_min, x_max, y_min, y_max = -0.006, 0.006, -0.001, 0.002
#range for scope_160.csv
x_min, x_max, y_min, y_max = -180*10**(-6), -60*10**(-6), 0.00224, 0.0023

c1.cd()

gr = ROOT.TH2F("hist", "noise", 2400, x_min, x_max, 50, y_min, y_max)

for i in range(len(df_noise.time)):
    x = df_noise.time[i]
    y = df_noise.signal[i]
    gr.Fill(x, y)

gr.Draw()

proj_fit = gr.ProjectionY()

c2.cd()
f = ROOT.TF1("f", "gaus", y_min, y_max)
f.SetParameters(5., 0., 0.0005)
proj_fit.Fit(f, "QR")

c1.SaveAs(path + "noise_data.pdf")
c1.SaveAs(path + "noise_data.png")
c2.SaveAs(path + "noise_fit.pdf")
c2.SaveAs(path + "noise_fit.png")

time.sleep(10000)
