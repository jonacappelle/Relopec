# Generated with SMOP  0.41-beta
# from libsmop import *
# myFunctionCalcFaultLocation.m

    #classdef myFunctionCalcFaultLocation
    
    #methods(Static)

import numpy as np
import copy

import numpy as np
import itertools
from numpy.linalg import multi_dot
from numpy.linalg import inv

import matplotlib.pyplot as plt

import math

def Fault(vF=None,i2=None,X=None,Ts=None,tn=None,FaultType=None,estFaultStableTime=None,*args,**kwargs):
    
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
        #vF = vFa;
                    #iF = (iaBf-iaAf);
        vF=copy.copy(vFb)
        iF=(ibBf - ibAf)
        #iF = (icBf-icAf);
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
    
    
    ZfFict=np.zeros((2,len(tn)))
    
    for n in np.arange(1,len(tn) - 1,1):
        A_matrix=[[iF[n] - iF[n - 1],np.dot((iF[n - 1] + iF[n]),Ts) / 2], [iF[n + 1] - iF[n],np.dot((iF[n + 1] + iF[n]),Ts) / 2]]
        B_matrix=[[np.dot((vF[n - 1] + vF[n]),(Ts/2))], [np.dot((vF[n] + vF[n + 1]),(Ts/2))]]
        ZfFict[:,[n]]= np.dot(np.linalg.pinv(A_matrix),B_matrix) # Compute pseudo inverse of matrix if it can't be inversed
        # TODO klopt nog niet helemaal - +- oke
    
    #find the overal inducance and resistance by taking the average
            #over one period (0.02 seconds for 50 hertz)
            #this step requires us to know the time of fault inception
    
    index1=np.argwhere(tn >= estFaultStableTime - 0.02)
    index2=np.argwhere(tn >= estFaultStableTime)

    LfFict=np.mean(ZfFict[0,index1[0][0]:index2[0][0]])
    
    RfFict=np.mean(ZfFict[1,index1[0][0]:index2[0][0]])
    return LfFict,RfFict,ZfFict
    
if __name__ == '__main__':
    pass
    
    
def LLLFault(vF=None,i2=None,X=None,Ts=None,tn=None,faultIncepTime=None,FaultType=None,*args,**kwargs):
    varargin = LLLFault.varargin
    nargin = LLLFault.nargin

    
    # voltage at the (assumed) fault location
    vFa=vF(1,arange())
# myFunctionCalcFaultLocation.m:65
    vFb=vF(2,arange())
# myFunctionCalcFaultLocation.m:66
    vFc=vF(3,arange())
# myFunctionCalcFaultLocation.m:67
    
    iaBf=i2(1,arange())
# myFunctionCalcFaultLocation.m:70
    ibBf=i2(2,arange())
# myFunctionCalcFaultLocation.m:71
    icBf=i2(3,arange())
# myFunctionCalcFaultLocation.m:72
    
    iaAf=X(1,arange())
# myFunctionCalcFaultLocation.m:75
    ibAf=X(2,arange())
# myFunctionCalcFaultLocation.m:76
    icAf=X(3,arange())
# myFunctionCalcFaultLocation.m:77
    vF=copy(vFa)
# myFunctionCalcFaultLocation.m:79
    iF=(iaBf - iaAf)
# myFunctionCalcFaultLocation.m:80
    ZfFict_a=zeros(2,length(tn))
