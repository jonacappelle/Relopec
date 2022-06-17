# Generated with SMOP  0.41-beta
# from libsmop import *
# myFunctionCalcNetwork.m

    # This script is to calculate the current and voltages (at the
# assumed fault location). 
#classdef myFunctionCalcNetwork
    
    #methods(Static) 
        # CALCULATING NETWORK PARAMETERS WHEN NOT CONSIDERING CAPACITIVE
        # COUPLING BETWEEN THE TRANSMISSION LINE (PREFERRED OPTION)
    
    

def NetworkParamNoCap(I_trans=None,V_trans=None,k=None,L_line=None,R_line=None,C_line=None,Ts=None,tn=None,Lg=None,Rg=None,*args,**kwargs):
    varargin = NetworkParamNoCap.varargin
    nargin = NetworkParamNoCap.nargin

    #SECTION LINE PARAMETERS 
            # before the fault
    L1=dot(k,L_line)
# myFunctionCalcNetwork.m:12
    R1=dot(k,R_line)
# myFunctionCalcNetwork.m:13
    
    L2=dot((1 - k),L_line)
# myFunctionCalcNetwork.m:15
    R2=dot((1 - k),R_line)
# myFunctionCalcNetwork.m:16
    
    i2=copy(I_trans)
# myFunctionCalcNetwork.m:19
    for n in arange(2,length(tn),1).reshape(-1):
        DiIn=(I_trans(arange(),n) - I_trans(arange(),n - 1)) / Ts
# myFunctionCalcNetwork.m:21
        vF[arange(),n]=V_trans(arange(),n) - dot(L1,DiIn) - dot(R1,I_trans(arange(),n))
# myFunctionCalcNetwork.m:22
    
    #SECOND SECTION (after fault using state space)
    X=zeros(3,length(tn))
# myFunctionCalcNetwork.m:26
    A=dot((- (R2 + Rg) / (L2 + Lg)),eye(3))
# myFunctionCalcNetwork.m:27
    B=dot((1 / (L2 + Lg)),concat([[dot((2 / 3),vF(1,arange())) - vF(2,arange()) / 3 - vF(3,arange()) / 3],[- vF(1,arange()) / 3 + dot((2 / 3),vF(2,arange())) - vF(3,arange()) / 3],[- vF(1,arange()) / 3 - vF(2,arange()) / 3 + dot((2 / 3),vF(3,arange()))]]))
# myFunctionCalcNetwork.m:28
    I=eye(3)
# myFunctionCalcNetwork.m:31
    for n in arange(2,length(tn),1).reshape(-1):
        X[arange(),n]=dot(((I - dot(A,Ts) / 2) ** (- 1)),(dot((I + dot(A,Ts) / 2),X(arange(),n - 1)) + dot((B(arange(),n) + B(arange(),n - 1)),Ts) / 2))
# myFunctionCalcNetwork.m:33
    
    return vF,i2,X
    
if __name__ == '__main__':
    pass
    
    
    # CALCULATE NETWORK PARAMETERS WHEN INCORPORATING CAPACITIVE
        # COUPLING BETWEEN THE TRANSMISSION LINES (NOT WORKING TOO WELL)
    

def NetworkParamWithCap(I_trans=None,V_trans=None,k=None,L_line=None,R_line=None,C_line=None,Ts=None,tn=None,Lg=None,Rg=None,*args,**kwargs):
    varargin = NetworkParamWithCap.varargin
    nargin = NetworkParamWithCap.nargin

    
    #SECTION LINE PARAMETERS
    TLen1=0.5
# myFunctionCalcNetwork.m:42
    TLen2=1 - TLen1
# myFunctionCalcNetwork.m:43
    L1=dot(dot(TLen1,k),L_line)
# myFunctionCalcNetwork.m:45
    R1=dot(dot(TLen1,k),R_line)
# myFunctionCalcNetwork.m:46
    C1=dot(dot(TLen1,k),C_line)
# myFunctionCalcNetwork.m:47
    L2=dot(dot(TLen2,(1 - k)),L_line)
# myFunctionCalcNetwork.m:49
    R2=dot(dot(TLen2,(1 - k)),R_line)
# myFunctionCalcNetwork.m:50
    C2=dot(dot(TLen2,(1 - k)),C_line)
# myFunctionCalcNetwork.m:51
    
    #FIRST SECTION (with caps)
    vC1=zeros(3,length(tn))
