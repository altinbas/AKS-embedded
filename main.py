import serialPort as sp
import utils
import settings

lastValues = {
    "lastPercentages": [[50],[50],[50]],
    "lastAmps": [],
    "lastTemps": [[0],[0],[0]],
    "lastWatts": [],
    "lastVoltages": [[0],[0],[0]]
}

portList = sp.getAllPorts()
openPorts = sp.openPorts(portList)
print(openPorts)
while 1:
    try:
        line = None
        if settings.isProduction == True:
            line = sp.readFromPort(openPorts["Battery"])
        else:
            line = sp.readFromPort(openPorts["Generic"])
        if line != b'':
            print(str(line))
            parsed = utils.parseBatteryData(str(line), lastValues)
            packData = utils.packData(parsed)
            if len(packData) > 0:
                for data in packData:
                    sp.writeToPort(openPorts["XBee"], data.encode())
    except:
        print("Error occured while trying to read from port: " + str(openPorts["Generic"]))

sp.closePorts(openPorts)
print(openPorts)