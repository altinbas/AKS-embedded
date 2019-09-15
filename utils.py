import settings as st

def parseBatteryData(data, lastValues):
    ''' Parse the given battery data with the corresponding OPcode,
        then add the calculated values into a limited list so that
        we can calculate the averages over a time period.
        data: data received from the battery
        lastValues: a reference to lastValues dictionary. '''
    # Check the development status, shape of data changes according to the status
    if st.isProduction:
        data = data[3:-10].split(",")
    else:
        data = data[3:-6].split(",")

    # SIDs starts from 1000, modify the ids so that they start from 0.
    # With this method, we can use them in lists to point out the
    # corresponding list
    sid = int(data[0]) - 1000
    opCode = data[1]

    mutatedData = None
    if opCode in st.batteryOPCodes["Temps"]:
        # Parse the obtained temperature data,
        # Output schema looks like [TEMP, TEMP],
        # TEMP could be 0.0, "---" or a correct temp.
        mutatedData = parseTemp(data[3:])
        for temp in mutatedData:
            # Iterate over all items, discard the 0.0 and "---" items.
            if type(temp) == type(0.0) and temp != 0.0:
                # add the item to the log list, if list is not populated enough.
                if len(lastValues["lastTemps"][sid]) < st.listLengths:
                    lastValues["lastTemps"][sid].append(float(temp))
                else:
                    # Detele the first item then add the net value if list is overpopulated.
                    del(lastValues["lastTemps"][sid][0])
                    lastValues["lastTemps"][sid].append(float(temp))

    elif opCode in st.batteryOPCodes["AmpsAndStatus"]:
        # Parse the obtained current and system status,
        # Output schema looks like [AMPS, STATUS TEXT],
        # AMPS is a signed float
        mutatedData = parseAmpSystem(data[3:])
        if len(lastValues["lastAmps"]) < st.listLengths:
            lastValues["lastAmps"].append(float(mutatedData[0]))
        else:
            del(lastValues["lastAmps"][0])
            lastValues["lastAmps"].append(float(mutatedData[0]))
        if len(lastValues["lastWatts"]) < st.listLengths:
            lastValues["lastWatts"].append(float(mutatedData[0] * lastValues["lastVoltages"][2][-1]))
        else:
            del(lastValues["lastWatts"][0])
            lastValues["lastWatts"].append(float(mutatedData[0] * lastValues["lastVoltages"][2][-1]))

    elif opCode in st.batteryOPCodes["Voltages"]:
        # Parse the obtained voltage and percentage data,
        # Output schema looks like:
        # [MinV, MaxV, VDifference, TotalV, Counter *Ignore*, MaxBatteryV, NomBatteryV, MinBatteryV, Percentage],
        mutatedData = parseVoltage(data[3:])
        if len(lastValues["lastPercentages"][sid]) < st.listLengths:
            lastValues["lastPercentages"][sid].append(float(mutatedData[-1][:4]))
        else:
            # Detele the first item then add the net value if list is overpopulated.
            del(lastValues["lastPercentages"][sid][0])
            lastValues["lastPercentages"][sid].append(float(mutatedData[-1][:4]))

        if len(lastValues["lastVoltages"][sid]) < st.listLengths:
            lastValues["lastVoltages"][sid].append(float(mutatedData[3]))
        else:
            # Detele the first item then add the net value if list is overpopulated.
            del(lastValues["lastVoltages"][sid][0])
            lastValues["lastVoltages"][sid].append(float(mutatedData[3]))
    elif opCode in st.batteryOPCodes["MinMaxCells"]:
        mutatedData = parseMinMaxCells(data[3:])
    else:
        mutatedData = ["Baba aküyü çalmışlar"]

    mutatedData.insert(0, sid)
    mutatedData.insert(1, opCode)
    return mutatedData

def parseAmpSystem(data):
    ''' Parse the given Amps and System status from the given data'''
    # Initiate an empty list for new values.
    newData = []
    # Append the mutated amps to the new list.
    newData.append(float(data[0]) / 100.0)
    # Append the corresponding system status text to the list.
    if (data[1] == "0"):
        newData.append("Sistem Normal")
    elif (data[1] == "1"):
        newData.append("Aşırı Deşarj Akımı")
    elif (data[1] == "2"):
        newData.append("Aşırı Şarj Akımı")
    elif (data[1] == "3"):
        newData.append("Yüksek Hücre Gerilimi")
    elif (data[1] == "4"):
        newData.append("Düşük Hücre Gerilimi")
    elif (data[1] == "5"):
        newData.append("Yüksek Sıcaklık")
    return newData

