/*
 * sv_subscriber_example.c
 *
 * Example program for Sampled Values (SV) subscriber
 *
 */

// MAC adres PI

// E4:5F:01:41:87:D5

#include "hal_thread.h"
#include <signal.h>
#include <stdio.h>
#include "sv_subscriber.h"
#include<stdlib.h>
#include <time.h>
#include <unistd.h>
#include <inttypes.h>

static bool running = true;

void sigint_handler(int signalId)
{
    running = 0;
}

typedef struct data{
    uint64_t t;

    float V1;
    float V2;
    float V3;

    float I1;
    float I2;
    float I3;

    uint32_t id;
} data_t;

int32_t ID = 0;

bool firstRun = true;
uint64_t actualTime = 0;
uint32_t overflowCnt = 0;
#define TIME_OVERFLOW_CNT   4000 - 1

/* Callback handler for received SV messages */
static void
svUpdateListener (SVSubscriber subscriber, void* parameter, SVSubscriber_ASDU asdu)
{
    // printf("svUpdateListener test\n");

    data_t data;

    // if(firstRun)
    // {
    //     // Send ID in first packet
    //     // TODO make sure that first packet is not a zero
    //     ID = SVSubscriber_ASDU_getINT32(asdu, 24);
    //     ID = 777
    //     firstRun = False
    //     fwrite(&ID, 1, sizeof(ID), stdout);
    // }else{

        uint16_t tempTime = SVSubscriber_ASDU_getSmpCnt(asdu);

        // Handle overflows
        actualTime = (uint64_t) tempTime + (overflowCnt * TIME_OVERFLOW_CNT);
        if( tempTime > TIME_OVERFLOW_CNT-1 )
        {
            overflowCnt++;
        }

        data.t = actualTime;
        
        data.I1 = (float) SVSubscriber_ASDU_getINT32(asdu, 0)/1000.0/10.0;
        data.I2 = (float) SVSubscriber_ASDU_getINT32(asdu, 8)/1000.0/10.0;
        data.I3 = (float) SVSubscriber_ASDU_getINT32(asdu, 16)/1000.0/10.0;

        data.V1 = (float) SVSubscriber_ASDU_getINT32(asdu, 32)/1000.0;
        data.V2 = (float) SVSubscriber_ASDU_getINT32(asdu, 40)/1000.0;
        data.V3 = (float) SVSubscriber_ASDU_getINT32(asdu, 48)/1000.0;

        data.id = (float) SVSubscriber_ASDU_getINT32(asdu, 24)/1000.0/10.0;

        // char str[120];
        // memset(str, 0, 120);
        // sprintf(str, "a%.2fab%.2fbc%.2fcd%.2fde%.2fef%.2ffg%.2fg\n", data.t, data.V1, data.V2, data.V3, data.I1, data.I2, data.I3);
        // sprintf(str, "%" PRIu64 " %.2f %.2f %.2f %.2f %.2f %.2f %d sizeofdata %d\n--------------------------------------------", data.t, data.V1, data.V2, data.V3, data.I1, data.I2, data.I3, data.id, sizeof(data));
        // sprintf(str, "%" PRIu64 " sizeofdata %d %d %d \n--------------------------------------------", data.t, (int) sizeof(data), (int) sizeof(data.id), (int) sizeof(data.t));

        // sprintf(str, "tempTime: %0.2f - time: %0.2f - overflowcnt: %0.2f\n----------------------------------------------------", (float) tempTime, data.t, (float) overflowCnt);

        // Write to Python
        fwrite(&data, 1, sizeof(data), stdout);
        // fwrite(&str, 1, 80, stdout);

        // Format description: https://www.typhoon-hil.com/documentation/typhoon-hil-software-manual/References/iec_61850_sampled_values_protocol.html
    // }
}

int
main(int argc, char** argv)
{
    SVReceiver receiver = SVReceiver_create();
    SVReceiver_setInterfaceId(receiver, "eth0");

    /* Create a subscriber listening to SV messages with APPID 4000h */
    SVSubscriber subscriber = SVSubscriber_create(NULL, 0x4000);

    /* Install a callback handler for the subscriber */
    SVSubscriber_setListener(subscriber, svUpdateListener, NULL);

    /* Connect the subscriber to the receiver */
    SVReceiver_addSubscriber(receiver, subscriber);

    // sleep(3);

    /* Start listening to SV messages - starts a new receiver background thread */
    SVReceiver_start(receiver);

    if (SVReceiver_isRunning(receiver)) {
        signal(SIGINT, sigint_handler);

        while (running)
            Thread_sleep(1);

        /* Stop listening to SV messages */
        SVReceiver_stop(receiver);
    }
    else {
        printf("Failed to start SV subscriber. Reason can be that the Ethernet interface doesn't exist or root permission are required.\n");
    }

    /* Cleanup and free resources */
    SVReceiver_destroy(receiver);
    return 0;
}
