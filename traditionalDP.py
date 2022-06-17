# Generated with SMOP  0.41-beta
# from libsmop import *
# traditionalDP.m

    ## READ IN THE VOLTAGE AND CURRENT WAVEFORMS
# The data should have the following format: rows are phases, colums are timestamps
    
    load('waveform_data\SimData_OHL.mat')
    #findData
    
    # find list of data points
    index=findData.findFaultDataIndex(ParameterValues)
# traditionalDP.m:8
    ErrorArray=zeros(length(index),3)
# traditionalDP.m:9
    for j in 2.reshape(-1):
        row=index(j)
# traditionalDP.m:12
        VabcOrig,IabcOrig,tOrig,faultLocData=findData.selectData(row,ParameterValues,CurveSignalValues,nargout=4)
# traditionalDP.m:13
        #GENERAL PARAMETERS
        BasicParameters
        Iabc,Vabc,t=myFunctionDataProcess.DownSample(Ts,TsSim,fs,IabcOrig,VabcOrig,tOrig,nargout=3)
# traditionalDP.m:19
        lineModelParamOHL
        Rg=remoteR(1,2)
# traditionalDP.m:22
        Lg=remoteL(1,2) / wb
# traditionalDP.m:23
        I_trans,V_trans,tn=myFunctionDataProcess.FilterFundamental(f,Ts,Iabc,Vabc,t,nargout=3)
# traditionalDP.m:27
        ## Calculate fault location with traditional algorithm
        I,V=myFunctionTradDP.makeFaultPhasors(Iabc,Vabc,f,Ts,faultIncepTime,t,nargout=2)
# traditionalDP.m:31
        errorTradDP,Imp_LL=myFunctionTradDP.TradDistanceProtectionLL(I,V,L_line,wb,faultLocData,nargout=2)
# traditionalDP.m:32
        ErrorArray[j,1]=errorTradDP
# traditionalDP.m:34
        ErrorArray[j,2]=Imp_LL(1)
# traditionalDP.m:35
        ErrorArray[j,3]=dot((faultLocData / 10),Z_line) + 15
# traditionalDP.m:36
        ErrorArray[j,4]=abs(faultLocData / 10)
# traditionalDP.m:37
    
    ErrorArraySort=sortrows(ErrorArray,4)
# traditionalDP.m:40
    myFunctionTradDP.plotRX(ErrorArraySort(arange(2,end()),2),ErrorArraySort(arange(2,end()),3),Z_line)