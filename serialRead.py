import sys
import glob
import serial

s = []

def availableSerialPorts():
    if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print(result)
    return result


def openSerial():
    global s
    ports = availableSerialPorts()
    for port in ports:

        if port.find("USB") > 0:
            print(port.find("USB"))
            s.append(serial.Serial(port, baudrate=38400, timeout = 0.1))
            print("Serial connection establised with port " + port)

openSerial()
print(s)

while 1:
    serial_line = None
    for port in s:
        if "USB1" in port.name:
            serial_line = port.readline()

        if serial_line != b'':
            print(port.name + ": " + str(serial_line))
            #ser.write(cmd.encode('ascii')+'\r\n')
            if "USB0" in port.name:
                #port.write("{}{}".format(serial_line,"\r\n").encode("ascii"))
                port.write(serial_line)