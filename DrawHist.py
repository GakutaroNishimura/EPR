import ROOT
import math
import sys
from array import array
import time

argvs = sys.argv  
argc = len(argvs)
data_path = "./FreqValue/"
fig_path = "./EPRshift/"

def DrawHist():
    cv  = ROOT.TCanvas("cv", "Histogram Example", 200, 10, 700, 500)
    i=0
    #files=["Test/TestFrequencyLoop3.txt","Test/TestFrequencyLoop5.txt","Test/TestFrequencyLoop6.txt","Test/TestFrequencyLoop7_2.txt","Test/TestFrequencyLoop7_500Hz.txt"]
    files=["Test/TestFrequencyLoop3_Ave64Factor30705_2.txt","Test/TestFrequencyLoop3_Ave64Factor3_flipflip.txt"]
    h = [ROOT.TH1S('h1', 'px', 200, 9.2e6, 9.3e6),ROOT.TH1S('h2', 'px', 200, 9.2e6, 9.3e6),ROOT.TH1S('h3', 'px', 200, 9.2e6, 9.3e6),ROOT.TH1S('h4', 'px', 200, 9.2e6, 9.3e6),ROOT.TH1S('h5', 'px', 200, 9.2e6, 9.3e6)]
    for j in range(2):
        with open(files[j],"r") as f:
            for line in f:
                elements=line.split(" ")
                for element in elements:
                    if(i%2==1): h[j].Fill(float(element))
                    i=i+1
        if(j==0): h[j].Draw()
        else: h[j].Draw("same")
        h[j].SetLineColor(j+1)
        print("RMS : %f  Mean : %f  MeanError : %f" %(h[j].GetRMS(),h[j].GetMean(), h[j].GetMean(11)))
        cv.Update()
                    

def DrawGraph():
    #files=["Test/TestFrequencyLockin0713_6.txt"]
    #files=["Test/0821_TestNMRFS_2.txt"]
    files=argvs[1]
    #files=["Test/TestFrequencyLockin0719_2.txt"]
    i=0
    j=0
    l=0
    V=[]
    V2=[]
    IB=[]
    t=[]
    Vup=[]
    Vdown=[]
    for j in range(1):
        with open(data_path + files,"r") as f:
            for line in f:
                elements=line.split(" ")
                t.append(j)
                j=j+1
                for element in elements:
                    if(i%3==0):
                        V.append(float(element))
                        #if(t[l]>260 and t[l]<360): Vup.append(float(element))
                        #if(t[l]>150 and t[l]<220): Vdown.append(float(element))
                        
                        #print("%f  %f" %(V[int(i/2)],t[int(i/2)]))
                    if(i%3==1): V2.append(float(element))
                    if(i%3==2):
                        IB.append(float(element))
                        l=l+1
                    i=i+1
    Va=array("d",V)
    ta=array("d",t)
    V2a=array("d",V2)
    IBa=array("d",IB)
    Vupa=array("d",Vup)
    Vdowna=array("d",Vdown)
    
    return Va,V2a,IBa,ta,Vupa, Vdowna, l

def CalPol(DeltaFreq, Temperature, atm):
    mu0=4*math.pi*1e-7 #H/m
    muB=927.401e-26 #J/T
    gI=-0.0002936400
    ge=2.002319 #ge=gJ in Ino silde
    I=5./2. #85Rb spin
    #I=3./2. #87Rb spin
    kappa=4.52+0.00934*Temperature
    muHe=-1.074617e-26 #J/T
    A=1.01191e9 #Hz 85Rb Hyperfine constant
    #B=2e-3#1.9e-3 #T
    #B=1.46519e-3 #T
    B=1.52158e-3 #T
    rhoHe=2.6867e19*1e6*atm #1/m^3
    h=6.626e-34 #J/s
    
    PolHe=DeltaFreq/(2/3*mu0*muB*ge/(h*(2*I+1))*(1+8*I/(2*I+1)**2*muB*ge*B/(h*A))*kappa*muHe*rhoHe)
    
    return PolHe

def CalEnergyLevel(mF,I, B):
    print(mF, I, B)
    mu0=4*math.pi*1e-7 #H/m
    muB=927.401e-26 #J/T
    gI=-0.0002936400
    ge=2.002319 #ge=gJ in Ino silde
    A85=1.01191e9 #Hz 85Rb Hyperfine constant
    A87=3.41734e9 #Hz 87Rb Hyperfine constant
    if(mF>0): sign=1
    if(mF<0): sign=-1
    h=6.626e-34 #J/s
    #DeltaEperh=3035.73e6
    if(I==5/2): DeltaEperh=A85*(I+1/2)
    elif(I==3/2): DeltaEperh=A87*(I+1/2)
    else:
        print("enter I==5/2 or I==3/2")
        return 0
    epsilon=(ge-gI)/(DeltaEperh*h)*muB*B
    
    #DeltaE=-DeltaEperh/(2*(2*I+1))+gI*muB*B*mF+DeltaEperh*(1+4*mF/(2*I+1)*epsilon+epsilon**2)**0.5
    DeltaE=-DeltaEperh/(2*(2*I+1))+gI*muB*B*mF/h+sign*DeltaEperh/2*(1+4*mF/(2*I+1)*epsilon+epsilon**2)**0.5
    #DeltaE=-DeltaEperh/(2*(2*I+1))+gI*muB*B*mF/h+sign*DeltaEperh/2*(1+4*mF/(2*I+1)*epsilon+epsilon**2)**05.
    print(-DeltaEperh/(2*(2*I+1)), gI*muB*B*mF/h, sign*DeltaEperh/2*(1+4*mF/(2*I+1)*epsilon+epsilon**2)**0.5)
    return DeltaE