# myFunctionCalcFaultLocation.m:81
    
    for n in arange(2,length(tn) - 1,1).reshape(-1):
        A_matrix=concat([[iF(n) - iF(n - 1),dot((iF(n - 1) + iF(n)),Ts) / 2],[iF(n + 1) - iF(n),dot((iF(n + 1) + iF(n)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:83
        B_matrix=concat([[dot((vF(n - 1) + vF(n)),Ts) / 2],[dot((vF(n) + vF(n + 1)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:84
        ZfFict_a[arange(),n]=dot(inv(A_matrix),B_matrix)
# myFunctionCalcFaultLocation.m:85
    
    
    vF=copy(vFb)
# myFunctionCalcFaultLocation.m:88
    iF=(ibBf - ibAf)
# myFunctionCalcFaultLocation.m:89
    ZfFict_b=zeros(2,length(tn))
# myFunctionCalcFaultLocation.m:90
    
    for n in arange(2,length(tn) - 1,1).reshape(-1):
        A_matrix=concat([[iF(n) - iF(n - 1),dot((iF(n - 1) + iF(n)),Ts) / 2],[iF(n + 1) - iF(n),dot((iF(n + 1) + iF(n)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:92
        B_matrix=concat([[dot((vF(n - 1) + vF(n)),Ts) / 2],[dot((vF(n) + vF(n + 1)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:93
        ZfFict_b[arange(),n]=dot(inv(A_matrix),B_matrix)
# myFunctionCalcFaultLocation.m:94
    
    
    vF=copy(vFc)
# myFunctionCalcFaultLocation.m:97
    iF=(icBf - icAf)
# myFunctionCalcFaultLocation.m:98
    ZfFict_c=zeros(2,length(tn))
# myFunctionCalcFaultLocation.m:99
    
    for n in arange(2,length(tn) - 1,1).reshape(-1):
        A_matrix=concat([[iF(n) - iF(n - 1),dot((iF(n - 1) + iF(n)),Ts) / 2],[iF(n + 1) - iF(n),dot((iF(n + 1) + iF(n)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:101
        B_matrix=concat([[dot((vF(n - 1) + vF(n)),Ts) / 2],[dot((vF(n) + vF(n + 1)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:102
        ZfFict_c[arange(),n]=dot(inv(A_matrix),B_matrix)
# myFunctionCalcFaultLocation.m:103
    
    
    
    
    index1=find(tn >= (faultIncepTime + 0.02 + dot(0,Ts)),1,'first')
# myFunctionCalcFaultLocation.m:108
    
    index2=find(tn >= (faultIncepTime + 0.02 + dot(200,Ts)),1,'first')
# myFunctionCalcFaultLocation.m:109
    
    #Lf_Fict_raw = (1/3)*(ZfFict_a(1,:)+ZfFict_b(1,:)+ZfFict_c(1,:));
            #LfFict = mean(Lf_Fict_raw(index1:index2));
    
    
    LfFict=median(concat([mean(ZfFict_a(1,arange(index1,index2))),mean(ZfFict_b(1,arange(index1,index2))),mean(ZfFict_c(1,arange(index1,index2)))]))
# myFunctionCalcFaultLocation.m:114
    
    #this step requires us to know the time of fault inception!
    
    
    #RfFict = mean(ZfFict(2,index1:index2));
    
    
    return LfFict
    
if __name__ == '__main__':
    pass
    
    
    #THIS FUNCTION IS TO FIND THE ZERO CROSSING AND HENCE THE FAULT
        #OPTIMISATION OF THIS METHOD MIGHT YIELD BETTER RESULTS
        #I ALREADY TRIED DIFFERENT APPROACHES BUT SECOND ORDER FIT SEEMS
        #BEST 
#         function [zeroCross1] = findZeroCross(LfFictArray, k)
#             zeroCross1 = 0;
#             LfFictFit = smooth(transpose(k),LfFictArray,0.1,'rloess');
#             LfFictFit2 = polyfit(transpose(k),LfFictFit,2);
#             LfFictFit2Plot = fit(transpose(k),LfFictFit,'poly2');
#             r = roots(LfFictFit2);
#             for n = 1:1:length(r)
#                 if r(n)<1 && r(n)>0
#                     zeroCross1 = r(n);
#                 end
#             end
#             figure(5)
#             plot(k, LfFictArray,'o','color','black');
#             hold on
#             plot(LfFictFit2Plot)
#             hold off
# 
#         end
    

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def plot_function(x, a):
    return a[2]*x**2 + a[1]*x + a[0]
    
def findZeroCross(LfFictArray=None,k=None,*args,**kwargs):

    zeroCross1=0
    zeroCross2=0
    zeroCross3=0
    zeroCross4=0
    LfFictFit=smooth(LfFictArray[:,0],5)
    LfFictFit3=smooth(LfFictFit,5)
    LfFictFit2=np.polyfit(np.transpose(k),LfFictFit,2)

    # Fitten maar
    LfFictFit2Plot=np.polyfit(np.transpose(k),LfFictFit,2)
    # k  is x range
    # maak y range

    ylist = plot_function(k, LfFictFit2Plot)

    r=np.roots(LfFictFit2)
    for n in np.arange(0,len(r)-1,1):
        if r[n] < 1 and r[n] > 0:
            zeroCross1=r[n]
    
    n=2
    while np.sign(LfFictFit3[n]) == np.sign(LfFictFit3[n - 1]) and n < len(k):

        n=n + 1

    
    zeroCross2=k[n - 1] + np.dot(abs(LfFictFit3[n - 1]),((k[n] - k[n - 1]) / abs(LfFictFit3[n] - LfFictFit3[n - 1])))
    zeroCross3=np.mean([zeroCross1,zeroCross2])
    # figure(5)
    # plot(k,LfFictArray,'o','color','black')
    # hold('on')
    # #     plot(k,LfFictFit)
    #     #     hold on
    # plot(LfFictFit2Plot)
    # #     hold on
    #     #     plot(k, LfFictFit3)
    # hold('off')

    plt.scatter(k, LfFictArray)
    plt.plot(k, ylist)
    plt.show()


    return zeroCross1
    
if __name__ == '__main__':
    pass
    
    
    #end
    
    #end