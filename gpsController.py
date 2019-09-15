def parseGPSData(data, lastValues):
    data = data[2:-5].split(",")
    opCode = data[0]
    mutatedData = []
    if opCode == "$GPVTG":
        mutatedData = parseSpeed(data)
        lastValues["lastSpeed"].append(mutatedData[-1])
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
    if(data[1] != ""):
        speed.append(data[-3])
    else:
        speed.append(0)
    return speed

#KONUM BILGISI
def parseCoordinates(data):
    # ['$GPGLL', '4044.62697', 'N', '02947.11831', 'E', '090520.00', 'A', 'A*6D']
    dataToSend = []
    if data[1] == "":
        dataToSend.append(str(0))
    else:
        first = str(float(data[1])/100) # 40.4462697
        second = first.split(".")
        third = float(second[1][:2] + "." + second[1][2:])
        fourth = third/60
        last = str(second[0])+ str(fourth)[1:]
        dataToSend.append(last)

    if data[3] == "":
        dataToSend.append(str(0))
    else:
        first = str(float(data[3])/100) # 40.4462697
        second = first.split(".")
        third = float(second[1][:2] + "." + second[1][2:])
        fourth = third/60
        last = str(second[0])+ str(fourth)[1:]
        dataToSend.append(last)

    return dataToSend