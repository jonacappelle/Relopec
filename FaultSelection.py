import numpy as np
import copy
import matplotlib.pyplot as plt
from numba import njit, objmode
from numba.pycc import CC


if __name__ == '__main__':
    pass

# cc = CC('my_module')
# cc.verbose = True
# cc.compile()

def calculate_fft(a):
    return np.fft.fft(a, axis=0)

# This function is precompiled
# Updated version of function for real time implementation
@njit
# @cc.export('RealTimeFaultIndentification', 'Tuple((u4,f4,f4,f8))(f4[:,:],f4[:,:],f4,f8,f4,i4,i4)')
def RealTimeFaultIndentification(Iabc=None,Vabc=None,t=None,minPreviousZ=None,Zbase=None,sampleFreq=None,gridFreq=None):

    Ts = 1/sampleFreq
    wd=(round((1 / gridFreq) / Ts))

    Z=np.zeros(6) # Changed from 3 to 6

    indexFaultIncep=0
    indexFaultStable=0
    estFaultStableTime=np.float32(0)
    indexExecute=0
    estFaultType=0
    estFaultIncepTime=np.float32(0)

    # Maybe this can be optimized
    with objmode(Ifft='complex128[:,:]'):
        Ifft=calculate_fft(Iabc)
    # x = fftfreq(len(Iabc[:,0]), 1 / 10000)
    with objmode(Vfft='complex128[:,:]'):
        Vfft=calculate_fft(Vabc)

    I=2.0*Ifft[1]/wd
    V=2.0*Vfft[1]/wd

    Zab=abs( (V[0] - V[1]) / (I[0] - I[1]) )
    Zbc=abs( (V[1] - V[2]) / (I[1] - I[2]) )
    Zca=abs( (V[2] - V[0]) / (I[2] - I[0]) )
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
    if minPreviousZ < (1.5*min(Z)) and indexFaultStable < 1 and min(Z) < (0.5*Zbase):
        estFaultStableTime=t
        indexFaultStable=indexFaultStable + 1
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

    
    return estFaultType,estFaultIncepTime,estFaultStableTime, min(Z)
