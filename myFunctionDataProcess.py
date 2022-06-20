# Generated with SMOP  0.41-beta
# from libsmop import *
# myFunctionDataProcess.m

    # THIS SCRIPT IS FOR GENERAL DATA PROCESSING
#classdef myFunctionDataProcess
    
    #methods(Static)
    
    # DOWNSAMPLING OF THE DATASET IF NECESSARY. IN THIS CASE, DOWNSAMPLING IS 
        # PERFORMED IF THE SAMPLE FREQUENCY OF THE DATA IS HIGHER THAN THE
        # FREQUENCY AT WHICH THE ALGORITHM WORKS.

import numpy as np    
from scipy.fft import fft, ifft    
import cmath


def zeros(a, b):
    return np.zeros((a, b))

def length(x):
    return len(x)

def transpose(x):
    return x.transpose()

def DownSample(Ts=None,TsSim=None,fs=None,IabcOrig=None,VabcOrig=None,tOrig=None,*args,**kwargs):
    varargin = DownSample.varargin
    nargin = DownSample.nargin

    if Ts > TsSim:
        downSampleRate=round(Ts / TsSim)
# myFunctionDataProcess.m:11
        IabcOrig=lowpass(IabcOrig,dot(0.4,fs),(1 / TsSim))
# myFunctionDataProcess.m:14
        VabcOrig=lowpass(VabcOrig,dot(0.4,fs),(1 / TsSim))
# myFunctionDataProcess.m:15
        IabcOrigDownSamp=downsample(IabcOrig,downSampleRate)
# myFunctionDataProcess.m:18
        VabcOrigDownSamp=downsample(VabcOrig,downSampleRate)
# myFunctionDataProcess.m:19
        tOrigDownSamp=downsample(tOrig,downSampleRate)
# myFunctionDataProcess.m:20
        Iabc=transpose(IabcOrigDownSamp)
# myFunctionDataProcess.m:23
        Vabc=transpose(VabcOrigDownSamp)
# myFunctionDataProcess.m:24
        t=transpose(tOrigDownSamp)
# myFunctionDataProcess.m:25
    else:
        Iabc=transpose(IabcOrig)
# myFunctionDataProcess.m:28
        Vabc=transpose(VabcOrig)
# myFunctionDataProcess.m:29
        t=transpose(tOrig)
# myFunctionDataProcess.m:30
    
    
    return Iabc,Vabc,t
    
if __name__ == '__main__':
    pass
    
    
    # FUNCTION TO FILTER OUT THE FUNDAMENTAL. OTHER FILTER OPTIONS
        # MIGHT BE BETTER...
    

def FilterFundamental(f=None,Ts=None,Iabc=None,Vabc=None,t=None,*args,**kwargs):

    # windowsize for 50Hz signal in #samples
    wd=(1/f)/Ts
    wd=int(wd) # cast to integer

    I_trans=zeros(3,length(t))
    V_trans=zeros(3,length(t))
    tn=t[wd-1:]

    for n in np.arange(0,length(tn)-1,1):

        # Current
        I_wd=Iabc[:,n:wd+n+1]
        y=fft(transpose(I_wd), axis=0)
        ytrans=zeros(length(I_wd[0]),3)
        ytrans = ytrans.astype('complex64')

        ytrans[3:100,:]=y[3:100,:]
        ytrans[-1-99: -1-2,:]=y[-1-99:-1-2,:]
        Itr_wd=ifft(ytrans, axis=0).real
        I_trans[:,(n+round(wd/2))]=transpose(Itr_wd[round(wd/2)-1,:])

        # Voltage
        V_wd=Vabc[:,n:wd+n+1]
        y=fft(transpose(V_wd), axis=0)
        ytrans=zeros(length(V_wd[0]),3)
        ytrans = ytrans.astype('complex64')

        ytrans[3:190,:]=y[3:190,:]
        ytrans[-1-189:-1-2,:]=y[-1-189:-1-2,:]
        Vtr_wd=ifft(ytrans, axis=0).real
        V_trans[:,(n+round(wd/2))]=transpose(Vtr_wd[round(wd/2)-1,:])
    
    I_trans=I_trans[:,wd-1:]
    V_trans=V_trans[:,wd-1:]
    tn=t[wd-1:]

    return I_trans,V_trans,tn
    
if __name__ == '__main__':
    pass
    
    
    

def plotTransSignals(tn=None,I_trans=None,V_trans=None,*args,**kwargs):
    varargin = plotTransSignals.varargin
    nargin = plotTransSignals.nargin

    figure(3)
    subplot(2,1,1)
    plot(tn,V_trans,'color','black')
    xlabel('time [s]')
    ylabel('Voltage [V]')
    
    title('3-ph voltages: non-fundamental frequencies')
    grid('on')
    set(gca,'Units','centimeters','Position',concat([1.5,8,8.5,2.5]))
    subplot(2,1,2)
    plot(tn,I_trans,'color','black')
    xlabel('time [s]')
    ylabel('current [A]')
    
    title('3-ph currents: non-fundamental frequencies')
    grid('on')
    set(gca,'Units','centimeters','Position',concat([1.5,2.5,8.5,2.5]))
    set(gcf,'Units','centimeters','Position',concat([0,0,11,12]))
    
    
    
    #end