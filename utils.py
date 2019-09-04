def parseBatteryData(data):
    parsedData = str(data)
    print(parsedData[2:-4])

def parseTemp(data):
    list = []
    new = data.replace("[", "").replace("]", "").replace("*", "")[:-3]
    datalist = new.split(',')[3:]
    for data in datalist:
        list.append(data[:2] + "," + data[2:])
    return list