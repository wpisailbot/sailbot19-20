/*
  comm_encoder.h - Library for en/decoding comms
*/

#ifndef Comm_encoder_h
#define Comm_encoder_h
#include <Arduino.h>

/* trim tab states*/
enum Trim_state {OFF = 0, NO_AP = 1, NO_PGM_PORT = 2, MIN_LIFT = 3, 
  MAX_LIFT_PORT = 4, MAX_LIFT_STBD = 5,
  MAX_DRAG_PORT = 6, MAX_DRAG_STBD = 7};
/* keywords */
const String mov_bal = "mov_bal";
const String trm_tab = "trm_tab";


/* msg structure */
struct msg
{
    int setting;
    String keyword;
};


String encode_msg(msg message);
msg decode_msg(String message);

#endif