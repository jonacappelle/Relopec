# Generated with SMOP  0.41-beta
# from libsmop import *
# lineModelParamOHL.m

    
    #CONFIGURATION FILE (2) WITH THE CHARACTERISTICS OF THE HIGH-VOLTAGE
#TRANSMISSION LINE.
    
    #2. Positive- and zero-sequence parameters at 50Hz:
    R1=0.11502
# lineModelParamOHL.m:6
    
    R0=0.39461
# lineModelParamOHL.m:7
    
    L1=0.00105
# lineModelParamOHL.m:8
    
    L0=0.00342
# lineModelParamOHL.m:9
    
    C1=1.13266e-08
# lineModelParamOHL.m:10
    
    C0=5.00782e-09
# lineModelParamOHL.m:11
    
    
    CableLen=10
# lineModelParamOHL.m:13
    
    R_line=dot(CableLen,R1)
# lineModelParamOHL.m:14
    L_line=dot(CableLen,L1)
# lineModelParamOHL.m:15
    C_line=dot(CableLen,C1)
# lineModelParamOHL.m:16
    Z_line=R_line + dot(dot(i,wb),L_line)
# lineModelParamOHL.m:17
    # X1/R1=5 X0/R0=2  I-3ph SCL=10kA, I-1ph SCL=6kA
    remoteR=concat([1.1784337797630415,0.16984155512168936])
# lineModelParamOHL.m:20
    
    remoteL=concat([0.8492077756084467,0.8492077756084467])
# lineModelParamOHL.m:21
    