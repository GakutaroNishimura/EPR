import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.ticker as ptick
import scipy.special as sp
import glob
import sys
import time

argvs = sys.argv

f_file = 120
l_file = 129

dir_path = "./peak/120-129/crystal_ball/"


def CrystalBall(x, x0, sigma_left, alpha_left, n_left, 
                sigma_right, alpha_right,n_right, const, Cap_N):
  Al = (n_left/np.abs(alpha_left))**n_left*np.exp(-alpha_left**2/2)
  Ar = (n_right/np.abs(alpha_right))**n_right*np.exp(-alpha_right**2/2)
  Bl = n_left/np.abs(alpha_left)-np.abs(alpha_left)
  Br = n_right/np.abs(alpha_right)-np.abs(alpha_right)
  #Cl = (n_left/np.abs(alpha_left))*(1/(n_left-1))*np.exp(-alpha_left**2/2)
  #Cr = (n_right/np.abs(alpha_right))*(1/(n_right-1))*np.exp(-alpha_right**2/2)
  #Dl = np.sqrt(np.pi/2)*(1+sp.erf(np.abs(alpha_left)/np.sqrt(2)))
  #Dr = np.sqrt(np.pi/2)*(1+sp.erf(np.abs(alpha_right)/np.sqrt(2)))
  #Nl = 1/(sigma_left*(Cl+Dl))
  #Nr = 1/(sigma_right*(Cr+Dr))

  if (x-x0)/sigma_left <= -alpha_left:
    y = const-Cap_N*Al*(Bl-(x-x0)/sigma_left)**(-n_left)
  elif -alpha_left< (x-x0)/sigma_left <= 0 :
    y = const-Cap_N*np.exp(-0.5*(x-x0)**2/sigma_left**2)
  elif 0 < (x-x0)/sigma_right <= alpha_right:
     y = const-Cap_N*np.exp(-0.5*(x-x0)**2/sigma_right**2)
  else:
     y = const-Cap_N*Ar*(Br+(x-x0)/sigma_right)**(-n_right)
  return y

crystal_ball = np.vectorize(CrystalBall)


file_path = [] #データのpathをしまうlist.""で囲まれた文字列のリストになる.
for i in range(f_file, l_file+1):
    path = glob.glob("./WaveData/scope_%d.csv"% i)
    file_path.append(path[0])

Nshift = int(len(file_path)/2)

EPRshift_l = []
F_dev = 500*10**3
F_mod = 4001

for i in range(Nshift):
  df_bf = pd.read_csv(file_path[2*i], names = ["time", "signal", "sync"], skiprows=2, skipfooter=1, engine="python")
  df_af = pd.read_csv(file_path[2*i+1], names = ["time", "signal", "sync"], skiprows=2, skipfooter=1, engine="python")

  print("start fitting")
  par, cov = curve_fit(crystal_ball, df_bf.time, df_bf.signal, p0 = (1.24e-04, 1.08390763e-05, 1.12849285e+00, 9.04483335e+01, 2.08097853e-05, 6.07396123e-01, 1.31912331e+02, 2.96644947e-03, 3.20672825e-03))
  x = np.linspace(0.1*10**(-3), 0.175*10**(-3), 1000)
  y = crystal_ball(x, par[0], par[1], par[2], par[3], par[4], par[5], par[6], par[7], par[8])

  t_bf = par[0]
  t_bf = f"{t_bf:.12f}"
  f=open(argvs[1],"a")
  f.write(t_bf + "\n")
  f.close()

  fig, ax = plt.subplots(figsize=(8,6))
  plt.plot(df_bf.time, df_bf.signal, ".", markersize=1)
  plt.plot(x, y)
  plt.grid(which="both")
  ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
  ax.ticklabel_format(style="sci", axis="x", scilimits=(-3,-3))
  ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
  ax.ticklabel_format(style="sci", axis="y", scilimits=(-3,-3))
  plt.savefig(dir_path + str(2*i) + ".png")
  print("fig saved")

  par, cov = curve_fit(crystal_ball, df_af.time, df_af.signal, p0 = (1.25e-04, 1.08390763e-05, 1.12849285e+00, 9.04483335e+01, 2.08097853e-05, 6.07396123e-01, 1.31912331e+02, 2.96644947e-03, 3.20672825e-03))
  x = np.linspace(0.1*10**(-3), 0.175*10**(-3), 1000)
  y = crystal_ball(x, par[0], par[1], par[2], par[3], par[4], par[5], par[6], par[7], par[8])

  t_af = par[0]
  t_af = f"{t_af:.12f}"
  f=open(argvs[1],"a")
  f.write(t_af + "\n")
  f.close()

  fig, ax = plt.subplots(figsize=(8,6))
  plt.plot(df_af.time, df_af.signal)
  plt.plot(x, y)
  plt.grid(which="both")
  ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
  ax.ticklabel_format(style="sci", axis="x", scilimits=(-3,-3))
  ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
  ax.ticklabel_format(style="sci", axis="y", scilimits=(-3,-3))
  plt.savefig(dir_path + str(2*i+1) + ".png")

