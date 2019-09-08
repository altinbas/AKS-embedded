import serialPort as sp
import utils
import settings
import logger as lg
import lcdController

lastValues = {
    "lastPercentages": [[50],[50],[50]],
    "lastAmps": [],
    "lastTemps": [[0],[0],[0]],
    "lastWatts": [],
    "lastVoltages": [[0],[0],[0]]
}

portList = sp.getAllPorts()
openPorts = sp.openPorts(portList)
try:
    lcdController.lcd_init()
except:
    print("Cannot initiate LCD")
print(openPorts)
while 1:
    try:
        line = None
        if settings.isProduction:
            line = sp.readFromPort(openPorts["Battery"])
        else:
            line = sp.readFromPort(openPorts["Generic"])
        if line != b'':
            print(str(line))

            parsed = utils.parseBatteryData(str(line), lastValues)
            lg.logging(parsed)
            packData = utils.packData(parsed)
            if len(packData) > 0:
                #lcdController.lcd_string("MAYMUNCUK      <",0x80)
                line1 = "%:{}    T:{}".format(lastValues["lastPercentages"][0][-1], lastValues["lastTemps"][0][-1])
                line2 = "A:{} V:{}".format(lastValues["lastAmps"][-1], lastValues["lastVoltages"][0][-1])
                lcdController.lcd_string(str(line1), 0x80)
                lcdController.lcd_string(str(line2), 0xC0)
                for data in packData:
                    print(data)
                    sp.writeToPort(openPorts["XBee"], data.encode())
    except:
        print("Error occured while trying to read from port: ")

sp.closePorts(openPorts)
print(openPorts)