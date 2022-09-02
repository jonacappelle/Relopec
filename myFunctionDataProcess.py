# THIS SCRIPT IS FOR GENERAL DATA PROCESSING

import numpy as np    
from scipy.fft import fft, ifft    
import cmath

if __name__ == '__main__':
    pass

def RealTimeFilterFundamental(f=None,Ts=None,Iabc=None,Vabc=None,t=None,*args,**kwargs):

    # windowsize for 50Hz signal in #samples
    wd=(1/f)/Ts
    wd=int(wd) # cast to integer

    I_trans=np.zeros((3,len(t)))
    V_trans=np.zeros((3,len(t)))
    tn=t[wd-1:]

    for n in np.arange(0,len(tn)-1):

        # Current
        I_wd=Iabc[:,n:wd+n+1]
        y=fft(I_wd.transpose(), axis=0)
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
        y=fft(I_wd.transpose(), axis=0)
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
