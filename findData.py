# Generated with SMOP  0.41-beta
# from libsmop import *
# findData.m

import numpy as np
from precision import Precision

    #This script is to find the right data set from the simulation. This will
#be different in a real-time implementation.
#classdef findData
    
    #methods(Static)
    
    #DATA COLUMNS:
    
    # 1 = location of the fault
        # 11 = type of fault (1=ag, 2=ab, 3=abg, 4=abc, 5=abcg)
        # 12 = inception time (1=0.6, 2=0.604, 3=0.608)
        # 17 = faultresistance (either 0 or 15)
    
    

def findFaultDataIndex(ParameterValues=None,*args,**kwargs):

    index=0
    for n in np.arange(1,len(ParameterValues),1).reshape(-1):
        if np.matrix(ParameterValues(n,11)) == 2 and np.matrix(ParameterValues(n,12)) == 1 and np.matrix(ParameterValues(n,17)) == 0:
            # index=cat(1,index,n)
            index=np.block(index, n)
    
    return index
    
if __name__ == '__main__':
    pass
    
    
    

def findMultipleFaultDataIndex(ParameterValues=None,*args,**kwargs):
    varargin = findMultipleFaultDataIndex.varargin
    nargin = findMultipleFaultDataIndex.nargin

    index=0
# findData.m:24
    FaultInceptionTimeArray=0
# findData.m:25
    for n in arange(1,length(ParameterValues),1).reshape(-1):
        if cell2mat(ParameterValues(n,11)) == 1 and cell2mat(ParameterValues(n,17)) == 0:
            index=cat(1,index,n)
# findData.m:28
            if ParameterValues(n,12) == 1:
                FaultInceptionTimeArray=cat(1,FaultInceptionTimeArray,0.6)
# findData.m:30
            else:
                if ParameterValues(n,12) == 2:
                    FaultInceptionTimeArray=cat(1,FaultInceptionTimeArray,0.604)
# findData.m:32
                else:
                    if ParameterValues(n,12) == 3:
                        FaultInceptionTimeArray=cat(1,FaultInceptionTimeArray,0.608)
# findData.m:34
    
    return index
    
if __name__ == '__main__':
    pass
    
    
    

def selectData(row=None,ParameterValues=None,CurveSignalValues=None,*args,**kwargs):
    varargin = selectData.varargin
    nargin = selectData.nargin

    faultLocData=cell2mat(ParameterValues(row,1))
# findData.m:41
    Vat=cell2mat(CurveSignalValues(row,1))
# findData.m:43
    Vbt=cell2mat(CurveSignalValues(row,2))
# findData.m:44
    Vct=cell2mat(CurveSignalValues(row,3))
# findData.m:45
    Iat=cell2mat(CurveSignalValues(row,4))
# findData.m:47
    Ibt=cell2mat(CurveSignalValues(row,5))
# findData.m:48
    Ict=cell2mat(CurveSignalValues(row,6))
# findData.m:49
    tOrig=transpose(Vat(arange(),1))
# findData.m:51
    VabcOrig=cat(2,Vat(arange(),2),Vbt(arange(),2),Vct(arange(),2))
# findData.m:52
    IabcOrig=cat(2,Iat(arange(),2),Ibt(arange(),2),Ict(arange(),2))
# findData.m:53
    Vat_grid=cell2mat(CurveSignalValues(row,34))
# findData.m:55
    Vbt_grid=cell2mat(CurveSignalValues(row,35))
# findData.m:56
    Vct_grid=cell2mat(CurveSignalValues(row,36))
# findData.m:57
    VabcOrig_grid=cat(2,Vat_grid(arange(),2),Vbt_grid(arange(),2),Vct_grid(arange(),2))
# findData.m:59
    figure(20)
    plot(tOrig,VabcOrig)
    return VabcOrig,IabcOrig,tOrig,faultLocData
    
if __name__ == '__main__':
    pass
    
    #end
#end