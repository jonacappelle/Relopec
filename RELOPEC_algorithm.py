# Generated with SMOP  0.41-beta
# from libsmop import *
# from smop.libsmop import *
import scipy.io

import findData
from precision import Precision
import myFunctionDataProcess
import precision
import pandas as pd
from BasicParameters import *
import myFunctionFaultSelection
import numpy as np
import myFunctionCalcNetwork
import myFunctionCalcFaultLocation

# THIS IS THE MAIN SCRIPT OF THE ALGORITHM


# The data should have the following format: rows are phases, colums are timestamps
# mat = scipy.io.loadmat('data.mat')
# ParameterValues = mat["ParameterValues"]

# print(mat.keys())
# print(ParameterValues)
# # print(mat)


# # find list of data points
# index=findData.findFaultDataIndex(ParameterValues)

# j=4
# row=index(j)
# VabcOrig,IabcOrig,tOrig,faultLocData=findData.selectData(row,ParameterValues,CurveSignalValues,nargout=4)

# ## PARAMETERS AND WAVEFORMS
    
# # BasicParameters

# Iabc,Vabc,t=myFunctionDataProcess.DownSample(Ts,TsSim,fs,IabcOrig,VabcOrig,tOrig,nargout=3)


# Load Simulation Data

data = scipy.io.loadmat('data.mat')
print(data.keys())

Iabc = data['Iabc']
Vabc = data['Vabc']
t = data['t']


## FAULT IDENTIFICATION AND CLASSIFICATION
    # THIS FUNCTION DETERMINES THE FAULT TYPE AND WHEN THE FAULT INITIATES.
    # THIS FUNTION IS FOR ONLINE PURPOSES!
estFaultType,estFaultIncepTime,estFaultStableTime=myFunctionFaultSelection.FaultIndentification(Iabc,Vabc,t,f,Ts,Zbase,nargout=3)
print("estFaultType")
print(estFaultType)
print("estFaultIncepTime")
print(estFaultIncepTime)
print("estFaultStableTime")
print(estFaultStableTime)

## FILTER OUT THE FUNDAMENTAL FREQUENCY
I_trans,V_trans,tn=myFunctionDataProcess.FilterFundamental(f,Ts,Iabc,Vabc,t,nargout=3)
    
## CALCULATING FICTITIOUS FAULT INDUCTANCE
    
# Making arrays for k and fictitious fault impedance
k=np.arange(0.01,0.99,0.005)

LfFictArray=np.zeros(len(k),1)
RfFictArray=np.zeros(len(k),1)

# Run calculation for every point in k (every point on the line)
    # 1=ABC, 2=AB, 3=BC, 4=CA, 5=Ag, 6=Bg, 7=Cg, 8=ABg, 9=BCg, 10=CAg
    # estFaultType = 2;  #in case you want to overrule the faultSelection function
    
for n in np.arange(1,len(k),1).reshape(-1):
    vF,i2,X=myFunctionCalcNetwork.NetworkParamNoCap(I_trans,V_trans,k(n),L_line,R_line,C_line,Ts,tn,Lg,Rg,nargout=3)

    LfFict,RfFict,ZfFict=myFunctionCalcFaultLocation.Fault(vF,i2,X,Ts,tn,estFaultType,estFaultStableTime,nargout=3)

    LfFictArray[n]=LfFict

## Find zero crossing and hence the distance to the fault
zeroCross1=myFunctionCalcFaultLocation.findZeroCross(LfFictArray,k)

## Results
zeroCross1
faultLocData / 10