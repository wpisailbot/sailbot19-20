/*
  comm_encoder.h - Library for en/decoding comms
*/

#ifndef Comm_encoder_h
#define Comm_encoder_h
#include <Arduino.h>
#include <Client.h>
#include <WiFiEsp.h>

/* trim tab states*/
enum Trim_state {MIN_LIFT = 0, STBD_TACK = 1, PORT_TACK = 2,
  MAX_DRAG_STBD = 3, MAX_DRAG_PORT = 4, MAN_CTRL = 5};

const String trm_stat = "trm_stat";
const String man_ctrl = "man_ctrl";

/* msg structure */
struct msg_t
{
    int setting;
    String keyword;
}; 

#pragma pack(1)
struct rigid_msg_t
{
  int16_t state;
  int16_t curHeelAngle;
  int16_t maxHeelAngle;
  int16_t controlAngle;
  int8_t vIn;
};
#pragma pop


String encode_msg(msg_t message);
msg_t decode_msg(String message);
void send_packet(Client * client, rigid_msg_t packet);
void read_packet(Client * client, rigid_msg_t * packet);


#endif