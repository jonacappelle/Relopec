/*
 * sv_subscriber_example.c
 *
 * Example program for Sampled Values (SV) subscriber
 *
 */

#include "hal_thread.h"
#include <signal.h>
#include <stdio.h>
#include "sv_subscriber.h"


static bool running = true;

void sigint_handler(int signalId)
{
    running = 0;
}

typedef struct data{
    float t;
    float V1;
    float V2;
    float V3;
    float I1;
    float I2;
    float I3;
} data_t;

/* Callback handler for received SV messages */
static void
svUpdateListener (SVSubscriber subscriber, void* parameter, SVSubscriber_ASDU asdu)
{
    // printf("svUpdateListener test\n");

    data_t data;
    data.t = (float) SVSubscriber_ASDU_getSmpCnt(asdu);

    data.I1 = (float) SVSubscriber_ASDU_getINT32(asdu, 0)/1000.0;
    data.I2 = (float) SVSubscriber_ASDU_getINT32(asdu, 0)/1000.0;
    data.I3 = (float) SVSubscriber_ASDU_getINT32(asdu, 0)/1000.0;

    data.V1 = (float) SVSubscriber_ASDU_getINT32(asdu, 0)/1000.0;
    data.V2 = (float) SVSubscriber_ASDU_getINT32(asdu, 0)/1000.0;
    data.V3 = (float) SVSubscriber_ASDU_getINT32(asdu, 0)/1000.0;

    char str[100];
    memset(str, 0, 100);
    // sprintf(str, "a%.2fab%.2fbc%.2fcd%.2fde%.2fef%.2ffg%.2fg\n", data.t, data.V1, data.V2, data.V3, data.I1, data.I2, data.I3);
    // sprintf(str, "%.2f %.2f %.2f %.2f %.2f %.2f %.2f", data.t, data.V1, data.V2, data.V3, data.I1, data.I2, data.I3);

    // Write to Python
    fwrite(str, 1, 100, stdout);

    // printf("Size: %d", SVSubscriber_ASDU_getDataSize(asdu));

    // const char* svID = SVSubscriber_ASDU_getSvId(asdu);

    // if (svID != NULL)
    //     printf("  svID=(%s)\n", svID);

    // printf("  smpCnt: %i\n", SVSubscriber_ASDU_getSmpCnt(asdu));
    // printf("  confRev: %u\n", SVSubscriber_ASDU_getConfRev(asdu));

    // /*
    //  * Access to the data requires a priori knowledge of the data set.
    //  * For this example we assume a data set consisting of FLOAT32 values.
    //  * A FLOAT32 value is encoded as 4 bytes. You can find the first FLOAT32
    //  * value at byte position 0, the second value at byte position 4, the third
    //  * value at byte position 8, and so on.
    //  *
    //  * To prevent damages due configuration, please check the length of the
    //  * data block of the SV message before accessing the data.
    //  */

    // char temp[100];
    // temp = SVSubscriber_ASDU_getDatSet(asdu);
    // printf("%X %X %X %X", temp[0], temp[1], temp[2], temp[3]);

    // Format description: https://www.typhoon-hil.com/documentation/typhoon-hil-software-manual/References/iec_61850_sampled_values_protocol.html

    // if (SVSubscriber_ASDU_getDataSize(asdu) == 64) {
    //     printf("ATCTR1 Amp: %f\n", (float) SVSubscriber_ASDU_getINT32(asdu, 0)/1000.0);
    //     printf("BTCTR2 Amp %f\n", (float) SVSubscriber_ASDU_getINT32(asdu, 8)/1000.0);
    //     printf("CTCTR2 Amp: %f\n", (float) SVSubscriber_ASDU_getINT32(asdu, 16)/1000.0);
    //     // printf("NmTCTR4 Amp: %f\n", (float) SVSubscriber_ASDU_getINT32(asdu, 24)/1000.0);

    //     printf("ATVTR1: %f\n", (float) SVSubscriber_ASDU_getINT32(asdu, 32)/100.0);
    //     printf("BTVTR2: %f\n", (float) SVSubscriber_ASDU_getINT32(asdu, 40)/100.0);
    //     printf("CTVTR3: %f\n", (float) SVSubscriber_ASDU_getINT32(asdu, 48)/100.0);
    //     // printf("NmTVTR4: %f\n", (float) SVSubscriber_ASDU_getINT32(asdu, 56)/100.0);
    // }
}

int
main(int argc, char** argv)
{
    SVReceiver receiver = SVReceiver_create();

    // if (argc > 1) {
    //     SVReceiver_setInterfaceId(receiver, argv[1]);
	// 	printf("Set interface id: %s\n", argv[1]);
    // }
    // else {
    //     printf("Using interface enp0s3\n");
        SVReceiver_setInterfaceId(receiver, "eth0");
    // }

    /* Create a subscriber listening to SV messages with APPID 4000h */
    SVSubscriber subscriber = SVSubscriber_create(NULL, 0x4000);

    /* Install a callback handler for the subscriber */
    SVSubscriber_setListener(subscriber, svUpdateListener, NULL);

    /* Connect the subscriber to the receiver */
    SVReceiver_addSubscriber(receiver, subscriber);

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
