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
import matplotlib.pyplot as plt
import timeit
import time
import tqdm
import multiprocessing as mp
from itertools import product
from itertools import repeat
import pickle

USE_CACHED_DATA = True

I_trans = None
V_trans = None
k = None
tn = None
estFaultType = None
estFaultStableTime = None

# Making arrays for k and fictitious fault impedance
k=np.arange(0.01,0.99+0.005,0.005)
LfFictArray=np.zeros((len(k),1))
RfFictArray=np.zeros((len(k),1))

pbar = tqdm.tqdm(total=196)
def update(*a):
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

    update()

    global I_trans
    global V_trans
    global k
    global tn
    global estFaultType
    global estFaultStableTime
    global LfFictArray
    global RfFictArray

    # for n in np.arange(0,len(k)-1,1):
    # for n in np.arange(0,2,1):
        # start1 = time.time()

    vF,i2,X=myFunctionCalcNetwork.NetworkParamNoCap(I_trans,V_trans,k[n],L_line,R_line,C_line,Ts,tn,Lg,Rg)

    # end1 = time.time()
    # start2 = time.time()

    LfFict,RfFict,ZfFict=myFunctionCalcFaultLocation.Fault(vF,i2,X,Ts,tn,estFaultType,estFaultStableTime)

    LfFictArray[n]=LfFict

    # end2 = time.time()

    # print("n:")
    # print(n)
    # print("Time:")
    # print(end1 - start1)
    # print(end2 - start2)

    

    return LfFict
    # return n

def write_data(name, data):

    with open(name, 'wb') as f:
        pickle.dump(data, f)

    print("Data saved to file")


def  read_data(name):

    with open(name, 'rb') as f:
        data = pickle.load(f)

    return data


# THIS IS THE MAIN SCRIPT OF THE ALGORITHM
if __name__=="__main__":

    if USE_CACHED_DATA == False:
        mp.freeze_support()

        # Load Simulation Data
        print("Load data")
        data = scipy.io.loadmat('data2.mat')

        Iabc = data['Iabc']
        Vabc = data['Vabc']
        t = data['t']

        # Fault identification and classification
        print("Detect fault")
        start = time.time()
        estFaultType,estFaultIncepTime,estFaultStableTime=myFunctionFaultSelection.FaultIndentification(Iabc,Vabc,t,f,Ts,Zbase)
        end = time.time()
        print("Time to detect fault:", end = ' ')
        print(end-start)
        print("estFaultType:", end = ' ')
        print(estFaultType)
        print("estFaultIncepTime:", end = ' ')
        print(estFaultIncepTime)
        print("estFaultStableTime:", end = ' ')
        print(estFaultStableTime)

        ## FILTER OUT THE FUNDAMENTAL FREQUENCY
        print("Filter fundamental")
        I_trans,V_trans,tn=myFunctionDataProcess.FilterFundamental(f,Ts,Iabc,Vabc,t,nargout=3)
            
        ## CALCULATING FICTITIOUS FAULT INDUCTANCE
        # Run calculation for every point in k (every point on the line)
        print("Start fault detection")
        pool = mp.Pool(processes=mp.cpu_count(), initializer=findFaultInit, initargs=(I_trans, V_trans, k, tn, estFaultType, estFaultStableTime))
        LfFictArray = pool.map(findFault, np.arange(0,len(k)))
        # LfFictArray = pool.map(findFault, np.arange(0,20))

        data = [k, LfFictArray]
        write_data("tempData", data)

    [k, LfFictArray] = read_data("tempData")

    ## Find zero crossing and hence the distance to the fault
    print("Find zero cross")
    zeroCross1=myFunctionCalcFaultLocation.findZeroCross(LfFictArray,k)
    print("zerocross:", end = ' ')
    print(zeroCross1)
    print("FaultLocData:", end = ' ')
    faultLocData = 0.3
    print(faultLocData) # Dit zou 0.3 moeten zijn
