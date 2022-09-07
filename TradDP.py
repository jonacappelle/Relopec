# Generated with SMOP  0.41-beta
# from libsmop import *
# myFunctionTradDP.m

    #classdef myFunctionTradDP
    #methods(Static)
    
    
@function
def makeFaultPhasors(Iabc=None,Vabc=None,f=None,Ts=None,faultIncepTime=None,t=None,*args,**kwargs):
    varargin = makeFaultPhasors.varargin
    nargin = makeFaultPhasors.nargin

    
    T1=find(t >= (faultIncepTime - dot(2,(1 / f))),1,'first')
# myFunctionTradDP.m:6
    T2=find(t >= (faultIncepTime + dot(5,(1 / f))),1,'first')
# myFunctionTradDP.m:7
    VabcFault=transpose(Vabc(arange(),arange(T1,T2)))
# myFunctionTradDP.m:8
    IabcFault=transpose(Iabc(arange(),arange(T1,T2)))
# myFunctionTradDP.m:9
    tFault=t(arange(T1,T2))
# myFunctionTradDP.m:10
    size(VabcFault)
    wd=round((1 / f) / Ts)
# myFunctionTradDP.m:12
    I=zeros(length(IabcFault),3)
# myFunctionTradDP.m:13
    V=zeros(length(VabcFault),3)
# myFunctionTradDP.m:14
    for n in arange(wd,length(VabcFault),1).reshape(-1):
        wdI=IabcFault((arange(n - wd + 1,n)),arange())
# myFunctionTradDP.m:17
        wdV=VabcFault((arange(n - wd + 1,n)),arange())
# myFunctionTradDP.m:18
        Ifft=fft(wdI)
# myFunctionTradDP.m:19
        Vfft=fft(wdV)
# myFunctionTradDP.m:20
        I[n,arange()]=dot(2,Ifft(2,arange())) / wd
# myFunctionTradDP.m:21
        V[n,arange()]=dot(2,Vfft(2,arange())) / wd
# myFunctionTradDP.m:22
    
    return I,V
    
if __name__ == '__main__':
    pass
    
    
    
@function
def TradDistanceProtectionLL(I=None,V=None,L_line=None,wb=None,faultLocData=None,*args,**kwargs):
    varargin = TradDistanceProtectionLL.varargin
    nargin = TradDistanceProtectionLL.nargin

    X_line=dot(wb,L_line)
# myFunctionTradDP.m:27
    Imp_LL=concat([0,0,0])
# myFunctionTradDP.m:28
    
    Imp_LL[1]=(V(end(),1) - V(end(),2)) / (I(end(),1) - I(end(),2))
# myFunctionTradDP.m:31
    
    #Imp_LL(3) = (V(end,3)-V(end,1))/(I(end,3)-I(end,1));
    
    
    #[val,ind] = min(abs(Imp_LL));
            #k=imag(Imp_LL(ind))/X_line;
    k=imag(Imp_LL(1)) / X_line
# myFunctionTradDP.m:38
    error=abs((faultLocData / 10) - k)
# myFunctionTradDP.m:39
    return error,Imp_LL
    
if __name__ == '__main__':
    pass
    
    
@function
def TradDistanceProtectionLG(I=None,V=None,Z_line=None,wb=None,faultLocData=None,*args,**kwargs):
    varargin = TradDistanceProtectionLG.varargin
    nargin = TradDistanceProtectionLG.nargin

    X_line=imag(Z_line)
# myFunctionTradDP.m:43
    
    Imp_LG=V(end(),1) / I(end(),1)
# myFunctionTradDP.m:46
    
    #Imp_LG = V(end,3)/I(end,3;
    
    k=imag(Imp_LG) / X_line
# myFunctionTradDP.m:50
    error=abs((faultLocData / 10) - k)
# myFunctionTradDP.m:51
    return error,Imp_LG
    
if __name__ == '__main__':
    pass
    
    
@function
def plotRX(Imp=None,actualFaultLocation=None,Z_line=None,*args,**kwargs):
    varargin = plotRX.varargin
    nargin = plotRX.nargin

    # define zone of protection
    p1=0
# myFunctionTradDP.m:56
    p2=dot(dot(0.85,imag(Z_line)),(i - tan(dot(10,pi) / 180)))
# myFunctionTradDP.m:57
    p3=dot(dot(0.85,imag(Z_line)),i) + 60
# myFunctionTradDP.m:58
    p4=dot(cos(dot(10,pi) / 180),60) - dot(dot(i,sin(dot(1,pi) / 180)),60)
# myFunctionTradDP.m:59
    zones=concat([p1,p2,p3,p4,p1])
# myFunctionTradDP.m:60
    
    figure(4)
    plot(Imp,'o','markersize',5,'color','black','linewidth',1)
    hold('on')
    plot(zones,'color',concat([50,50,50]) / 255,'linewidth',1,'HandleVisibility','off')
    plot(actualFaultLocation,'s','markersize',5,'color','black','linewidth',1)
    
    
    
    #STYLING THE PLOT
    legend('$Z_\mathrm{relay}$','$Z_\mathrm{true}$','Location','southoutside','NumColumns',1,'Interpreter','latex','fontsize',10)
    
    title(cellarray(['Fault-loop impedance','LG Fault']),'Interpreter','latex','fontsize',10)
    
    set(gca,'Units','centimeters','Position',concat([1.5,3.5,3.2,2.8]))
    set(gcf,'Units','centimeters','Position',concat([0,0,9,8.5]))
    set(gca,'TickLabelInterpreter','latex')
    set(gca,'box','off')
    xlabel('$R \, [\Omega]$','Interpreter','latex','fontsize',10)
    ylabel('$X \, [\Omega]$','Interpreter','latex','fontsize',10)
    xlim(concat([- 5,70]))
    ylim(concat([- 10,5]))
    grid('on')
    hold('on')
    return
    
if __name__ == '__main__':
    pass
    
    
    #end
#end