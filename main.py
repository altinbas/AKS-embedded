import serialPort as sp
import utils
import settings
import logger as lg
import lcdController
import gpsController

lastValues = {
    "lastPercentages": [[50],[50],[50]],
    "lastAmps": [],
    "lastTemps": [[0],[0],[0]],
    "lastWatts": [],
    "lastVoltages": [[0],[0],[0]],
    "lastLocation": [[0.0],[0.0]],
    "lastSpeed": [0]
}

portList = sp.getAllPorts()
print(portList)
openPorts = sp.openPorts(portList)
try:
    lcdController.lcd_init()
except:
    print("Cannot initiate LCD")
print(openPorts)
while 1:
    try:
        line = None
        gps = None
        if settings.isProduction:
            line = sp.readFromPort(openPorts["Battery"])
            gps = sp.readFromPort(openPorts["Generic"])
        else:
            gps = sp.readFromPort(openPorts["Generic"])
        if line != b'' and line != None:
            print(str(line))
            parsed = utils.parseBatteryData(str(line), lastValues)
            lg.logging(parsed)
            packData = utils.packData(parsed)
            if len(packData) > 0:
                for data in packData:
                    print(data)
                    sp.writeToPort(openPorts["XBee"], data.encode())
        if gps != b'':
            parsed = gpsController.parseGPSData(str(gps), lastValues)
            print(parsed)
            packData = utils.packData(parsed)
            if len(packData) > 0:
                try:
                    #lcdController.lcd_string("MAYMUNCUK      <",0x80)
                    line1 = "%:{}    T:{}".format(lastValues["lastPercentages"][0][-1], lastValues["lastTemps"][0][-1])
                    line2 = "A:{} S:{}".format(lastValues["lastAmps"][-1], lastValues["speed"][-1])
                    lcdController.lcd_string(str(line1), 0x80)
                    lcdController.lcd_string(str(line2), 0xC0)
                except:
                    print("Cannot communicate with the LCD")
                for data in packData:
                    print(data)
                    sp.writeToPort(openPorts["XBee"], data.encode())
    except:
        print("Error occured while trying to read from port: ")

sp.closePorts(openPorts)
print(openPorts)