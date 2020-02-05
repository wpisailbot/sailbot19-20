#!/bin/bash

PROTOC_PATH=protoc.exe # modify this if your protoc is in a different place
NANOPB_PATH=../nanopb*/generator-bin/protoc # moodify this if your nanopb copy is elsewhere

# Generate BBB proto files
$PROTOC_PATH -I=Protos --python_out=BBB_new/gRPC Protos/*.proto
py -3 -m grpc_tools.protoc -I=Protos --python_out=BBB_new/gRPC --grpc_python_out=BBB_new/gRPC Protos/*.proto

# Generate Teensy proto files
$NANOPB_PATH --nanopb_out=./custom_libraries/nanopb-lib/ Protos/TrimTabMessages.proto
$NANOPB_PATH --nanopb_out=./custom_libraries/nanopb-lib/ Protos/PWMMessages.proto