def DeltaEnergyLevel(mF,I, B):
    if(mF<0): return (CalEnergyLevel(mF+1,I,B)-CalEnergyLevel(mF,I,B))/1e6
    if(mF>0): return (CalEnergyLevel(mF,I,B)-CalEnergyLevel(mF-1,I,B))/1e6
    
if __name__ == '__main__':
    #fB1=CalEnergyLevel(3,5/2,2.0002e-3)-CalEnergyLevel(2,5/2,2.0002e-3)
    #fB2=CalEnergyLevel(3,5/2,2e-3)-CalEnergyLevel(2,5/2,2e-3)
    #fB3=CalEnergyLevel(-3,5/2,2.0002e-3)-CalEnergyLevel(-2,5/2,2.0002e-3)
    #fB4=CalEnergyLevel(-3,5/2,2e-3)-CalEnergyLevel(-2,5/2,2e-3)
    #print(fB4,fB2,fB1-fB2, fB3-fB4, fB2+fB4)
    Va,V2a, IBa, ta,Vupa, Vdowna, Npoint=DrawGraph()
    c=ROOT.TCanvas("c","c",1000,800)
    #Verror=[250 for i in range(Npoint]
    Verror=[0 for i in range(Npoint)]
    terror=[0 for i in range(Npoint)]
    Verrora=array("d",Verror)
    terrora=array("d",terror)
    #c.Divide(2,2)
    c.cd(1)
    g=ROOT.TGraphErrors(int(Npoint), ta, Va,terrora, Verrora)
    # g.GetXaxis().SetRangeUser(1400., 3300.)
    # g.GetYaxis().SetRangeUser(7310000., 7345000.)
    g.SetTitle("")
    g.GetXaxis().SetTitle("number of measurements")
    g.GetYaxis().SetTitle("EPR frequency [Hz]")
    g.GetXaxis().SetLabelSize(0.04)
    g.GetYaxis().SetLabelSize(0.04)
    g.GetXaxis().SetTitleSize(0.06)
    g.GetYaxis().SetTitleSize(0.06)
    g.GetXaxis().SetTitleOffset(0.9)
    g.GetYaxis().SetTitleOffset(1.15)
    g.SetName("HoseiGo")
    g.Draw("APL")
    g.SetMarkerStyle(2)
    ROOT.gPad.SetTopMargin(0.06)
    ROOT.gPad.SetBottomMargin(0.14)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetRightMargin(0.05)
    files = argvs[1]
    c.SaveAs(fig_path + files + ".pdf")
    #g.GetYaxis().SetRangeUser(9200e3,9250e3)
    #g.GetYaxis().SetRangeUser(8.860e6,8.890e6)
    #g.GetYaxis().SetRangeUser(13700e3,13760e3)
    #g.GetYaxis().SetRangeUser(9210e3,9260e3)

    #print(CalPol(10.88e3, 181, 3))
    #print("Polarization %f "%(CalPol(16.14e3/2, 181, 3)))
    #print("Polarization %f "%(CalPol(21.96e3/2, 181, 3)))
    """s
    c.cd(2)
    gIB=ROOT.TGraph(int(Npoint), ta, IBa)
    gIB.Draw("AP")
    gIB.SetMarkerStyle(2)
    gIB.GetYaxis().SetRangeUser(0.835,0.8362)

    #hVdown=ROOT.TH1F("Vdown","Vdown",300,9210e3,9250e3)
    #hVup=ROOT.TH1F("Vup","Vup",300,9210e3,9250e3)
    hVdown=ROOT.TH1F("Vdown","Vdown",300,13705e3,13740e3)
    hVup=ROOT.TH1F("Vup","Vup",300,13705e3,13740e3)
    for x in Vdowna:
        hVdown.Fill(x)
    for x in Vupa:
        hVup.Fill(x)
    c.cd(3)
    ROOT.gStyle.SetOptStat("RMe")
    ROOT.gStyle.SetStatFormat("6.8g");
    hVup.Draw()
    c.Update()
    c.cd(4)
    ROOT.gStyle.SetOptStat("RMe")
    ROOT.gStyle.SetStatFormat("6.8g");
    hVdown.Draw()
    """
    c.Update()
    
    
