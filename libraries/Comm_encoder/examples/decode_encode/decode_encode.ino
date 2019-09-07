#include <Comm_encoder.h>

// Encoding a message then decoding it
// Created 2019-09-06

msg msg1 = {(int)OFF, trm_tab};
msg msg2 = {(int)MIN_LIFT, trm_tab};
msg msg3 = {100, mov_bal};
msg msg4 = {0, mov_bal};
msg msg5 = {-100, mov_bal};

void setup()
{
  Serial.begin(9600);
  String string1 = encode_msg(msg1);
  String string2 = encode_msg(msg2);
  String string3 = encode_msg(msg3);
  String string4 = encode_msg(msg4);
  String string5 = encode_msg(msg5);

  Serial.println("Encoded:");
  Serial.println(string1);
  Serial.println(string2);
  Serial.println(string3);
  Serial.println(string4);
  Serial.println(string5);

  msg new_msg1 = decode_msg(string1);
  msg new_msg2 = decode_msg(string2);
  msg new_msg3 = decode_msg(string3);
  msg new_msg4 = decode_msg(string4);
  msg new_msg5 = decode_msg(string5);

  Serial.println("Decoded:");
  Serial.println(new_msg1.keyword + " : " + new_msg1.setting);
  Serial.println(new_msg2.keyword + " : " + new_msg2.setting);
  Serial.println(new_msg3.keyword + " : " + new_msg3.setting);
  Serial.println(new_msg4.keyword + " : " + new_msg4.setting);
  Serial.println(new_msg5.keyword + " : " + new_msg5.setting);

}

void loop()
{
}
