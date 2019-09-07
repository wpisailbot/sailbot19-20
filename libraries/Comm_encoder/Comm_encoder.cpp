#include <Comm_encoder.h>

String encode_msg(msg message){
    String out_msg = String(message.keyword) + String(" : ") + String(message.setting);    
    return out_msg;
}

msg decode_msg(String in_msg){
    String setting = in_msg.substring(10, in_msg.length());
    msg message = {setting.toInt(), in_msg.substring(0, 7)};
    return message;
}