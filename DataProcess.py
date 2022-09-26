# THIS SCRIPT IS FOR GENERAL DATA PROCESSING

import numpy as np    
from scipy.fftpack import fft, ifft  , fftfreq  
import cmath
import matplotlib.pyplot as plt

if __name__ == '__main__':
    pass

# Updated version of function for real time implementation
def RealTimeFilterFundamental(Iabc=None,Vabc=None,t=None,sampleFreq=None,f=None,*args,**kwargs):

    Ts=1/sampleFreq
    # windowsize for 50Hz signal in #samples
    wd=(1/f)/Ts
    wd=int(wd) # cast to integer

    I_trans=np.zeros((3,len(t)))
    V_trans=np.zeros((3,len(t)))
    tn=t[wd-1:]

    Iabc = Iabc.transpose()
    Vabc = Vabc.transpose()

    for n in np.arange(0,len(tn)-1):

        # Current
        I_wd=Iabc[:,n:wd+n+1]
        y=fft(I_wd.transpose(), axis=0)
        # x = np.fft.fftfreq(len(I_wd[0]), 1 / 10000)
        ytrans=np.zeros((len(I_wd[0]),3))
        ytrans = ytrans.astype('complex64')

        ytrans[3:100,:]=y[3:100,:]
        ytrans[-1-99: -1-3+1,:]=y[-1-99:-1-3+1,:]
        Itr_wd=ifft(ytrans, axis=0).real
        I_trans[:,(n+round(wd/2))]=Itr_wd[round(wd/2)-1,:].transpose()

        # Voltage
        V_wd=Vabc[:,n:wd+n+1]
        y=fft(V_wd.transpose(), axis=0)
        ytrans=np.zeros((len(V_wd[0]),3))
        ytrans = ytrans.astype('complex64')

        ytrans[3:190,:]=y[3:190,:]
        ytrans[-1-189:-1-3+1,:]=y[-1-189:-1-3+1,:]
        Vtr_wd=ifft(ytrans, axis=0).real
        V_trans[:,(n+round(wd/2))]=Vtr_wd[round(wd/2)-1,:].transpose()
    
    I_trans=I_trans[:,wd-1:(len(I_trans[0])-100)]
    V_trans=V_trans[:,wd-1:(len(V_trans[0])-100)]
    tn=t[wd-1:(len(t)-100)]

    return I_trans,V_trans,tn


def FilterFundamental(f=None,Ts=None,Iabc=None,Vabc=None,t=None,*args,**kwargs):

    # windowsize for 50Hz signal in #samples
    wd=(1/f)/Ts
    wd=int(wd) # cast to integer

    I_trans=np.zeros((3,len(t)))
    V_trans=np.zeros((3,len(t)))
    tn=t[wd-1:]

    for n in np.arange(0,len(tn)-1):

        # Current
        I_wd=Iabc[:,n:wd+n+1]
        y=fft(I_wd, axis=0)
        x = fftfreq(len(I_wd[0]), 1 / 10000)
        ytrans=np.zeros((len(I_wd[0]),3))
        ytrans = ytrans.astype('complex64')

        ytrans[3:100,:]=y[3:100,:]
        ytrans[-1-99: -1-3+1,:]=y[-1-99:-1-3+1,:]
        Itr_wd=ifft(ytrans, axis=0).real
        I_trans[:,(n+round(wd/2))]=Itr_wd[round(wd/2)-1,:].transpose()

        # Voltage
        V_wd=Vabc[:,n:wd+n+1]
        y=fft(V_wd.transpose(), axis=0)
        ytrans=np.zeros((len(V_wd[0]),3))
        ytrans = ytrans.astype('complex64')

        ytrans[3:190,:]=y[3:190,:]
        ytrans[-1-189:-1-3+1,:]=y[-1-189:-1-3+1,:]
        Vtr_wd=ifft(ytrans, axis=0).real
        V_trans[:,(n+round(wd/2))]=Vtr_wd[round(wd/2)-1,:].transpose()
    
    I_trans=I_trans[:,wd-1:]
    V_trans=V_trans[:,wd-1:]
    tn=t[wd-1:]

    return I_trans,V_trans,tn


def findStartCropInceptionTime(tn, V_trans, I_trans, estFaultIncepTime):

    # Plot before (debugging)
    # plt.plot(tabc, Vabc[:,0])
    # plt.plot(tn, V_trans[0])
    # plt.show()

    start = np.argwhere(tn>=estFaultIncepTime)[0][0]
    tn = tn[start:]
    V_trans = V_trans[:,start:]
    I_trans = I_trans[:,start:]

    # Plot after (debugging)
    # plt.plot(tabc, Vabc[:,0])
    # plt.plot(tn, V_trans[0])
    # plt.show()

    return tn, V_trans, I_trans
