import sys
from time import gmtime, strftime
from datetime import datetime





def logging(datapack):
    today=datetime.now()
    with open('logs.txt', 'a', encoding='utf-8') as file:
        file.write("{}--{}\n".format(datapack,today.strftime("%H:%M:%S.%f")[:-3]))
        file.close()
