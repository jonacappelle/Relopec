# Generated with SMOP  0.41-beta
# from libsmop import *
# myFunctionCalcFaultLocation.m

    #classdef myFunctionCalcFaultLocation
    
    #methods(Static)
    

def Fault(vF=None,i2=None,X=None,Ts=None,tn=None,FaultType=None,estFaultStableTime=None,*args,**kwargs):
    varargin = Fault.varargin
    nargin = Fault.nargin

    
    # voltage at the (assumed) fault location
    vFa=vF(1,arange())
# myFunctionCalcFaultLocation.m:8
    vFb=vF(2,arange())
# myFunctionCalcFaultLocation.m:9
    vFc=vF(3,arange())
# myFunctionCalcFaultLocation.m:10
    
    iaBf=i2(1,arange())
# myFunctionCalcFaultLocation.m:13
    ibBf=i2(2,arange())
# myFunctionCalcFaultLocation.m:14
    icBf=i2(3,arange())
# myFunctionCalcFaultLocation.m:15
    
    iaAf=X(1,arange())
# myFunctionCalcFaultLocation.m:18
    ibAf=X(2,arange())
# myFunctionCalcFaultLocation.m:19
    icAf=X(3,arange())
# myFunctionCalcFaultLocation.m:20
    
    if 1 == (FaultType):
        #vF = vFa;
                    #iF = (iaBf-iaAf);
        vF=copy(vFb)
# myFunctionCalcFaultLocation.m:27
        iF=(ibBf - ibAf)
# myFunctionCalcFaultLocation.m:28
        #iF = (icBf-icAf);
    else:
        if 2 == (FaultType):
            vF=vFa - vFb
# myFunctionCalcFaultLocation.m:32
            iF=(iaBf - iaAf) - (ibBf - ibAf)
# myFunctionCalcFaultLocation.m:33
        else:
            if 3 == (FaultType):
                vF=vFb - vFc
# myFunctionCalcFaultLocation.m:35
                iF=(ibBf - ibAf) - (icBf - icAf)
# myFunctionCalcFaultLocation.m:36
            else:
                if 4 == (FaultType):
                    vF=vFc - vFa
# myFunctionCalcFaultLocation.m:38
                    iF=(icBf - icAf) - (iaBf - iaAf)
# myFunctionCalcFaultLocation.m:39
                else:
                    if 5 == (FaultType):
                        vF=copy(vFa)
# myFunctionCalcFaultLocation.m:41
                        iF=(iaBf - iaAf)
# myFunctionCalcFaultLocation.m:42
    
    
    ZfFict=zeros(2,length(tn))
