from typing import Union
import serial

class PrologixBus:
    def __init__(self,device_file = '/dev/ttyUSB0',channel = -1):
        self.serial = serial.Serial(device_file, baudrate=115200, timeout=5)
        self.channel = -1
        # Pushed the prologix adapter to controller mode
        self.serial.write("++mode 1\r".encode())
        # Disables auto-read mode, can enable later on when needed
        self.serial.write("++auto 0\r".encode())
        # Asserts end of message line at end of each line
        self.serial.write("++eoi 1\r".encode())
        # Unset addresses
        self.DMM_addr = -1
        self.FG_addr = -1
        self.lockin_addr = -1

    def SendCommand(self,addr : int,command : str) -> None:
        if(self.channel != addr):
            addrstr = "++addr" + str(addr) + "\r"
            self.serial.write(addrstr.encode())
        cmdstr = command + "\r"
        self.serial.write(cmdstr.encode())

    def ReadSingle(self, addr : int) -> str:
        if(self.channel != addr):
            addrstr = "++addr" + str(addr) + "\r"
            self.serial.write(addrstr.encode())
        self.serial.write("++read eoi\r".encode())
        return self.serial.readline()


def DMM_ID(pbus : PrologixBus) -> None:
    pbus.SendCommand(pbus.DMM_addr,"*IDN?")
    print(pbus.ReadSingle(pbus.DMM_addr).strip())

def FG_ID(pbus : PrologixBus) -> None:
    pbus.SendCommand(pbus.FG_addr,"*IDN?")
    print(pbus.ReadSingle(pbus.FG_addr).strip())

def lockin_ID(pbus : PrologixBus) -> None:
    print("The ID command for lockin does not seem to work but it is connected at address:"+str(pbus.lockin_addr))

def meas4W(pbus : PrologixBus) -> float:
    pbus.SendCommand(pbus.DMM_addr,"MEAS:FRES?")
    return float(pbus.ReadSingle(pbus.DMM_addr).strip())

if __name__ == "__main__":
    pbus = PrologixBus()
    pbus.DMM_addr = 20
    pbus.lockin_addr = 23
    pbus.SendCommand(23,"Q")
    print(pbus.ReadSingle(23).strip())
    for i in range(1,100):
        pbus.SendCommand(23,"Q")
        print(pbus.ReadSingle(23).strip())
        print(meas4W)


    