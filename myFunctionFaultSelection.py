import numpy as np
from scipy.fft import fft, ifft
import copy
import matplotlib.pyplot as plt
# from numba import jit, objmode

if __name__ == '__main__':
    pass

# @jit(nopython=False)
def fft(a):
    return np.fft.fft(a, axis=0)


temp = 0

# @jit(nopython=True)
def RealTimeFaultIndentification(Iabc=None,Vabc=None,t=None,minPreviousZ=None,*args,**kwargs):
    
    f=50
    sampleFreq=4000 #4khz
    Ts = 1/sampleFreq

    Zbase = 45

    wd=200#round((1 / f) / Ts)
    I=np.zeros(3)
    V=np.zeros(3)

    # IabcForm=Iabc.transpose()
    # VabcForm=Vabc.transpose()
    Z=np.zeros(6) # Changed from 3 to 6
    # V=Vabc.transpose()
    indexFaultIncep=0
    indexFaultStable=0
    estFaultStableTime=0
    indexExecute=0
    estFaultType=0
    estFaultIncepTime=0

    # The for loop simulates the real-time behaviour of the data
    # In practice: these values need to be executed only once at 2 kHz

    # Window of 200 samples: wd=200
    wdI=Iabc
    wdV=Vabc

    # Maybe this can be optimized
    # with objmode(Ifft='complex128[:]'):
    Ifft=fft(wdI)
    # with objmode(Vfft='complex128[:]'):
    Vfft=fft(wdV)

    I = I.astype('complex64')
    V = V.astype('complex64')

    I=(2.0*Ifft[1,:]/wd)
    V=(2.0*Vfft[1,:]/wd)

    Zab=abs((V[0] - V[1]) / (I[0] - I[1]))
    Zbc=abs((V[1] - V[2]) / (I[1] - I[2]))
    Zca=abs((V[2] - V[0]) / (I[2] - I[0]))
    Za=abs(V[0] / I[0])
    Zb=abs(V[1] / I[1])
    Zc=abs(V[2] / I[2])

    Z[0]=Zab
    Z[1]=Zbc
    Z[2]=Zca
    Z[3]=Za
    Z[4]=Zb
    Z[5]=Zc


    if min(Z) < (0.5*Zbase) and indexFaultIncep < 1:
        estFaultIncepTime=t
        indexFaultIncep=indexFaultIncep + 1
    # if min(Z[k - wd,:]) < (1.5*min(Z)) and indexFaultStable < 1 and min(Z) < (0.5*Zbase):
    if minPreviousZ < (1.5*min(Z)) and indexFaultStable < 1 and min(Z) < (0.5*Zbase):
        estFaultStableTime=t
        indexFaultStable=indexFaultStable + 1
        # indexExecute=copy.copy(k)
        if Zab < (0.5*Zbase) and Zbc < (0.5*Zbase) and Zca < (0.5*Zbase):
            estFaultType=1
        else:
            if Zab < (0.5*Zbase) and Zbc > (0.5*Zbase) and Zca > (0.5*Zbase):
                estFaultType=2
            else:
                if Zab > (0.5*Zbase) and Zbc < (0.5*Zbase) and Zca < (0.5*Zbase):
                    estFaultType=3
                else:
                    if Zab > (0.5*Zbase) and Zbc > (0.5*Zbase) and Zca< (0.5*Zbase):
                        estFaultType=4

        print("estFaultType:", end = ' ')
        print(estFaultType)
        print("estFaultIncepTime:", end = ' ')
        print(estFaultIncepTime)
        print("estFaultStableTime:", end = ' ')
        print(estFaultStableTime)
    
    # global temp
    # temp = temp + 1

    # if temp > 100:
    #     plt.scatter(t, min(Z))
    #     plt.scatter(t, minPreviousZ)
    #     plt.pause(0.00001)

    #     temp = 0
    
    return estFaultType,estFaultIncepTime,estFaultStableTime, min(Z)

# @jit(nopython=True)
def testDataset(Iabc=None,Vabc=None,t=None,f=None,Ts=None,Zbase=None,*args,**kwargs):
    
    wd=round((1 / f) / Ts)
    I=np.zeros((len(t),3))
    V=np.zeros((len(t),3))

    IabcForm=Iabc.transpose()
    VabcForm=Vabc.transpose()
    Z=np.zeros((len(t),6)) # Changed from 3 to 6
    V=Vabc.transpose()
    indexFaultIncep=0
    indexFaultStable=0
    estFaultStableTime=0
    indexExecute=0
    estFaultType=0

    # The for loop simulates the real-time behaviour of the data
    # In practice: these values need to be executed only once at 2 kHz
    for k in np.arange(6645,len(t)):
        wdI=IabcForm[k-wd:k,:]
        wdV=VabcForm[k-wd:k,:]

        time = 6645

        return wdI, wdV, Z, t



# @jit(nopython=True)
def FaultIndentification(Iabc=None,Vabc=None,t=None,f=None,Ts=None,Zbase=None,*args,**kwargs):
    
    wd=round((1 / f) / Ts)
    I=np.zeros((len(t),3))
    V=np.zeros((len(t),3))

    IabcForm=Iabc.transpose()
    VabcForm=Vabc.transpose()
    Z=np.zeros((len(t),6)) # Changed from 3 to 6
    V=Vabc.transpose()
    indexFaultIncep=0
    indexFaultStable=0
    estFaultStableTime=0
    indexExecute=0
    estFaultType=0

    # The for loop simulates the real-time behaviour of the data
    # In practice: these values need to be executed only once at 2 kHz
    for k in np.arange(wd+1,len(t)):
        wdI=IabcForm[k-wd:k,:]
        wdV=VabcForm[k-wd:k,:]

        # Maybe this can be optimized
        # with objmode(Ifft='complex128[:]'):
        Ifft=fft(wdI)
        # with objmode(Vfft='complex128[:]'):
        Vfft=fft(wdV)

        I = I.astype('complex64')
        V = V.astype('complex64')

        I[k,:]=(2.0*Ifft[1,:]/wd)
        V[k,:]=(2.0*Vfft[1,:]/wd)

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

        # if k > 6600:
        #     plt.scatter(t[k], min(Z[k,:]))
        #     plt.pause(0.00001)

        if min(Z[k - wd,:]) != 0:
            print(" ")

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
                        if Zab > (0.5*Zbase) and Zbc > (0.5*Zbase) and Zca< (0.5*Zbase):
                            estFaultType=4
            # plt.scatter(t[k], 200)
            # plt.pause(0.00001)

    # Not necessary I guess    
    # Zab=abs((V[:,0] - V[:,1]) / (I[:,0] - I[:,1]))
    # Zbc=abs((V[:,1] - V[:,2]) / (I[:,1] - I[:,2]))
    # Zca=abs((V[:,2] - V[:,0]) / (I[:,2] - I[:,0]))
    # Za=abs(V[:,0] / I[:,0])
    # Zb=abs(V[:,1] / I[:,1])
    # Zc=abs(V[:,2] / I[:,2])

    print("estFaultType:", end = ' ')
    print(estFaultType)
    print("estFaultIncepTime:", end = ' ')
    print(estFaultIncepTime)
    print("estFaultStableTime:", end = ' ')
    print(estFaultStableTime)
    
    return estFaultType,estFaultIncepTime,estFaultStableTime
