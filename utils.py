import settings as st

def parseBatteryData(data):
    data = data[3:-6].split(",")
    sid = data[0]
    opCode = data[1]

    if opCode in st.batteryOPCodes["Temps"]:
        print(parseTemp(data[3:]))
    elif opCode in st.batteryOPCodes["AmpsAndStatus"]:
        print(parseAmpSystem(data[3:]))
    else:
        print("Baba aküyü çalmışlar")
    """elif opCode in st.batteryOPCodes["Temps"]:
    elif opCode in st.batteryOPCodes["AmpsAndStatus"]:
    elif opCode in st.batteryOPCodes["MinMaxCells"]:"""

def parseAmpSystem(data):
    newData = []
    newData.append(float(data[0]) / 100.0)
    #lblGuc.Text = Convert.ToInt32(Convert.ToDouble(lblToplamGerilim.Text) * num).ToString() + " Watt";
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
    newData = []
    for value in data:
        if value != "---":
            newData.append(float(value) / 10.0)
        else:
            newData.append(value)
    return newData