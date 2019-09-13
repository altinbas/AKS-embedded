import serialPort as sp

portList = sp.getAllPorts()
openPorts = sp.openPorts(portList)

while True:
    try:
        line = sp.readFromPort(openPorts["Generic"])
        if line != b'':
            line2 = str(line)[2:-5]
            lineList = line2.split(",")
            if lineList[0] == "$GPGLL":
                print(lineList)
                l1=float(lineList[1])
                l2=float(lineList[3])
                if l1>4100 and l2>2840:
                    print("hala oçun evini gösteriyo")

    except:
        print("Error occured while trying to read from port: ")

sp.closePorts(openPorts)
print(openPorts)