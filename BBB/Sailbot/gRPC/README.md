# gRPC files are GENERATED
These files are here to enable easy startup. If you modify the implementations on how gRPC is used or how the messages are defined, you have to regenerate the files.

To regenerate these files: 
- Run `generateProtos.sh` using bash command. You may have to change where the script looks for the protoc programs for Google and Nanopb.
- If applicable, place the regenerated Arduino files in the libraries directory of your Arduino installation (follow the [instructions for adding custom libraries](https://www.arduino.cc/en/hacking/libraries) if this is confusing). These files are placed in `./sailbot19-20/custom-libraries/nanopb-lib`. Place all .h files, including the ones in all subfolders, into the custom Arduino library folder.