import ROOT
import pandas as pd
import numpy as np
import time
import glob


#path = "./peak/56-61/"
#dir_path = "./peak/36-55/test/"
dir_path = "./peak/36-55/SkewedGaus/"
dir_path = "./peak/56-61/SkewedGaus/"

# 読み込むファイルの番号（scope_〇〇.csv）の番号を指定.first_file(f_file)からlast_file(l_file)まで.
# Nfile_bfで保存するファイル名を変える.
f_file = 56
l_file = 61
Nfile_bf = 3
Npeak = 2
file_path = [] #データのpathをしまうlist.""で囲まれた文字列のリストになる.
for i in range(f_file, l_file+1):
    path = glob.glob("./WaveData/scope_%d.csv"% i)
    file_path.append(path[0])

Save = "notSAVE"
peak = []
peak_e = []
peak_ideal = []
EPR_freq_list = []

F_mod = 1000    # modulation freq [Hz]
F_dev = 700     # deviation freq. [kHz]
F_0 = 7225      # 変調磁場の中心周波数 [kHz]
      # 一回で取得するピークの数
Fit_Range = 0.0001*4      # ピークをフィットするときの横軸の幅
canvasWidth = 600
canvasHeight = 300

# noise_fit.pyで得た、sweep磁場がないときのsignalのノイズ.
# averageの回数で大きさが変わる.
Noise = 0.0001097      # noise for df56-df61 [V]
#Noise = 0.0003883       # noise for df36-df55 [V]


# 前ピークを一個ずつフィット.
for j in range(len(file_path)):
    # data frameにデータを読み込み.
    df = pd.read_csv(file_path[j], names = ["time", "signal", "sync"], skiprows = 2)
    for i in range(Npeak):
        Fit_center = 0.000533512052921227-Npeak/2/F_mod+i/F_mod
        print("Fit_center = " + str(Fit_center))
        # create a TGraph with the data
        gr = ROOT.TGraphErrors(len(df.time), np.array(df.time), np.array(df.signal), np.array([0.0 for i in range(len(df.time))]), np.array([Noise for i in range(len(df.time))]))
        # set the fit function and the fit range
        
        #f = ROOT.TF1("f", "[3]-gaus(x,[0],[1],[2])*ROOT::Math::normal_cdf(x,[4],[5])", Fit_center-Fit_Range, Fit_center+Fit_Range) #フィットは合うけどピークの位置とパラメータの関係がわからない.
        #f.SetParameters(0.004061, Fit_center, 7.449*10**(-5), -0.0006041, 7.449*10**(-5), Fit_center) #par for the 36-55, normal_cdf
        
        #f = ROOT.TF1("f", "[3]-gaus(x,[0],[1],[2])*ROOT::Math::normal_cdf([4]*x, 1, 0)", Fit_center-Fit_Range, Fit_center+Fit_Range)
        #f.SetParameters(0.003598, Fit_center, 6.413*10**(-5), 0.0006041, -21) #par for the 56-61, normal_cdf
        
        f = ROOT.TF1("f", "[3] - gaus(x,[0],[1],[2]) + [4]*expo((x-[1])/[5])*TMath::Erfc((x-[1])/(TMath::Sqrt2()*[2])-[2]/(TMath::Sqrt2()*[5]))", Fit_center-Fit_Range, Fit_center+Fit_Range)
        f.SetParameters(0.003598, Fit_center, 6.413*10**(-5), 0.0006041, 1, 1) #par for the 56-61, Takada San's skewed gaus
        
        #f = ROOT.TF1("f", "[3] - gaus(x,[0],[1],[2]) + [4]*expo((x-[1])/[5])*TMath::Erfc((x-[1])/(TMath::Sqrt2()*[2])-[2]/(TMath::Sqrt2()*[5])) + [6]*TMath::Erfc((x-[1])/(TMath::Sqrt2()*[2]))", Fit_center-Fit_Range, Fit_center+Fit_Range)
        #f.SetParameters(0.003598, Fit_center, 6.413*10**(-5), 0.0006041, 1, 1, 1) #par for the 56-61, Takada San's skewed gaus
        
        #f = ROOT.TF1("f", "[3]-gaus(x,[0],[1],[2])*ROOT::Math::normal_cdf(x,[2],[1])", Fit_center-Fit_Range, Fit_center+Fit_Range)        
        # set initial parameter values for the fit
        
        
        
        #f.SetParameters(0.003, Fit_center, 0.0001, 0.0006041) #par for the 56-61
        # perform the fit
        gr.Fit(f, "QR")
        # get the fitted parameters
        par = [f.GetParameter(k) for k in range(f.GetNpar())]
        par_e = [f.GetParError(k) for k in range(f.GetNpar())]
        peak.append(par[1])
        peak_e.append(par_e[1])
        print(par)
        # create a TGraph with the fitted function
        #gr_fit = ROOT.TGraph(1000, np.linspace(Fit_center-Fit_Range, Fit_center+Fit_Range, 1000), np.array([f.Eval(x, *par[1:]) for x in np.linspace(Fit_center-Fit_Range, Fit_center+Fit_Range, 1000)]))
        gr.SetMarkerStyle(1)
        gr.SetMarkerSize(2)
        gr.SetName("a")
        gr.GetXaxis().CenterTitle(True)
        gr.GetXaxis().SetTitle("time [s]")
        gr.GetYaxis().CenterTitle(True)
        gr.GetYaxis().SetTitle("voltage [V]")
        gr.Draw("AP")
        #gr_fit.Draw("same")
        #gr_fit.SetLineColor(2)
        ROOT.gStyle.SetOptFit(1)    #グラフに統計ボックスを表示.
        c1 = ROOT.gROOT.FindObject("c1")
        c1.Draw("AP")
        gr.Draw("same")
        c1.Update()
        if Save == "SAVE":
            if j < Nfile_bf:
                c1.SaveAs(dir_path + "e_bf" + str(j) + "_peak" +  str(i) + ".pdf")
                c1.SaveAs(dir_path + "e_bf" + str(j) + "_peak" +  str(i) + ".png")
            else:
                c1.SaveAs(dir_path + "e_af" + str(j-10) + "_peak" +  str(i) + ".pdf")
                c1.SaveAs(dir_path + "e_af" + str(j-10) + "_peak" +  str(i) + ".png")
        if i == 0:
            time.sleep(10000)
        

