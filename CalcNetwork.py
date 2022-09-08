# CALCULATING NETWORK PARAMETERS WHEN NOT CONSIDERING CAPACITIVE
# COUPLING BETWEEN THE TRANSMISSION LINE (PREFERRED OPTION)

from timeit import timeit
import numpy as np
import itertools
from numpy.linalg import multi_dot
from numpy.linalg import inv
import timeit
import time
from numba import njit, jit, prange

if __name__ == '__main__':
    pass

@njit(cache=True)
def NetworkParamNoCap(I_trans=None,V_trans=None,k=None,L_line=None,R_line=None,C_line=None,Ts=None,tn=None,Lg=None,Rg=None,*args,**kwargs):

    #SECTION LINE PARAMETERS 
    # before the fault
    L1=k*L_line
    R1=k*R_line
    # after the fault
    L2=(1-k)*L_line
    R2=(1-k)*R_line
    i2=I_trans
    vF = np.zeros((3,len(I_trans[0])))   

    for n in np.arange(1,len(tn)):
        DiIn=(I_trans[:,n] - I_trans[:,n-1]) / Ts
        vF[:,n]=V_trans[:,n] - L1*DiIn - R1*I_trans[:,n]

    #SECOND SECTION (after fault using state space)
    X=np.zeros((3,len(tn)))
    A=(- (R2 + Rg) / (L2 + Lg)*np.eye(3))

    temp1 = (2/3)*vF[0,:] - vF[1,:]/3 - vF[2,:]/3
    temp2 = - vF[0,:]/3 + (2/3)*vF[1,:] - vF[2,:]/3
    temp3 = - vF[0,:]/3 - vF[1,:]/3 + (2/3)*vF[2,:]

    temp = np.vstack((temp1, temp2, temp3))
    B=(1 / (L2 + Lg)) * temp

    # temp = [temp1, temp2, temp3]
    # B=np.dot((1 / (L2 + Lg)),temp)


    I=np.eye(3)

    for n in np.arange(1,len(tn)):
        # X[:,n]= np.dot(  (np.linalg.inv((I-A*Ts/2))),(   np.dot(((I+A*Ts/2)),(X[:,n-1]))  +   ((B[:,n] + B[:,n-1])*Ts/2)  )   )
        X[:,n]=   np.linalg.inv((I-A*Ts/2))  @    (  (I+A*Ts/2) @ X[:,n-1]  +   ((B[:,n] + B[:,n-1]) * (Ts/2))  )   

    
    return vF,i2,X
