import serial
import json

class AirmarReader():

    def __init__(self):
        #open serial port
        self.serial = serial.Serial('/dev/ttyAMC0')


        #TODO -either make a into a ros node or multithread
        # - create function to read (in own thread) and return/publish as json.dumps({})
        
    def readLineToJson(self, line):

        tag = line.split(',',1)[0]
        type_code = tag[-3:]
        args = line.split(',')
        args[len(args) - 1] = args[len(args) - 1].split('*')[0] #get rid of checksum

        if(type_code == 'ROT'): #rate of turn degrees per minute. negative is to port
            return {"rate-of-turn":args[1]}
        elif(type_code == 'GLL'):
            return {"Latitude":args[1], 
                    "Latitude-direction":args[2],
                    "Longitude":args[3],
                    "Longitude-direction":args[4]}
        elif(type_code == 'VTG'):
            return {"track-degrees-true":args[1],
                    "track-degrees-magnetic":args[3],
                    "speed-knots":args[5],
                    "speed-kmh":args[7]}
        elif(type_code == 'XDR'):
            ret = {}
            if(args[4] == "ENV_OUTSIDE_T"): #in celcius
                ret["outside-temp"] = args[2]
            elif(args[4] == "ENV_ATMOS_P"): #in ???
                ret["atmospheric-pressure"] = args[2]
            if(len(args) > 5):
                if(args[8] == "ENV_OUTSIDE_T"): #in celcius
                    ret["outside-temp"] = args[6]
                elif(args[8] == "ENV_ATMOS_P"): #in ???
                    ret["atmospheric-pressure"] = args[6]
            
            return ret
        
        elif(type_code == 'HDG'):
            return {"magnetic-sensor-heading":args[1], #degrees
                    "magnetic-deviation":args[2], #degrees
                    "magnetic-deviation-direction":args[3],
                    "magnetic-variation":args[4], #degrees
                    "magnetic-variation-direction":args[5]}
        
        elif(type_code == 'VHW'): #water speed and direction (speed not showing up)
            return {}  #not sure we need
        elif(type_code == 'GGA'): #GPS position, quality, elevation, # of satilites
            return {} #not sure needed, repeated gps from GLL
        elif(type_code == 'DTM'): #unreferenced in documentation except as datnum reference -- unusable
            return {}
        elif(type_code == 'GSV'): #GPS satilites in view
            return {} #no need for this data
        elif(type_code == 'GSA'): # GPS Dilution of Precision
            return {} #not sure if needed
        elif(type_code == 'GRS'): #"The GRS message is used to support the Receiver Autonomous Integrity Monitoring (RAIM)." -- unneeded
            return {}
        elif(type_code == 'MWD'): 
            return {"wind-angle-true":args[1], # in degrees
                    "wind-speed-true-knots":args[5],
                    "wind-speed-true-meters":args[7]} #in m/s
        elif(type_code == 'MWV'):
            return {"wind-angle-relative":args[1], # in degrees
                    "wind-speed-relative-meters":args[3]} #in m/s
        elif(type_code == 'ZDA'): #date & time
            return {} # unneeded
        elif(type_code == 'OUT'): #real key is 'PMAROUT', shortened to OUT, since all others are 3 letters
            #"PGN is translated to a Maretron proprietary NMEA 0183 sentence " -- used for pitch and roll
            return {"roll":args[2],
                    "pitch":args[3]}
        else:
            raise ValueError("Unknown NEMA code: " + type_code)
            return {}
