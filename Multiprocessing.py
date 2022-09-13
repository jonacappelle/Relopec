import multiprocessing as mp
import tqdm
import CalcFaultLocation
import CalcNetwork


if __name__ == '__main__':
    pass


# Progress bar
pbar = tqdm.tqdm(total=200)
def update_progress(*a):
    pbar.update()

def findFaultInit(I_trans_local, V_trans_local, k_local, tn_local, estFaultType_local, estFaultStableTime_local):
    global I_trans 
    I_trans = I_trans_local
    global V_trans 
    V_trans = V_trans_local
    global k 
    k = k_local
    global tn
    tn = tn_local
    global estFaultType
    estFaultType = estFaultType_local
    global estFaultStableTime
    estFaultStableTime = estFaultStableTime_local
    return 

def findFault(n):

    update_progress()

    global I_trans
    global V_trans
    global k
    global tn
    global estFaultType
    global estFaultStableTime
    global LfFictArray
    global RfFictArray

    vF,i2,X=CalcNetwork.NetworkParamNoCap(I_trans,V_trans,k[n],L_line,R_line,C_line,Ts,tn,Lg,Rg)

    LfFict,RfFict,ZfFict=CalcFaultLocation.Fault(vF,i2,X,Ts,tn,estFaultType,estFaultStableTime)

    # LfFictArray[n]=LfFict    # This is now in parallel
    return LfFict

