# sailbot19-20
Sailbot code for 2019-2020 MQP

# Status
The following have been addressed and tested at least to some extent:
## BBB
- [X] Socket comms with the trim tab
- [X] gRPC
- [X] Modular architecture
- [X] Comms with Arduino
- [ ] Comms stability and recovery
## Arduino
- [X] Reading PWM - Arduino
- [ ] Outputting PWM - Rudder
- [ ] Outputting PWM - Ballast
- [X] Comms with BBB
- [ ] Comms stability and recovery


# Crossplatform issue tips
## Generating Protobuf and gRPC files
You must generate language specific Protobuf and gRPC files in order to use the `.proto` definitions. To do this, run `generateProtos.sh`. If it doesn't work, check that the directories in the script match what you have going on. Use the below commands, comments in the script, and the internet to help.

Also check that you have the following installed:
* [Nanopb](https://github.com/nanopb/nanopb/tree/nanopb-0.3.9.3), version 0.3.9.3 is the last known working version
* [Protobuf](https://github.com/protocolbuffers/protobuf/releases/tag/v3.11.0), version 3.11.0 is the last known working version.
* [Python3](https://www.python.org/downloads/)
* [gRPC](https://grpc.io/docs/quickstart/python/)

`$SRC_DIR` is the source of the .proto files and `$DST_DIR` is where the generated language-specific files should go. `$NANOPB_PATH` is the path to the protoc program packaged with Nanopb, and `$PROTOC_PATH` is where the protoc application packaged with Protobuf is located.

Note that the protobuf files must be generated twice - once for the BBB and once for the Arduino-based boards.

### Protobuf files for BBB
Linux:
```bash
$PROTOC_PATH -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/*.proto
```
Windows:
```sh
$PROTOC_PATH -I='$SRC_DIR' --python_out='$DST_DIR' '$SRC_DIR/*.proto'
```

### Protobuf files for Arduino-based boards
Linux:
```bash
$NANOPB_PATH --nanopb_out=$DST_DIR $SRC_DIR/TrimTabMessages.proto
$NANOPB_PATH --nanopb_out=$DST_DIR $SRC_DIR/ArduinoMessages.proto
```
Windows:
```sh
$NANOPB_PATH --nanopb_out='$DST_DIR' '$SRC_DIR/TrimTabMessages.proto'
$NANOPB_PATH --nanopb_out='$DST_DIR' '$SRC_DIR/ArduinoMessages.proto'
```


### gRPC files for BBB
Linux:
```sh
python -m grpc_tools.protoc -I=$SRC_DIR --python_out=$DST_DIR --grpc_python_out=$DST_DIR $SRC_DIR/*.proto
```
Windows:
```sh
py -3 -m grpc_tools.protoc -I='$SRC_DIR' --python_out='$DST_DIR' --grpc_python_out='$DST_DIR' '$SRC_DIR/*.proto'
```