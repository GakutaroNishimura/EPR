import ROOT
import pandas as pd
import numpy as np
import time
import glob


#path = "./peak/56-61/"
dir_path = "./peak/36-55/test/"

# 読み込むファイルの番号（scope_〇〇.csv）の番号を指定。first_file_beforeflip(f_file_bf)から-->.
# -->last_file_beforeflip(l_file_bf)までが、フリップ前のデータ.
# f_file_afからl_file_afがフリップ後.
f_file_bf = 36
l_file_bf = 45
f_file_af = 46
l_file_af = 55
file_path_bf = [] #データのpathｗｐしまうlist.""で囲まれた文字列のリストになる.
file_path_af = []
for i in range(f_file_bf, l_file_bf+1):
    path = glob.glob("./WaveData/scope_%d.csv"% i)
    file_path_bf.append(path[0])
    
for i in range(f_file_af, l_file_af+1):
    path = glob.glob("./WaveData/scope_%d.csv"% i)
    file_path_af.append(path[0])

peak_bf = []
peak_af = []
peak_bf_e = []
peak_af_e = []
peak_ideal_bf = []
peak_ideal_af = []
EPR_freq_list = []
EPR_freq_list_bf = []
EPR_freq_list_af = []

F_mod = 1000 #[Hz]
F_dev = 700 #[kHz]
F_0 = 7225 #[kHz]
Npeak = 10
Fit_Range = 0.0001
canvasWidth = 600
canvasHeight = 300

# noise_fit.pyで得た、sweep磁場がないときのsignalのノイズ.
# averageの回数で大きさが変わる.
#Noise = 0.0001097 # noise for df56-df61
Noise = 0.0003883 # noise for df36-df55


# flip前のデータのピークをフィット.
for j in range(len(file_path_bf)):
    # data frameにデータを読み込み.
    df = pd.read_csv(file_path_bf[j], names = ["time", "signal", "sync"], skiprows = 2)
    for i in range(Npeak):
        Fit_center = 0.000533512052921227-Npeak/2/F_mod+i/F_mod
        # create a TGraph with the data
        gr = ROOT.TGraphErrors(len(df.time), np.array(df.time), np.array(df.signal), np.array([0.0 for i in range(len(df.time))]), np.array([Noise for i in range(len(df.time))]))
        # set the fit function and the fit range
        f = ROOT.TF1("f", "[0]-gaus(x, [1], [2], [3])", Fit_center-Fit_Range, Fit_center+Fit_Range)
        # set initial parameter values for the fit
        f.SetParameters(0, 0.003, Fit_center, 6*10**(-5))
        # perform the fit
        gr.Fit(f, "QR")
        # get the fitted parameters
        par = [f.GetParameter(k) for k in range(f.GetNpar())]
        par_e = [f.GetParError(k) for k in range(f.GetNpar())]
        peak_bf.append(par[2])
        peak_bf_e.append(par_e[2])
        # create a TGraph with the fitted function
        gr_fit = ROOT.TGraph(1000, np.linspace(Fit_center-Fit_Range, Fit_center+Fit_Range, 1000), np.array([f.Eval(x, *par[1:]) for x in np.linspace(Fit_center-Fit_Range, Fit_center+Fit_Range, 1000)]))
        gr.SetMarkerStyle(1)
        gr.SetMarkerSize(2)
        gr.SetName("a")
        gr.GetXaxis().CenterTitle(True)
        gr.GetXaxis().SetTitle("time [s]")
        gr.GetYaxis().CenterTitle(True)
        gr.GetYaxis().SetTitle("voltage [V]")
        gr.Draw("AP")
        gr_fit.Draw("same")
        gr_fit.SetLineColor(2)
        ROOT.gStyle.SetOptFit(1)
        c1 = ROOT.gROOT.FindObject("c1")
        c1.SaveAs(dir_path + "e_bf" + str(j) + "_peak" +  str(i) + ".pdf")
        c1.SaveAs(dir_path + "e_bf" + str(j) + "_peak" +  str(i) + ".png")
        #time.sleep(10000)
        
        

for j in range(len(file_path_af)):
    df = pd.read_csv(file_path_af[j], names = ["time", "signal", "sync"], skiprows = 2)
    for i in range(Npeak):
        #Fit_center = 0.0005471147644754069-Npeak/2/F_mod+i/F_mod
        Fit_center = 0.000533512052921227-Npeak/2/F_mod+i/F_mod
        # create a TGraph with the data
        gr = ROOT.TGraphErrors(len(df.time), np.array(df.time), np.array(df.signal), np.array([0.0 for i in range(len(df.time))]), np.array([Noise for i in range(len(df.time))]))
        # set the fit function and the fit range
        f = ROOT.TF1("f", "[0]-gaus(x, [1], [2], [3])", Fit_center-Fit_Range, Fit_center+Fit_Range)
        # set initial parameter values for the fit
        f.SetParameters(0, 0.003, Fit_center, 6*10**(-5))
        # perform the fit
        gr.Fit(f, "QR")
        # get the fitted parameters
        par = [f.GetParameter(k) for k in range(f.GetNpar())]
        par_e = [f.GetParError(k) for k in range(f.GetNpar())]
        #print(par)
        #print(par_e)
        peak_af.append(par[2])
        peak_af_e.append(par_e[2])
        # create a TGraph with the fitted function
        gr_fit = ROOT.TGraph(1000, np.linspace(Fit_center-Fit_Range, Fit_center+Fit_Range, 1000), np.array([f.Eval(x, *par[1:]) for x in np.linspace(Fit_center-Fit_Range, Fit_center+Fit_Range, 1000)]))
        gr.SetMarkerStyle(1)
        gr.SetMarkerSize(2)
        #gr.GetXaxis().SetRangeUser(250., 500.)
        #gr.GetYaxis().SetRangeUser(0.98,1.02)
        gr.SetName("a")
        gr.GetXaxis().CenterTitle(True)
        gr.GetXaxis().SetTitle("time")
        gr.GetYaxis().CenterTitle(True)
        gr.GetYaxis().SetTitle("voltage")
        gr.Draw("AP")
        gr_fit.Draw("same")
        gr_fit.SetLineColor(2)
        ROOT.gStyle.SetOptFit(1)
        c1 = ROOT.gROOT.FindObject("c1")
        c1.SaveAs(dir_path + "e_af" + str(j) + "_peak" +  str(i) + ".pdf")
        c1.SaveAs(dir_path + "e_af" + str(j) + "_peak" +  str(i) + ".png")
        #time.sleep(10000)
    
        

