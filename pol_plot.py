import numpy as np
import pandas as pd
import ROOT
import time

df = pd.read_csv("pol1.csv", names=["pol", "pol_dev"], skiprows=1)

df120 = df[:5]
df110 = df[5:10]
df100 = df[10:12]
df90 = df[12:15]

index = np.linspace(1.0, 15.0, len(df))

N120 = len(df120.pol)
N110 = len(df110.pol)
N100 = len(df100.pol)
N90 = len(df90.pol)

c1 = ROOT.TCanvas("c1", "title", 400, 400)
gr = ROOT.TGraph(15, index, np.array(df.pol))
gr.SetTitle(";number of measurements;polarization %;")
gr120 = ROOT.TGraphErrors(N120, index[:5], np.array(df120.pol), np.array([0.0 for i in range(N120)]), np.array(df120.pol_dev))
gr120.SetMarkerStyle(7)
gr120.SetMarkerColor(ROOT.kRed)
gr120.SetLineColor(ROOT.kRed)
gr110 = ROOT.TGraphErrors(N110, index[5:10], np.array(df110.pol), np.array([0.0 for i in range(N110)]), np.array(df110.pol_dev))
gr110.SetMarkerStyle(25)
gr110.SetMarkerSize(0.5)
gr110.SetMarkerColor(ROOT.kBlue)
gr110.SetLineColor(ROOT.kBlue)
gr100 = ROOT.TGraphErrors(N100, index[10:12], np.array(df100.pol), np.array([0.0 for i in range(N100)]), np.array(df100.pol_dev))
gr100.SetMarkerStyle(22)
gr100.SetMarkerColor(ROOT.kBlack)
gr100.SetLineColor(ROOT.kBlack)
gr90 = ROOT.TGraphErrors(N90, index[12:15], np.array(df90.pol), np.array([0.0 for i in range(N90)]), np.array(df90.pol_dev))
gr90.SetMarkerStyle(21)
gr90.SetMarkerSize(0.5)
gr90.SetMarkerColor(ROOT.kMagenta)
gr90.SetLineColor(ROOT.kMagenta)
gr.SetMarkerStyle(1)
gr.Draw("AP")
gr120.Draw("P")
gr110.Draw("P")
gr100.Draw("P")
gr90.Draw("P")
c1.SetGridx()
c1.SetGridy()
c1.BuildLegend()
c1.Draw("same")


time.sleep(1000)
