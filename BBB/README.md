# Purpose
Code replicating and extending upon the functions of the Arduino in the hull. The BBB is much more capable than the Arduino and offers functionality that allows for much faster development.
# How to develop
The Linux image on the board does not have a graphical interface, so you have to interact with it through the terminal. You can either use something like `nano` or `vim`, or you can develop on your machine in your favorite IDE and copy the files to the BBB.
## Copy from computer to the BBB
```sh
scp -rp BBB_new/* debian@192.168.7.2:~/Sailbot/
```
## Copy from the BBB to computer
```sh
scp -r debian@192.168.7.2:~/Sailbot/* BBB/
```
## Generate protobuf files
You must generate language specific protobuf files in order to use the `.proto` definitions. To do this, run `generateProtos.sh`. If it doesn't work, check that the directories in the script match what you have going on. Use the below commands, comments in the script, and the internet to help.

Assuming you are working in the root project directory, `$SRC_DIR` is `sailbot19-20` and `$DST_DIR` is `sailbot19-20\BBB`.
### Generating protobuf files
Linux:
```bash
protoc -I=$SRC_DIR --python_out=$DST_DIR $SRC_DIR/comms.proto
```
Windows:
```sh
protoc.exe -I='$SRC_DIR' --python_out='$DST_DIR' '$SRC_DIR/comms.proto'
```
### Geneating gRPC files
Linux:
```sh
python -m grpc_tools.protoc -I=$SRC_DIR --python_out=$DST_DIR --grpc_python_out=$DST_DIR $SRC_DIR/comms.proto
```
Windows:
```sh
py -3 -m grpc_tools.protoc -I='$SRC_DIR' --python_out='$DST_DIR' --grpc_python_out='$DST_DIR' '$SRC_DIR/comms.proto'
```

## Required library files to run
`sudo pip install grpcio`

`sudo pip install protobuf`

# How to run
1. Ssh into the Beaglebone Black with `ssh debian@192.168.7.2`
2. Enter `temppwd` for the password
3. Get into the Sailbot directory with `cd Sailbot/`
4. You can either
    * Run the startup script with `./startup.sh`. If you encounter an issue, try running `chmod +x startup.sh` and trying again.
    * Run the main script and server seperately in separate terminals:
    ```sh
    python main.py
    python web_server.py
    ```