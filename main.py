import serialPort as sp
import utils

portList = sp.getAllPorts()
openPorts = sp.openPorts(portList)
print(openPorts)
while 1:
    try:
        line = sp.readFromPort(openPorts["Generic"])
        if line != b'':
            print(str(line))
            utils.parseBatteryData(str(line))
            sp.writeToPort(openPorts["XBee"], line)
    except:
        print("Error occured while trying to read from port: " + str(openPorts["Generic"]))

sp.closePorts(openPorts)
print(openPorts)