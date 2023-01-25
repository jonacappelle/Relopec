import numpy as np
import time
from threading import Thread, Event
import queue

# Own libraries
import DataProcess
import FaultSelection
import CalcNetwork
import CalcFaultLocation
from BasicParameters import *
from ctypes import *
from getData import *
from Varia import *

# Making arrays for k and fictitious fault impedance
LfFictArray=np.zeros((len(k),1))
RfFictArray=np.zeros((len(k),1))

# Create a queue for buffering incomming data
dataQueue = queue.Queue()
idQueue = queue.Queue()
# Notify thread when to start - stop capturing data
startEvent = Event()
faultDetectedEvent = Event()

# Start thread to get real time data
try:
    t = Thread(target=getRealTimeData, args=(startEvent, faultDetectedEvent, dataQueue, idQueue, ))
    t.start()
except:
    print("Error: unable to start thread")

# MAIN SCRIPT OF THE ALGORITHM
if __name__=="__main__":

    checkSettings()

    print("Init data buffers")
    # Initialize data buffer and fill with bufferCalculationLength samples
    tabc, Vabc, Iabc = initDataBuffers(dataQueue, bufferCalculationLength)

    # the Z from 200 samples earlier
    previousZarray = np.zeros(bufferCalculationLength)

    estFaultIncepTime_first = True
    checkStableTime = False
    estFaultIncepTime = 0

    #########################################################
    # PART I: Needs to run at 4 kHz continuously
    #########################################################

    print("Start fault detection")
    # Fault detection loop
    while(1):

        # Do the calculations on the updated data with the latest 200st array for comparing Z
        try:
            estFaultType,estFaultIncepTime_temp,estFaultStableTime, Z = FaultSelection.RealTimeFaultIndentification( \
                                                                        Iabc[-bufferCalculationLength:], \
                                                                        Vabc[-bufferCalculationLength:], \
                                                                        tabc[-1], \
                                                                        previousZarray[int(-bufferCalculationLength/everyXSamples)], \
                                                                        Zbase, sampleFreq, gridFreq, checkStableTime) # compensate for Z array with everyXSamples
        except:
            estFaultType = 0
            estFaultIncepTime_temp = 0
            estFaultStableTime = 0
            Z = 0
            # print("Divide by zero")
        
        if estFaultIncepTime_temp != 0 and estFaultIncepTime_first:
            # Only store estFaultIncepTime's first value
            estFaultIncepTime = estFaultIncepTime_temp
            estFaultIncepTime_first = False
            
        if estFaultType != 0:
            # triggerGPIO()
            printFaultTimes(estFaultType, estFaultIncepTime, estFaultStableTime)
            break
        
        if USE_FIXED_STABLE_TIME and (not estFaultIncepTime_first) and (tabc[-1] >= (estFaultIncepTime + fixed_stable_time)):
            checkStableTime = True
                
        tabc, Vabc, Iabc = updateData(tabc, Vabc, Iabc, dataQueue, everyXSamples, bufferLength)

        # Add Z to previous array and roll
        previousZarray = rollFaster(previousZarray, Z)

    # Get some more data after fault has occurred
    tabc, Vabc, Iabc = addData(tabc, Vabc, Iabc, numberOfExtraSamplesAfterFault, dataQueue)

    print("Stop gathering data")
    # Let event handler know a fault has been detected and stop collecting data
    faultDetectedEvent.set()

    #########################################################
    # PART II: Calculate fault location: only needs to run once to fault has been identified by part I
    #########################################################
    # Second part
    print("Filter fundamental")
    start = time.time()
    I_trans,V_trans,tn=DataProcess.RealTimeFilterFundamental(Iabc,Vabc,tabc,sampleFreq,gridFreq)
    stop = time.time()
    print(f"Time filter fundamental: {stop-start}")

    # Crop data array based on the start time of fault localisation
    tn, V_trans, I_trans = DataProcess.findStartCropInceptionTime(tn, V_trans, I_trans, estFaultIncepTime)

    print("Start calculating fault location")

    # Calculate fictitious fault inductance for every point on the line (k)
    for n in np.arange(0,len(k)-1,1):
        start1 = time.time()
        vF,i2,X=CalcNetwork.NetworkParamNoCap(I_trans,V_trans,k[n],L_line,R_line,C_line,sampleFreq,tn,Lg,Rg)
        stop1 = time.time()

        start2 = time.time()
        LfFict,RfFict,ZfFict=CalcFaultLocation.Fault(vF,i2,X,sampleFreq,gridFreq,tn,estFaultType,estFaultStableTime)
        stop2 = time.time()

        LfFictArray[n]=LfFict        

    stop = time.time()

    # Find zero crossing and hence the distance to the fault
    print("Find zero cross")
    zeroCross1=CalcFaultLocation.findZeroCross(LfFictArray,k)
    # Dit zou 0.3 moeten zijn voor "data.mat" en 0.8 voor "data2.mat"

    print(f"Total time: {stop-start}")


    # Save data to file
    saveDataToFile(idQueue, zeroCross1, stop-start, estFaultType, estFaultIncepTime, estFaultStableTime)

    # GPIOCleanup()
