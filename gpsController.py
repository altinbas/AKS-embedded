def parseGPSData(data, lastValues):
    data = data[2:-5].split(",")
    opCode = data[0]
    mutatedData = []
    if opCode == "$GPVTG":
        mutatedData = parseSpeed(data)
        lastValues["lastSpeed"].append(mutatedData[-1])
        print(mutatedData)
    elif opCode == "$GPGLL":
        mutatedData = parseCoordinates(data)
        if mutatedData[0] != "0":
            lastValues["lastLocation"][0].append(mutatedData[0])
            lastValues["lastLocation"][1].append(mutatedData[1])
    mutatedData.insert(0, opCode)
    return mutatedData

#HIZ VERISI
def parseSpeed(data):
    speed = []
    if data[-3] == "":
        speed.append(0)
    else:
        speed.append(data[-3])
    return speed

#KONUM BILGISI
def parseCoordinates(data):
    dataToSend = []
    if data[1] == "":
        dataToSend.append(str(0))
    else:
        dataToSend.append(str(float(data[1])/100)) #N or S
        dataToSend.append(data[2])

    if data[3] == "":
        dataToSend.append(str(0))
    else:
        dataToSend.append(str(float(data[3])/100)) #W or E
        dataToSend.append(data[4])
    return dataToSend