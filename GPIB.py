from typing import Union
import serial

class PrologixBus:
    def __init__(self,device_file = '/dev/ttyUSB0',channel = -1):
        self.serial = serial.Serial(device_file,115200,timeout=5)
        self.channel = -1
        # Pushed the prologix adapter to controller mode
        self.serial.write("++mode 1\r".encode())
        # Disables auto-read mode, can enable later on when needed
        self.serial.write("++auto 0\r".encode())
        # Asserts end of message line at end of each line
        self.serial.write("++eoi 1\r".encode())

    def SendCommand(self,addr,command):
        if(self.channel != addr):
            addrstr = "++addr" + str(addr) + "\r"
            self.serial.write(addrstr.encode())
        cmdstr = command + "\r"
        self.serial.write(cmdstr.encode())

    def ReadSingle(self, addr):
        if(self.channel != addr):
            addrstr = "++addr" + str(addr) + "\r"
            self.serial.write(addrstr.encode())
        self.serial.write("++read eoi\r".encode())
        return self.serial.readline()
    
if __name__ == "__main__":
    pbus = PrologixBus()
    pbus.SendCommand(19,"*IDN?")
    print(pbus.ReadSingle(19).strip())
    pbus.SendCommand(20,"*IDN?")
    print(pbus.ReadSingle(20).strip())
    pbus.SendCommand(23,"Q")
    print(pbus.ReadSingle(23).strip())
    for i in range(1,100):
        pbus.SendCommand(23,"Q")
        print(pbus.ReadSingle(23).strip())


    