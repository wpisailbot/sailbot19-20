import serial
import json

class AirmarReader():

    def __init__(self):
        #open serial port
        self.serial = serial.Serial('/dev/ttyAMC0')
        


    def readLineToJson(self):

        line = self.serial.readline()
        tag = line.split(',',1)[0]
        type_code = tag[-3:]
        args = line.split(',')

        if(type_code == 'ROT'):
            return json.dumps({"rotation":args[1]})
        elif(type_code == 'GLL'):
            #TODO
            return "TODO"
        elif(type_code == 'VTG'):
            #not sure if all fields needed
            return json.dumps({"speed-knots":args[4],
                               "speed-kmh":args[6]})
        elif(type_code == 'XDR'):
            return json.dumps({"outside-temp":args[2],
                               "atmospheric-pressure":args[6]})
        elif(type_code == 'HDG'):
            #TODO
            return json.dumps({"":args[]})
        elif(type_code == 'VHW'):
            return json.dumps({"":args[]})
        elif(type_code == 'GGA'):
            return json.dumps({"":args[]})
        elif(type_code == ''):
            return json.dumps({"":args[]})
        elif(type_code == ''):
            return json.dumps({"":args[]})
        elif(type_code == ''):
            return json.dumps({"":args[]})
        elif(type_code == ''):
            return json.dumps({"":args[]})
        elif(type_code == ''):
            return json.dumps({"":args[]})
            
    
