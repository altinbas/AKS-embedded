import serial
import settings
from serial.tools import list_ports

def getAllPorts():
    ''' Reads all the available serial ports from the system,
        then classify them based on their descriptions. '''
    # USB file paths, might be different on different systems.
    usbTemplate = settings.usbTemplate
    # Port list dictionary.
    portList = {}

    # Initialize serial port dictionary.
    plist = list_ports.comports()

    # Iterate over all ports to classify them.
    for port in plist:
        print(port.description)
        # Car's battery shows up as "USB2.0 Ser!" in the system.
        if "Ser!" in port.description:
            portList["Battery"] = usbTemplate.format(port.name)
        elif "UART" in port.description:
            portList["XBee"] = usbTemplate.format(port.name)
        elif "Serial" in port.description:
            portList["Generic"] = usbTemplate.format(port.name)
        else:
            portList["Discard"] = usbTemplate.format(port.name)
    return portList

def openPorts(portList):
    ''' Opens given ports except the discarded ones and
        return the open ports dictionary. '''
    # Dictionary that holds the open port names and serial properties.
    openPorts = {}

    # Get every item in the given ports list and open them individually.
    for name, port in portList.items():
        # If the port is not one of the discarded ones, open the port and save it to openPorts dictionary.
        if name != "Discard":
            try:
                if name != "Generic":
                    openPorts[name] = serial.Serial(port,
                        baudrate = settings.portSettings["baudrate"],
                        timeout = settings.portSettings["timeout"])
                else:
                    openPorts[name] = serial.Serial(port,
                        baudrate = settings.portSettings["gpsBaudrate"],
                        timeout = settings.portSettings["timeout"])
            except:
                print("Error occured while trying to open port: " + name + " " + port)
    return openPorts

def closePorts(portList):
    ''' Closes the ports given with portList. '''
    # Iterate over all the open ports, then try to close them.
    for name, port in portList.items():
        print("Closing port: " + name)
        try:
            port.close()
        except:
            print("Could not disconnect from the port?")

def writeToPort(port, data):
    ''' Writes the given data to the given port. '''
    try:
        port.write(data)
    except:
        print("Could not write data to given port")

def readFromPort(port):
    ''' Reads data from the given port then returns it. '''
    try:
        return port.readline()
    except:
        print("Could not read from given port")
        return None