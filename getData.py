import pickle
import scipy.io
import sys
import numpy as np
from numba import njit, objmode
import struct

from BasicParameters import USE_IEC61850_DATA, USE_SIMULATED_DATA, sampleFreq


if __name__ == '__main__':
    pass

# Global variables
faultDetected = False

# Dataset
MatlabSimDataSet = scipy.io.loadmat('data2.mat')
MatlabSimDataSetIndex = 0

# Global variable for printing buffer occupancy
cnt = 0

def getData(dataQueue):

    # Get data from Queue
    data = dataQueue.get()
    
    global cnt
    cnt += 1
    if cnt >= 5000:
        cnt = 0
        print(f"Buffer size: {dataQueue.qsize()}")

    return data[0], data[1], data[2]

def initDataBuffers(dataQueue, bufferCalculationLength):

    # Get the first set of data
    tabc, Vabc, Iabc = getData(dataQueue)

    # Fill array for first time
    sample_cnt = 0
    while(sample_cnt <= bufferCalculationLength - 2): # with len of 200, only take 198
        t, V, I = getData(dataQueue)
        Iabc = np.vstack((Iabc, I))
        Vabc = np.vstack((Vabc, V))
        tabc = np.append(tabc, t)
        sample_cnt += 1

    return tabc, Vabc, Iabc

def rollFaster(x, newdata):

    x[0:-1] = x[1:]
    x[-1] = newdata
    return x

def updateData(tabc, Vabc, Iabc, dataQueue, everyXSamples, bufferLength):

    for x in range(everyXSamples):
        # Fill last place with new data
        t, V, I = getData(dataQueue) # Data is comming in at 4kHz or faster from C program (checked)

        if len(tabc) <= bufferLength:
            # Append data to full array if not full yet
            Iabc = np.vstack((Iabc, I))
            Vabc = np.vstack((Vabc, V))
            tabc = np.append(tabc, t)
        else:
            Iabc = rollFaster(Iabc, I)
            Vabc = rollFaster(Vabc, V)
            tabc = rollFaster(tabc, t)

    return tabc, Vabc, Iabc

def addData(tabc, Vabc, Iabc, amount, dataQueue):

    for x in range(amount):

        # Fill last place with new data
        t, V, I = getData(dataQueue) # Data is comming in at 4kHz or faster from C program (checked)

        Iabc = rollFaster(Iabc, I)
        Vabc = rollFaster(Vabc, V)
        tabc = rollFaster(tabc, t)

        x += 1

    return tabc, Vabc, Iabc

def write_data(name, data):

    with open(name, 'wb') as f:
        pickle.dump(data, f)

    print("Data saved to file")

def  read_data(name):

    with open(name, 'rb') as f:
        data = pickle.load(f)

    return data


def getRealTimeData(faultDetectedEvent, dataQueue):

    print("Start RealTimeData Thread")

    global MatlabSimDataSetIndex
    global faultDetected

    # Keep running until fault is detected
    while(not faultDetectedEvent.is_set()):

        if USE_SIMULATED_DATA == True:

            MatlabSimDataSetIndex += 1

            t = MatlabSimDataSet['t']
            Iabc = MatlabSimDataSet['Iabc'].transpose()
            Vabc = MatlabSimDataSet['Vabc'].transpose()

            if(MatlabSimDataSetIndex > len(t)-2 ):
                break

            # Buffer the data to transfer to main algorithm
            dataQueue.put( np.array( (t[MatlabSimDataSetIndex,0], Vabc[MatlabSimDataSetIndex], Iabc[MatlabSimDataSetIndex]), dtype=object ) )

        if USE_IEC61850_DATA == True:

            # Read the data
            temp = sys.stdin.buffer.read(32)

            # uint64_t - float x6
            splitPacket = struct.unpack('Qffffff', temp)

            t = splitPacket[0] / sampleFreq

            V1 = splitPacket[1]
            V2 = splitPacket[2]
            V3 = splitPacket[3]

            I1 = splitPacket[4]
            I2 = splitPacket[5]
            I3 = splitPacket[6]

            V = np.array( (V1, V2, V3) )
            I = np.array( (I1, I2, I3) )

            dataQueue.put( np.array( (t, V, I), dtype=object ) )