# myFunctionCalcNetwork.m:55
    i2=zeros(3,length(tn))
# myFunctionCalcNetwork.m:56
    vF=zeros(3,length(tn))
# myFunctionCalcNetwork.m:57
    v0C1=zeros(1,length(tn))
# myFunctionCalcNetwork.m:58
    for n in arange(2,length(tn),1).reshape(-1):
        # VOLTAGE AT FIRST CAP
        DiIn=(I_trans(arange(),n) - I_trans(arange(),n - 1)) / Ts
# myFunctionCalcNetwork.m:62
        vC1[arange(),n]=V_trans(arange(),n) - dot(L1,DiIn) - dot(R1,I_trans(arange(),n))
# myFunctionCalcNetwork.m:63
        v0C1[n]=dot((1 / 3),(vC1(1,n) + vC1(2,n) + vC1(3,n)))
# myFunctionCalcNetwork.m:66
        Dv0C1=(v0C1(n) - v0C1(n - 1)) / Ts
# myFunctionCalcNetwork.m:67
        i2[1,n]=I_trans(1,n) - dot(C1,((vC1(1,n) - vC1(1,n - 1)) / Ts - Dv0C1))
# myFunctionCalcNetwork.m:68
        i2[2,n]=I_trans(2,n) - dot(C1,((vC1(2,n) - vC1(2,n - 1)) / Ts - Dv0C1))
# myFunctionCalcNetwork.m:69
        i2[3,n]=I_trans(3,n) - dot(C1,((vC1(3,n) - vC1(3,n - 1)) / Ts - Dv0C1))
# myFunctionCalcNetwork.m:70
        Di2=(i2(arange(),n) - i2(arange(),n - 1)) / Ts
# myFunctionCalcNetwork.m:73
        vF[arange(),n]=vC1(arange(),n) - dot(L1,Di2) - dot(R1,i2(arange(),n))
# myFunctionCalcNetwork.m:74
    
    
    #SECOND SECTION (with caps)
    X=zeros(9,length(tn))
# myFunctionCalcNetwork.m:78
    Dv0=zeros(1,length(tn))
# myFunctionCalcNetwork.m:79
    v0=dot((1 / 3),(vF(1,arange()) + vF(2,arange()) + vF(3,arange())))
# myFunctionCalcNetwork.m:80
    for n in arange(2,length(tn),1).reshape(-1):
        Dv0[n]=(v0(n) - v0(n - 1)) / Ts
# myFunctionCalcNetwork.m:82
    
    U=concat([[dot((1 / L2),vF(1,arange()))],[dot((1 / L2),vF(2,arange()))],[dot((1 / L2),vF(3,arange()))],[Dv0],[Dv0],[Dv0],[- v0 / (L2 + Lg)],[- v0 / (L2 + Lg)],[- v0 / (L2 + Lg)]])
# myFunctionCalcNetwork.m:84
    A=concat([[- R2 / L2,0,0,- 1 / L2,0,0,0,0,0],[0,- R2 / L2,0,0,- 1 / L2,0,0,0,0],[0,0,- R2 / L2,0,0,- 1 / L2,0,0,0],[1 / C2,0,0,0,0,0,- 1 / C2,0,0],[0,1 / C2,0,0,0,0,0,- 1 / C2,0],[0,0,1 / C2,0,0,0,0,0,- 1 / C2],[0,0,0,1 / (L2 + Lg),0,0,- (R2 + Rg) / (L2 + Lg),0,0],[0,0,0,0,1 / (L2 + Lg),0,0,- (R2 + Rg) / (L2 + Lg),0],[0,0,0,0,0,1 / (L2 + Lg),0,0,- (R2 + Rg) / (L2 + Lg)]])
# myFunctionCalcNetwork.m:87
    I=eye(9)
# myFunctionCalcNetwork.m:96
    for n in arange(2,length(tn),1).reshape(-1):
        X[arange(),n]=dot((pinv(I - dot(A,Ts) / 2)),(dot((I + dot(A,Ts) / 2),X(arange(),n - 1)) + dot((U(arange(),n) + U(arange(),n - 1)),Ts) / 2))
# myFunctionCalcNetwork.m:98
    
    return vF,i2,X
    
if __name__ == '__main__':
    pass
    
    
    
    #end
#end