# 一つのピークの時刻から、他のピークの時刻を求める.
# ピーク数が奇数の場合は未対応.
# p_zenhan、p_kouhanは取得するピークの数によって変わる.
# データの中心（時刻０）から左のピークと、中心のすぐ右のピークがp_zenhan.
# p_zenhanは中心のすぐ右のピークの時刻から、1/F_modずつ引いた時刻を計算して、idealなピークの時刻を求めている.
# p_kouhanは中心のすぐ右のピークの時刻に、1/F_modずつ足した時刻を計算している.
k = 0
for j in range(len(file_path)):
    if Npeak == 2:
        for i in range(2):
            p = peak[1+2*j] -1/F_mod + i/F_mod
            peak_ideal.append(p)
    else:
        p_zenhan = peak[k : k+int(Npeak/2)+1]
        p_kouhan = peak[k+int(Npeak/2)+1 : k+Npeak]
        for i in range(0, int(Npeak/2)+1):
            p = peak[int(Npeak/2)+2*j*int(Npeak/2)] -Npeak/2/F_mod + i/F_mod
            peak_ideal.append(p)
            k += 1

        for i in range(1, int(Npeak/2)):
            p = peak[int(Npeak/2)+2*j*int(Npeak/2)] + i/F_mod
            peak_ideal.append(p)
            k += 1

    

# 各ピークについて、peak_idealとpeakの時間差を計算.
peak_dev = [peak[i]-peak_ideal[i] for i in range(len(peak))]


# peak_devで得た時間差に対応する周波数を計算.
f_dev = [F_mod*F_dev*i for i in peak_dev]


#convert time errors to freq. errors.
f_e = [F_mod*F_dev*i for i in peak_e]


#calculate the EPR freq. of all peaks.
# 時刻０の右隣のピークのEPR周波数を求め、時刻が負のピークと、時刻０の右隣の更に右のピークたちに、f_devを加えていく.
for i in range(len(file_path)):
    iEPR_freq = F_dev*F_mod*peak[int(Npeak/2)+2*i*int(Npeak/2)]+F_0-F_dev/2
    for j in f_dev[Npeak*i:Npeak*i+Npeak]:
        EPR_freq = iEPR_freq+j
        EPR_freq_list.append(EPR_freq)


EPR_freq_list = EPR_freq_list
EPR_freq_list_e = f_e
NPoint = len(EPR_freq_list)
index = [i for i in range(1, NPoint+1, 1)]

gr = ROOT.TGraphErrors(NPoint, np.array(index, dtype="float"), np.array(EPR_freq_list), np.array([0.0 for i in range(len(EPR_freq_list))]), np.array(EPR_freq_list_e))
gr.SetMarkerStyle(3)
gr.SetMarkerSize(1)
gr.SetName("a")
gr.GetXaxis().CenterTitle(True)
gr.GetXaxis().SetTitle("number of measurment")
gr.GetYaxis().CenterTitle(True)
gr.GetYaxis().SetTitle("EPR freq. [kHz]")
gr.Draw("AP")
c1 = ROOT.gROOT.FindObject("c1")
c1.SaveAs(dir_path + "EPRfreq.pdf")
c1.SaveAs(dir_path + "EPRfreq.png")
