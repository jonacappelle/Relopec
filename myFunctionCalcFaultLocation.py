# FAULT CALCULATION

import numpy as np
import copy
import numpy as np
import itertools
from numpy.linalg import multi_dot
from numpy.linalg import inv
import matplotlib.pyplot as plt
import math
import timeit
import time
# from numba import njit, jit, prange

if __name__ == '__main__':
    pass

def calculate_optimized(iF, vF, Ts, tn):
    ZfFict=np.zeros((2,len(tn)))

    for n in np.arange(1,len(tn) - 1,1):
        A_matrix=[[iF[n] - iF[n - 1],np.dot((iF[n - 1] + iF[n]),Ts) / 2], [iF[n + 1] - iF[n],np.dot((iF[n + 1] + iF[n]),Ts) / 2]]
        B_matrix=[[np.dot((vF[n - 1] + vF[n]),(Ts/2))], [np.dot((vF[n] + vF[n + 1]),(Ts/2))]]
        ZfFict[:,[n]]= np.dot(np.linalg.pinv(A_matrix),B_matrix) # Compute pseudo inverse of matrix if it can't be inversed

    return ZfFict

def Fault(vF=None,i2=None,X=None,Ts=None,tn=None,FaultType=None,estFaultStableTime=None,*args,**kwargs):
    
    iF = None

    # voltage at the (assumed) fault location
    vFa=vF[0,:]
    vFb=vF[1,:]
    vFc=vF[2,:]
    
    iaBf=i2[0,:]
    ibBf=i2[1,:]
    icBf=i2[2,:]
    
    iaAf=X[0,:]
    ibAf=X[1,:]
    icAf=X[2,:]
    
    if 1 == (FaultType):
        vF=copy.copy(vFb)
        iF=(ibBf - ibAf)
    else:
        if 2 == (FaultType):
            vF=vFa - vFb
            iF=(iaBf - iaAf) - (ibBf - ibAf)
        else:
            if 3 == (FaultType):
                vF=vFb - vFc
                iF=(ibBf - ibAf) - (icBf - icAf)
            else:
                if 4 == (FaultType):
                    vF=vFc - vFa
                    iF=(icBf - icAf) - (iaBf - iaAf)
                else:
                    if 5 == (FaultType):
                        vF=copy.copy(vFa)
                        iF=(iaBf - iaAf)
    
    ZfFict = calculate_optimized(iF, vF, Ts, tn)

    # Find the overal inducance and resistance by taking the average over one period (0.02 seconds for 50 hertz) this step requires us to know the time of fault inception
    index1=np.argwhere(tn >= estFaultStableTime - 0.02)
    if(index1[0][0] == 0 ):
        print("Choose a bigger window")
    index2=np.argwhere(tn >= estFaultStableTime)

    LfFict=np.mean(ZfFict[0,index1[0][0]:index2[0][0]])
    RfFict=np.mean(ZfFict[1,index1[0][0]:index2[0][0]]) # This is not even necessary I guess
    return LfFict,RfFict,ZfFict

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth 

def removeOutliers(x, y):
    # y = np.array(y[:,0])
    y = np.array(y)
    x = np.array(x)
    mean = np.mean(y)
    standard_deviation = np.std(y)
    distance_from_mean = abs(y - mean)
    max_deviations = 1
    not_outlier = distance_from_mean < max_deviations * standard_deviation
    y_noOutliers = y[not_outlier]
    x_noOutliers = x[not_outlier]
    return x_noOutliers, y_noOutliers

def findZeroCross(LfFictArray=None,k=None,*args,**kwargs):

    zeroCross1=0

    # Remove outliers
    k_noOutliers, LfFictFit_noOutliers = removeOutliers(k, LfFictArray)
    
    # Smooth
    LfFictFit_noOutliers=smooth(LfFictFit_noOutliers,20) # frac = +-0.1
    # LfFictFit3=smooth(LfFictFit,150) # frac = +-0.8

    LfFictFit2=np.polyfit(k_noOutliers,LfFictFit_noOutliers,2)
    y_np = np.polyval(LfFictFit2, k)

    # Calculate zeros
    r=np.roots(LfFictFit2)
    for n in np.arange(0,len(r),1):
        if r[n] < 1 and r[n] > 0:
            zeroCross1=r[n]
    
    print("zerocross:", end = ' ')
    print(zeroCross1)

    # Not necessary I guess
    # n=2
    # while np.sign(LfFictFit3[n]) == np.sign(LfFictFit3[n - 1]) and n < len(k):
    #     n=n + 1
    # zeroCross2=k[n - 1] + np.dot(abs(LfFictFit3[n - 1]),((k[n] - k[n - 1]) / abs(LfFictFit3[n] - LfFictFit3[n - 1])))
    # zeroCross3=np.mean([zeroCross1,zeroCross2])

    # Plotting
    plt.scatter(k, LfFictArray, color="grey", alpha=0.5, label="Data")
    plt.scatter(k_noOutliers, LfFictFit_noOutliers, color="green", alpha=0.5, label="No outliers + smoothed")
    plt.plot(k, y_np, color="red", label="Fit np")
    plt.legend()
    plt.title("ZeroCross: " + str('{:.3f}'.format(zeroCross1)))
    plt.ylim(-0.03, 0.03)
    plt.savefig("result.png")
    # plt.show()
    
    return zeroCross1
