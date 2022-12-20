# FAULT CALCULATION
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from numba import njit

if __name__ == '__main__':
    pass

@njit(cache=True)
def calculate_optimized(iF, vF, Ts, tn):
    ZfFict=np.zeros((2,len(tn)))

    for n in np.arange(1,len(tn) - 1,1):
        A_matrix=np.array( ((iF[n] - iF[n - 1]), (((iF[n - 1] + iF[n]) * Ts) / 2), (iF[n + 1] - iF[n]), (((iF[n + 1] + iF[n]) * Ts) / 2))  )
        B_matrix=np.array(( ((vF[n - 1] + vF[n]) * (Ts/2)), ((vF[n] + vF[n + 1]) * (Ts/2)) ))
        A_matrix1 = np.reshape(A_matrix, (2,2))

        ZfFict[:,n]= (np.linalg.pinv(A_matrix1) @ B_matrix) # Compute pseudo inverse of matrix if it can't be inversed

    return ZfFict

def Fault(vF=None,i2=None,X=None,sampleFreq=None,gridFreq=None,tn=None,FaultType=None,estFaultStableTime=None,*args,**kwargs):
    
    Ts=1/sampleFreq
    iF = None
    LfFict = None
    RfFict = None

    # voltage at the (assumed) fault location
    vFa=vF[0,:]
    vFb=vF[1,:]
    vFc=vF[2,:]
    
    iaBf=i2[0,:]
    ibBf=i2[1,:]
    icBf=i2[2,:]
    
    iaAf=X[0,:]
    ibAf=X[1,:]
    icAf=X[2,:]
    
    if 1 == (FaultType):
        vF=vFb.copy()
        iF=(ibBf - ibAf)
    else:
        if 2 == (FaultType):
            vF=vFa - vFb
            iF=(iaBf - iaAf) - (ibBf - ibAf)
        else:
            if 3 == (FaultType):
                vF=vFb - vFc
                iF=(ibBf - ibAf) - (icBf - icAf)
            else:
                if 4 == (FaultType):
                    vF=vFc - vFa
                    iF=(icBf - icAf) - (iaBf - iaAf)
                else:
                    if 5 == (FaultType):
                        vF=vFa.copy()
                        iF=(iaBf - iaAf)

    ZfFict = calculate_optimized(iF, vF, Ts, tn)

    # Find the overal inducance and resistance by taking the average over one period (0.02 seconds for 50 hertz) \
    # this step requires us to know the time of fault inception
    index1=np.argwhere(tn >= (estFaultStableTime - (1/gridFreq)) )
    if(index1[0][0] == 0 ):
        print("Choose a bigger window")
    index2=np.argwhere(tn >= estFaultStableTime)

    LfFict=np.mean(ZfFict[0,index1[0][0]:index2[0][0]])
    RfFict=np.mean(ZfFict[1,index1[0][0]:index2[0][0]]) # This is not even necessary I guess
    return LfFict,RfFict,ZfFict

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth 

def removeOutliers(x, y):
    y = np.array(y[:,0])
    x = np.array(x)

    mean = np.mean(y)
    standard_deviation = np.std(y)
    distance_from_mean = abs(y - mean)
    max_deviations = 1
    
    not_outlier = distance_from_mean < max_deviations * standard_deviation
    y_noOutliers = y[not_outlier]
    x_noOutliers = x[not_outlier]
    return x_noOutliers, y_noOutliers

def findZeroCross(LfFictArray=None,k=None,*args,**kwargs):

    zeroCross=0

    # Remove outliers
    k_noOutliers, LfFictFit_noOutliers = removeOutliers(k, LfFictArray)
    
    # Smooth
    LfFictFit_noOutliers=smooth(LfFictFit_noOutliers,20) # frac = +-0.1

    LfFictFit2=np.polyfit(k_noOutliers,LfFictFit_noOutliers,2)
    y_np = np.polyval(LfFictFit2, k)

    # Calculate zeros
    r=np.roots(LfFictFit2)
    for n in np.arange(0,len(r),1):
        if r[n] < 1 and r[n] > 0:
            zeroCross=abs(r[n])
    
    # Always remove imaginary part
    try:
        zeroCross = zeroCross.real
    except:
        zeroCross = zeroCross

    # Find minimum of polyfit

    print("fault location:", end = ' ')
    print(zeroCross)

    # Plotting
    # plt.scatter(k, LfFictArray, color="grey", alpha=0.5, label="Data")
    # plt.scatter(k_noOutliers, LfFictFit_noOutliers, color="green", alpha=0.5, label="No outliers + smoothed")
    # # plt.plot(k, y_np, color="red", label="Fit np")
    # plt.legend()
    # plt.title("ZeroCross: " + str('{:.3f}'.format(zeroCross1)))
    # plt.ylim(-0.03, 0.03)
    # plt.savefig("result.png")
    # plt.show()
    
    return zeroCross
