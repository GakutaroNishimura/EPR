import numpy as np
import pandas as pd
import sys

argvs = sys.argv
path = "./FreqValue/"

T = 0 
mu_0 = 1.25663*10**(-6)          #[m kg s^-2 A^-2]
mu_B = 9.27401*10**(-24)         #[J T^-1] = [m^2 A]
mu_He = -1.07461*10**(-26)       #[J T^-1] = [m^2 A]
mu_N = 5.05078*10**(-27)
mu_Xe_131 = 0.687020*mu_N
mu_Xe_129 = -0.777960*mu_N
g_I = -0.000293640
g_e = -2.00231
#g_J = 2.002332
I = 5/2
A = 1.01191*10**9                #[s^-1]
He_num = 2.68678*3.3*10**25      #[m^-3]
Xe_num = 5.88*10**3*6.02*10**23/131.3           #[m^-3]
B = 1.5*10**(-3)                 #[T]
kappa_Xe = 518
h = 6.62607*10**(-34)  #[J s]

def EPRshift(bfs, bff, afs, aff):
    files = path + argvs[2]
    df = pd.read_table(files, usecols=[0], names=["EPRfreq."], sep=" ")
    df1 = df.iloc[bfs:bff, 0]
    df2 = df.iloc[afs:aff, 0]
    df1_mean = df1.mean()
    df2_mean = df2.mean()
    df1_std = df1.std()
    df2_std = df2.std()
    delta_EPR = df1_mean-df2_mean
    delta_EPR_std = np.sqrt(df1_std**2+df2_std**2)

    return df1_mean, df2_mean, delta_EPR, delta_EPR_std


def CalPol(delta_EPR, delta_EPR_std):
    abs_Pol = 100*delta_EPR/(2*(2*mu_0/3)*(mu_B*g_e/(h*(2*I+1)))*(1-(8*I/(2*I+1)**2)*(mu_B*g_e*B/(h*A)))*kappa_Xe*mu_Xe_129*Xe_num)
    abs_Pol_std = 100*delta_EPR_std/(2*(2*mu_0/3)*(mu_B*g_e/(h*(2*I+1)))*(1-(8*I/(2*I+1)**2)*(mu_B*g_e*B/(h*A)))*kappa_Xe*mu_Xe_129*Xe_num)

    return abs_Pol, abs_Pol_std


if __name__ == "__main__":
    bfs = input("flip前のスタート地点を入力してください : ")
    bfs = int(bfs)
    bff = input("flip前の終了地点を入力してください : ")
    bff = int(bff)
    afs = input("flip後のスタート地点を入力してください : ")
    afs = int(afs)
    aff = input("flip後の終了地点を入力してください : ")
    aff = int(aff)

    df1_mean, df2_mean, delta_EPR, delta_EPR_std = EPRshift(bfs, bff, afs, aff)

    print("bfEPRfreq. : %f   afEPRfreq. : %f  delta_EPR : %f  delta_EPR_std : %f" %(df1_mean, df2_mean, delta_EPR, delta_EPR_std))

    abs_pol, abs_pol_std = CalPol(delta_EPR, delta_EPR_std)

    print("abs_pol : %f    abs_pol_std : %f" %(abs_pol, abs_pol_std))

    f=open(argvs[1],"a")
    f.write("%f %f\n" %(abs_pol, abs_pol_std))
    f.close()