# 一つのピークの時刻から、他のピークの時刻を求める.
# p_zenhan、p_kouhanは取得するピークの数によって変わる.奇数は未対応.
# データの中心（時刻０）から左のピークと、中心のすぐ右のピークがp_zenhan.
# p_zenhanは中心のすぐ右のピークの時刻から、1/F_modずつ引いた時刻を計算して、idealなピークの時刻を求めている.
# p_kouhanは中心のすぐ右のピークの時刻に、1/F_modずつ足した時刻を計算している.
k = 0
for j in range(len(file_path_bf)):
    if Npeak == 2:
        for i in range(2):
            p = peak_bf[1+2*j] -1/F_mod + i/F_mod
            peak_ideal_bf.append(p)
    else:
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

       
for j in range(len(file_path_af)):
    if Npeak == 2:
        for i in range(2):
            p = peak_af[1+2*j] -1/F_mod + i/F_mod
            peak_ideal_af.append(p)
    else:
        p_zenhan = peak_af[k : k+int(Npeak/2)+1]
        p_kouhan = peak_af[k+int(Npeak/2)+1 : k+Npeak]
        for i in range(0, int(Npeak/2)+1):
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


#convert time errors to freq. errors
f_bf_e = [F_mod*F_dev*i for i in peak_bf_e]
#print(f_bf_e)
f_af_e = [F_mod*F_dev*i for i in peak_af_e]


#calculate the EPR freq. of all peaks
# 時刻０の右隣のピークのEPR周波数を求め、時刻が負のピークと、時刻０の右隣の更に右のピークたちに、f_devを加えていく.
for i in range(len(file_path_bf)):
    iEPR_freq = F_dev*F_mod*peak_bf[int(Npeak/2)+2*i*int(Npeak/2)]+F_0-F_dev/2
    for j in f_dev_bf[Npeak*i:Npeak*i+Npeak]:
        EPR_freq_bf = iEPR_freq+j
        EPR_freq_list_bf.append(EPR_freq_bf)


for i in range(len(file_path_af)):
    iEPR_freq = F_dev*F_mod*peak_af[int(Npeak/2)+2*i*int(Npeak/2)]+F_0-F_dev/2
    for j in f_dev_af[Npeak*i:Npeak*i+Npeak]:
        EPR_freq_af = iEPR_freq+j
        EPR_freq_list_af.append(EPR_freq_af)

#print(EPR_freq_list_bf)
EPR_freq_list = EPR_freq_list_bf + EPR_freq_list_af
EPR_freq_list_e = f_bf_e + f_af_e
#print(EPR_freq_list)
#print(EPR_freq_list_e)
NPoint = len(EPR_freq_list)
index = [i for i in range(1, NPoint+1, 1)]

gr = ROOT.TGraphErrors(NPoint, np.array(index, dtype="float"), np.array(EPR_freq_list), np.array([0.0 for i in range(len(EPR_freq_list))]), np.array(EPR_freq_list_e))
gr.SetMarkerStyle(3)
gr.SetMarkerSize(1)
#gr.GetXaxis().SetRangeUser(0., 13.)
#gr.GetYaxis().SetRangeUser(0.98,1.02)
gr.SetName("a")
gr.GetXaxis().CenterTitle(True)
gr.GetXaxis().SetTitle("number of measurment")
gr.GetYaxis().CenterTitle(True)
gr.GetYaxis().SetTitle("EPR freq. [kHz]")
gr.Draw("AP")
c1 = ROOT.gROOT.FindObject("c1")
c1.SaveAs(dir_path + "EPRfreq.pdf")
c1.SaveAs(dir_path + "EPRfreq.png")

#print(peak_bf)
#print(peak_af)
        
        
        
        
        
        
        
        

"""
        if i == Npeak-1:
            # save the plot
            #print("Aaaaa")
            #c = ROOT.gROOT.FindObject("c")
            #time.sleep(10000)
            c.Update()
            #time.sleep(10000)
            c.SaveAs(path_56to61 + "bf" + str(j) + ".png")
            c.Close()
            #c.SaveAs(path_56to61 + "bf" + str(j) + ".png")
    #ROOT.gROOT.GetListOfCanvases().Delete() # delete the canvas and the TGraphs  
"""