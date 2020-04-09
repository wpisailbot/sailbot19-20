import Constants as CONST

def LOG_I(message):
    """
    Prints a message with the color-coded INFO: header
    :param message [string] The message to print
    """
    print(CONST.INFO + "INFO: " + CONST.ENDC + message)

def LOG_E(message):
    """
    Prints a message with the color-coded ERNO: header
    :param message [string] The message to print
    """
    print(CONST.ERNO + "ERNO: " + CONST.ENDC + message)

def LOG_W(message):
    """
    Prints a message with the color-coded WARN: header
    :param message [string] The message to print
    """
    print(CONST.WARN + "WARN: " + CONST.ENDC + message)

def LOG_F(message):
    """
    Prints a message with the color-coded FAIL: header
    :param message [string] The message to print
    """
    print(CONST.FAIL + "FAIL: " + CONST.ENDC + message)

def LOG_D(message):
    """
    Prints a message with the color-coded DEBG: header
    :param message [string] The message to print
    """
    print(CONST.DEBG + "DEBG: " + CONST.ENDC + message)

def LOG_M(message):
    """
    Prints a message with the color-coded MESS: header
    :param message [proto.vessel_state] The message to print
    """
    print(CONST.MESS + "MESS: " + CONST.ENDC)
    print(str(message))
    