def parseTemp(data):
    ''' Parse the temperature from the given data '''
    newData = []
    # Iterate over each given data then convert the data to proper temperature value.
    for value in data:
        if value != "---" and value != "0.0":
            newData.append(float(value) / 10.0)
    return newData

def parseVoltage(data):
    #newData = []
    minMaxValues = []
    try:
        #for value in data:
            #newData.append(value)
        min_Voltage = 4200
        max_Voltage = 0
        counter = 0
        total_Voltage = 0.0
        BMS_Sayisi = 5  #already defined in somewhere else
        for i in range(BMS_Sayisi):
            for value in data:
                if value != "----":
                    current_value = int(value)
                    if (current_value < min_Voltage):
                        min_Voltage = current_value #takes the smallest value in data
                    if (current_value > max_Voltage):
                        max_Voltage = current_value #takes the highest value in data
                    counter = counter + 1 #counter
                    total_Voltage += float(current_value) #sums all voltage values in data
        minMaxValues.append(str(min_Voltage)) #gerilim min
        minMaxValues.append(str(max_Voltage))#gerilim max
        minMaxValues.append(str(max_Voltage - min_Voltage)) #gerilim fark
        minMaxValues.append(str(total_Voltage / 1000.0)) #toplam gerilim
        seriHucreSayisi = counter
        minMaxValues.append(str(seriHucreSayisi))
        minMaxValues.append(str(float(4200) * (float(counter) / 1000.0))) #max batarya gerilimi
        minMaxValues.append(str(float(3700) * (float(counter) / 1000.0))) #txbNomBataryaGerilimi
        minMaxValues.append(str(float(2800) * (float(counter) / 1000.0)))#min batarya gerilimi

        maxBataryaGerilimi = float(minMaxValues[5]) #txbMaxBataryaGerilimi
        minBataryaGerilimi = float(minMaxValues[7]) #txbMinBataryaGerilimi
        totalVoltage= float(total_Voltage / 1000.0)
        if totalVoltage > minBataryaGerilimi:
            totalVoltage -= minBataryaGerilimi
            maxBataryaGerilimi -= minBataryaGerilimi
            voltagePercentage = float(100.0 * totalVoltage / maxBataryaGerilimi)

            minMaxValues.append(str(voltagePercentage)) #+ " %"
        else:
            minMaxValues.append("0") # % voltage percentage
    except:
        pass

    return minMaxValues
    # 1. min gerilim 2.max gerilim 3. gerilim farkı
    # 4.toplam gerilim 5. counter 6.max batarya gerilimi
    # 7. nom batarya gerilimi 8. min batarya gerilimi 9.VOLTAGE PERCENTAGE

def parseMinMaxCells(data):
    return data

def packData(data):
    packed = []
    opCode = None
    if len(data) > 1:
        opCode = data[1]
    if opCode == "21":
        packed.append(packBatteryLevel(data))
        packed.append(maxV(data))
        packed.append(minV(data))
        packed.append(differenceV(data))
    elif opCode == "24":
        packed.append(packCurrent(data))
    elif opCode == "22":
        packed.append(packTemp(data))
    elif data[0] == "$GPVTG":
        packed.append(packSpeed(data))
    elif data[0] == "$GPGLL":
        packed.append(packCoordinates(data, 0))
        packed.append(packCoordinates(data, 1))

    return packed

def packBatteryLevel(data):
    return "{}:{}*".format(st.ids["batteryLevel"], data[-1][:4])

def packCurrent(data):
    return "{}:{}*".format(st.ids["current"], data[2])

def packTemp(data):
    return "{}:{}*".format(st.ids["temps"][data[0]], data[2])

def maxV(data):
    return "{}:{}*".format(st.ids["maxV"][data[0]], data[3])

def minV(data):
    return "{}:{}*".format(st.ids["minV"][data[0]], data[2])

def differenceV(data):
    return "{}:{}*".format(st.ids["differenceV"][data[0]], data[4])

def packSpeed(data):
    return "{}:{}*".format(st.ids["speed"], data[1])

def packCoordinates(data, i):
    if i == 0:
        return "{}:{}*".format(st.ids["coordinates"][0], data[1])
    else:
        return "{}:{}*".format(st.ids["coordinates"][1], data[2])