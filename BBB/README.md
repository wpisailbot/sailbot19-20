# How to develop
__If you are developing from scratch, head on over to the `/helloworld/` directory in this folder and follow the instructions there.__

The Linux image on the board does not have a graphical interface, so you have to interact with it through the terminal. You can either use something like `nano` or `vim`, or you can develop on your machine in your favorite IDE and copy the files to the BBB. We used VS Code for our development and copied the files over for testing.
## Copy from computer to the BBB
```sh
scp -rp BBB_new/* debian@192.168.7.2:~/Sailbot/
```
## Copy from the BBB to computer
```sh
scp -r debian@192.168.7.2:~/Sailbot/* BBB/
```

# How to run
We will use 192.168.7.2 here, but you may need to change this to match the IP address assigned to the board by your router if you're connecting using LAN.

1. SSH into the BeagleBone Black with `ssh debian@192.168.7.2` (or navigate to 192.168.7.2 and use the terminal there and skip to step 3).
2. Enter `temppwd` for the password
3. Make directory for project code `mkdir Sailbot`
4. Get into the Sailbot directory with `cd Sailbot/`
5. You can 
    * Run the startup script with `./startup.sh`. If you encounter an issue, try running `chmod +x startup.sh` and trying again.
    * Run the main script and server seperately in separate terminals:
    ```sh
    python3 main.py
    python -m webserver.webserver
    ```
    * To run modules standalone, run `python3 -m Example.example`, where example is the module in `Example/example.py`

## Troubleshooting
If you see that one Protobuf/gRPC file can't find another, run `2to3-2.7 gRPC/ -w -n` from the `Sailbot/` directory. Protobuf uses the Python2 import scheme and this command does the conversion.