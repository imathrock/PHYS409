import serial

class dmm():
    def __init__(self, device_file = '/dev/ttyUSB0', channel = 21):
        # begin serial 
        self.ser = serial.Serial(device_file,timeout=3)
        # Clear any pending buffers
        self.ser.flushOutput()
        self.ser.flushInput()
        # Pushed the prologix adapter to controller mode
        self.ser.write("++mode 1\r".encode())
        # Disables auto-read mode, can enable later on when needed
        self.ser.write("++auto 0\r".encode())
        # Asserts end of message line at end of each line
        self.ser.write("++eoi 1\r".encode())
        self.channel = channel
        addr_string = "++addr " + str(self.channel) + "\r"
        self.ser.write(addr_string.encode())
        self.ser.flushOutput()
        self.ser.flushInput()
    
    def SendCommand(self, command):
        cmdstr = command + "\r"
        self.ser.write(cmdstr.encode())
    
    def ReadSingle(self):
        self.ser.write("++read eoi\r".encode())
        value = self.ser.readline()
        self.ser.flushInput()
        self.ser.flushOutput()
        return value


dmm = dmm("/dev/ttyUSB0", channel=21)  # HP 34401A
dmm.SendCommand("*IDN?")
print(dmm.ReadSingle().decode().strip())