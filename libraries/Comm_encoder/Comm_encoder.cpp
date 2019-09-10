#include <Comm_encoder.h>
#include <Client.h>
#include <WiFiEsp.h>

String encode_msg(msg_t message){
    String out_msg = String(message.keyword) + String(" : ") + String(message.setting);    
    return out_msg;
}

msg_t decode_msg(String in_msg){
    String setting = in_msg.substring(10, in_msg.length());
    msg_t message = {(int)setting.toInt(), in_msg.substring(0, 7)};
    return message;
}

void send_packet(Client * client, rigid_msg_t packet){
    client->write((byte *) &packet, sizeof(rigid_msg_t));
}

void read_packet(Client * client, rigid_msg_t * packet){
    int buffer_size = client->available();
    byte buffer[buffer_size];
    for(int i = 0; i < buffer_size; i++){
        buffer[i] = client->read();
    }

    packet = (rigid_msg_t *) buffer;
}