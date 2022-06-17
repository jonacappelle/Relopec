# Generated with SMOP  0.41-beta
# from libsmop import *
# myFunctionFaultSelection.m

    #classdef myFunctionFaultSelection
    #methods(Static)
import numpy as np
from scipy.fft import fft, ifft
import copy
import matplotlib.pyplot as plt

def length(x):
    return len(x)

def zeros(a, b):
    return np.zeros((a, b))

def transpose(x):
    return x.transpose()

def dot(a, b):
    return np.sum(a.conj()*b, axis=0)
    
def FaultIndentification(Iabc=None,Vabc=None,t=None,f=None,Ts=None,Zbase=None,*args,**kwargs):

    # this function should be a real-time function, so simulated in
            # a for loop
    
    wd=round((1 / f) / Ts)
    I=zeros(length(t),3)
    V=zeros(length(t),3)
    IabcForm=transpose(Iabc)
    VabcForm=transpose(Vabc)
    Z=zeros(length(t),6) # Changed from 3 to 6
    V=transpose(Vabc)
    indexFaultIncep=0
    indexFaultStable=0
    estFaultStableTime=0
    indexExecute=0
    estFaultType=0

    for k in np.arange(wd,length(t),1):
        wdI=IabcForm[k-wd+1:k+1,:]
        wdV=VabcForm[k-wd+1:k+1,:]
        Ifft=fft(wdI)
        temp=np.absolute(Ifft)

        plt.plot(temp)
        plt.show()

        Vfft=fft(wdV)
        I[k,:]=2*Ifft[1,:]/wd
        V[k,:]=2*Vfft[1,:]/wd

        Zab=abs((V[k,0] - V[k,1]) / (I[k,0] - I[k,1]))
        Zbc=abs((V[k,1] - V[k,2]) / (I[k,1] - I[k,2]))
        Zca=abs((V[k,2] - V[k,0]) / (I[k,2] - I[k,0]))
        Za=abs(V[k,0] / I[k,0])
        Zb=abs(V[k,1] / I[k,1])
        Zc=abs(V[k,2] / I[k,2])

        Z[k,0]=Zab
        Z[k,1]=Zbc
        Z[k,2]=Zca
        Z[k,3]=Za
        Z[k,4]=Zb
        Z[k,5]=Zc

        if min(Z[k,:]) < (0.5*Zbase) and indexFaultIncep < 1:
            estFaultIncepTime=t[k]
            indexFaultIncep=indexFaultIncep + 1
        if min(Z[k - wd,:]) < (1.5*min(Z[k,:])) and indexFaultStable < 1 and min(Z[k,]) < (0.5*Zbase):
            estFaultStableTime=t[k]
            indexFaultStable=indexFaultStable + 1
            indexExecute=copy.copy(k)
            if Zab < (0.5*Zbase) and Zbc < (0.5*Zbase) and Zca < (0.5*Zbase):
                estFaultType=1
            else:
                if Zab < (0.5*Zbase) and Zbc > (0.5*Zbase) and Zca > (0.5*Zbase):
                    estFaultType=2
                else:
                    if Zab > (0.5*Zbase) and Zbc < (0.5*Zbase) and Zca < (0.5*Zbase):
                        estFaultType=3
                    else:
                        if Zab > (0.5*Zbase) and Zbc(k,2) > (0.5*Zbase) and Zca(k,3) < (0.5*Zbase):
                            estFaultType=4
    
    
    Zab=abs((V[:,0] - V[:,1]) / (I[:,0] - I[:,1]))
    Zbc=abs((V[:,1] - V[:,2]) / (I[:,1] - I[:,2]))
    Zca=abs((V[:,2] - V[:,0]) / (I[:,2] - I[:,0]))
    Za=abs(V[:,0] / I[:,0])
    Zb=abs(V[:,1] / I[:,1])
    Zc=abs(V[:,2] / I[:,2])
    
    #estFaultIncepTime=0;
    
    # figure(6)
    # plot(t,Zab)
    # hold('on')
    # plot(t,Zbc)
    # plot(t,Zca)
    
    # figure(7)
    # plot(t,Za)
    # hold('on')
    # plot(t,Zb)
    # plot(t,Zc)
    return estFaultType,estFaultIncepTime,estFaultStableTime
    
if __name__ == '__main__':
    pass
    
    #end
#end