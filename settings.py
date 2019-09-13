isProduction = False
usbTemplate = "/dev/{}"
BMSCount = 3
listLengths = 3

portSettings = {
    "baudrate": 38400,
    "gpsBaudrate": 9600,
    "timeout": 0.1
}

batteryOPCodes = {
    "Voltages": "21",
    "Temps": "22",
    "AmpsAndStatus": "24",
    "MinMaxCells": "26"
}

ids = {
    "batteryLevel": "100",
    "current": "110",
    "temps": [
        "120",
        "121",
        "122"
    ],
    "maxV": [
        "130",
        "131",
        "132"
    ],
    "minV": [
        "140",
        "141",
        "142"
    ],
    "differenceV": [
        "150",
        "151",
        "152"
    ],
    "coordinates": [
        "160",
        "161"
    ],
    "speed": "170"
}