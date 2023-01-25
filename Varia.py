import numpy as np
# import RPi.GPIO as GPIO
from BasicParameters import *

def printFaultTimes(estFaultType, estFaultIncepTime, estFaultStableTime):
    print("Fault detected!")
    print("estFaultType:", end = ' ')
    print(estFaultType)
    print("estFaultIncepTime:", end = ' ')
    print(estFaultIncepTime)
    print("estFaultStableTime:", end = ' ')
    print(estFaultStableTime)


k_start = 0.01
k = np.arange(k_start,1-k_start+(1/number_of_k),(1/number_of_k))


def checkSettings():
    if USE_IEC61850_DATA:
        print("USE_IEC61850_DATA")
    if USE_SIMULATED_DATA:
        print("USE_SIMULATED_DATA")
    if USE_FIXED_STABLE_TIME:
        print("USE_FIXED_STABLE_TIME")

if everyXSamples > 4:
    raise Exception("everyXSamples must be greater or equal to 4 to ensure 1000 Hz update rate")


def saveDataToFile(idQueue, zeroCross1, time, estFaultType, estFaultIncepTime, estFaultStableTime):
    datasetNr = idQueue.get()
    filename = "RELOPEC_" + str(datasetNr) + ".txt"
    f = open(filename, "a")
    f.write(str(datasetNr))
    f.write(",")
    f.write(str(zeroCross1))
    f.write(",")
    f.write(str(time))
    f.write(",")
    f.write(str(estFaultType))
    f.write(",")
    f.write(str(estFaultIncepTime))
    f.write(",")
    f.write(str(estFaultStableTime))
    f.write("\n")
    f.close()



# def triggerGPIO():
#     pin = 12

#     GPIO.setmode(GPIO.BOARD)
#     GPIO.setup(pin, GPIO.OUT)
#     GPIO.output(pin, GPIO.HIGH)

# def GPIOCleanup():
#     GPIO.cleanup()