# myFunctionCalcFaultLocation.m:45
    
    for n in arange(2,length(tn) - 1,1).reshape(-1):
        A_matrix=concat([[iF(n) - iF(n - 1),dot((iF(n - 1) + iF(n)),Ts) / 2],[iF(n + 1) - iF(n),dot((iF(n + 1) + iF(n)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:47
        B_matrix=concat([[dot((vF(n - 1) + vF(n)),Ts) / 2],[dot((vF(n) + vF(n + 1)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:48
        ZfFict[arange(),n]=dot(inv(A_matrix),B_matrix)
# myFunctionCalcFaultLocation.m:49
    
    #find the overal inducance and resistance by taking the average
            #over one period (0.02 seconds for 50 hertz)
            #this step requires us to know the time of fault inception
    
    index1=find(tn >= (estFaultStableTime - 0.02),1,'first')
# myFunctionCalcFaultLocation.m:56
    index2=find(tn >= (estFaultStableTime),1,'first')
# myFunctionCalcFaultLocation.m:57
    LfFict=mean(ZfFict(1,arange(index1,index2)))
# myFunctionCalcFaultLocation.m:58
    
    RfFict=mean(ZfFict(2,arange(index1,index2)))
# myFunctionCalcFaultLocation.m:59
    return LfFict,RfFict,ZfFict
    
if __name__ == '__main__':
    pass
    
    
def LLLFault(vF=None,i2=None,X=None,Ts=None,tn=None,faultIncepTime=None,FaultType=None,*args,**kwargs):
    varargin = LLLFault.varargin
    nargin = LLLFault.nargin

    
    # voltage at the (assumed) fault location
    vFa=vF(1,arange())
# myFunctionCalcFaultLocation.m:65
    vFb=vF(2,arange())
# myFunctionCalcFaultLocation.m:66
    vFc=vF(3,arange())
# myFunctionCalcFaultLocation.m:67
    
    iaBf=i2(1,arange())
# myFunctionCalcFaultLocation.m:70
    ibBf=i2(2,arange())
# myFunctionCalcFaultLocation.m:71
    icBf=i2(3,arange())
# myFunctionCalcFaultLocation.m:72
    
    iaAf=X(1,arange())
# myFunctionCalcFaultLocation.m:75
    ibAf=X(2,arange())
# myFunctionCalcFaultLocation.m:76
    icAf=X(3,arange())
# myFunctionCalcFaultLocation.m:77
    vF=copy(vFa)
# myFunctionCalcFaultLocation.m:79
    iF=(iaBf - iaAf)
# myFunctionCalcFaultLocation.m:80
    ZfFict_a=zeros(2,length(tn))
# myFunctionCalcFaultLocation.m:81
    
    for n in arange(2,length(tn) - 1,1).reshape(-1):
        A_matrix=concat([[iF(n) - iF(n - 1),dot((iF(n - 1) + iF(n)),Ts) / 2],[iF(n + 1) - iF(n),dot((iF(n + 1) + iF(n)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:83
        B_matrix=concat([[dot((vF(n - 1) + vF(n)),Ts) / 2],[dot((vF(n) + vF(n + 1)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:84
        ZfFict_a[arange(),n]=dot(inv(A_matrix),B_matrix)
# myFunctionCalcFaultLocation.m:85
    
    
    vF=copy(vFb)
# myFunctionCalcFaultLocation.m:88
    iF=(ibBf - ibAf)
# myFunctionCalcFaultLocation.m:89
    ZfFict_b=zeros(2,length(tn))
# myFunctionCalcFaultLocation.m:90
    
    for n in arange(2,length(tn) - 1,1).reshape(-1):
        A_matrix=concat([[iF(n) - iF(n - 1),dot((iF(n - 1) + iF(n)),Ts) / 2],[iF(n + 1) - iF(n),dot((iF(n + 1) + iF(n)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:92
        B_matrix=concat([[dot((vF(n - 1) + vF(n)),Ts) / 2],[dot((vF(n) + vF(n + 1)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:93
        ZfFict_b[arange(),n]=dot(inv(A_matrix),B_matrix)
# myFunctionCalcFaultLocation.m:94
    
    
    vF=copy(vFc)
# myFunctionCalcFaultLocation.m:97
    iF=(icBf - icAf)
# myFunctionCalcFaultLocation.m:98
    ZfFict_c=zeros(2,length(tn))
# myFunctionCalcFaultLocation.m:99
    
    for n in arange(2,length(tn) - 1,1).reshape(-1):
        A_matrix=concat([[iF(n) - iF(n - 1),dot((iF(n - 1) + iF(n)),Ts) / 2],[iF(n + 1) - iF(n),dot((iF(n + 1) + iF(n)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:101
        B_matrix=concat([[dot((vF(n - 1) + vF(n)),Ts) / 2],[dot((vF(n) + vF(n + 1)),Ts) / 2]])
# myFunctionCalcFaultLocation.m:102
        ZfFict_c[arange(),n]=dot(inv(A_matrix),B_matrix)
# myFunctionCalcFaultLocation.m:103
    
    
    
    
    index1=find(tn >= (faultIncepTime + 0.02 + dot(0,Ts)),1,'first')
# myFunctionCalcFaultLocation.m:108
    
    index2=find(tn >= (faultIncepTime + 0.02 + dot(200,Ts)),1,'first')
# myFunctionCalcFaultLocation.m:109
    
    #Lf_Fict_raw = (1/3)*(ZfFict_a(1,:)+ZfFict_b(1,:)+ZfFict_c(1,:));
            #LfFict = mean(Lf_Fict_raw(index1:index2));
    
    
    LfFict=median(concat([mean(ZfFict_a(1,arange(index1,index2))),mean(ZfFict_b(1,arange(index1,index2))),mean(ZfFict_c(1,arange(index1,index2)))]))
# myFunctionCalcFaultLocation.m:114
    
    #this step requires us to know the time of fault inception!
    
    
    #RfFict = mean(ZfFict(2,index1:index2));
    
    
    return LfFict
    
if __name__ == '__main__':
    pass
    
    
    #THIS FUNCTION IS TO FIND THE ZERO CROSSING AND HENCE THE FAULT
        #OPTIMISATION OF THIS METHOD MIGHT YIELD BETTER RESULTS
        #I ALREADY TRIED DIFFERENT APPROACHES BUT SECOND ORDER FIT SEEMS
        #BEST 
#         function [zeroCross1] = findZeroCross(LfFictArray, k)
#             zeroCross1 = 0;
#             LfFictFit = smooth(transpose(k),LfFictArray,0.1,'rloess');
#             LfFictFit2 = polyfit(transpose(k),LfFictFit,2);
#             LfFictFit2Plot = fit(transpose(k),LfFictFit,'poly2');
#             r = roots(LfFictFit2);
#             for n = 1:1:length(r)
#                 if r(n)<1 && r(n)>0
#                     zeroCross1 = r(n);
#                 end
#             end
#             figure(5)
#             plot(k, LfFictArray,'o','color','black');
#             hold on
#             plot(LfFictFit2Plot)
#             hold off
# 
#         end
    
    
def findZeroCross(LfFictArray=None,k=None,*args,**kwargs):
    varargin = findZeroCross.varargin
    nargin = findZeroCross.nargin

    zeroCross1=0
# myFunctionCalcFaultLocation.m:149
    zeroCross2=0
# myFunctionCalcFaultLocation.m:150
    zeroCross3=0
# myFunctionCalcFaultLocation.m:151
    zeroCross4=0
# myFunctionCalcFaultLocation.m:152
    LfFictFit=smooth(transpose(k),LfFictArray,0.1,'rloess')
# myFunctionCalcFaultLocation.m:154
    LfFictFit3=smooth(transpose(k),LfFictFit,0.8,'rloess')
# myFunctionCalcFaultLocation.m:155
    LfFictFit2=polyfit(transpose(k),LfFictFit,2)
# myFunctionCalcFaultLocation.m:156
    LfFictFit2Plot=fit(transpose(k),LfFictFit,'poly2')
# myFunctionCalcFaultLocation.m:157
    r=roots(LfFictFit2)
# myFunctionCalcFaultLocation.m:158
    for n in arange(1,length(r),1).reshape(-1):
        if r(n) < 1 and r(n) > 0:
            zeroCross1=r(n)
# myFunctionCalcFaultLocation.m:161
    
    n=2
# myFunctionCalcFaultLocation.m:164
    while sign(LfFictFit3(n)) == sign(LfFictFit3(n - 1)) and n < length(k):

        n=n + 1
# myFunctionCalcFaultLocation.m:166

    
    zeroCross2=k(n - 1) + dot(abs(LfFictFit3(n - 1)),((k(n) - k(n - 1)) / abs(LfFictFit3(n) - LfFictFit3(n - 1))))
# myFunctionCalcFaultLocation.m:168
    zeroCross3=mean(concat([zeroCross1,zeroCross2]))
# myFunctionCalcFaultLocation.m:169
    figure(5)
    plot(k,LfFictArray,'o','color','black')
    hold('on')
    #     plot(k,LfFictFit)
        #     hold on
    plot(LfFictFit2Plot)
    #     hold on
        #     plot(k, LfFictFit3)
    hold('off')
    return zeroCross1
    
if __name__ == '__main__':
    pass
    
    
    #end
    
    #end