import serial

class dmm():
    def __init__(self, device_file = '/dev/ttyUSB0', channel = 20):
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

    def DMMConfig(self, type, mode, range, res):
        type = type.upper()
        mode = mode.upper()
        if type not in ['VOLT', 'CURR', 'RES']:
            raise ValueError("Measurement type must be set to 'VOLT', 'CURR', 'RES'")
        if type != 'RES' and mode not in ['DC', 'AC']:
            raise ValueError("mode must be 'DC' or 'AC' for VOLT or CURR")
        cmd = 'CONF:'
        if type == 'RES':
            cmd+=type
        else:
            cmd+=f'{type}:{mode}'
        if range is not none:
            cmd+= f'{range}'
            if res is not none:
                cmd+=f',{res}'
        print("Configuration of DMM is :",cmd)
        self.SendCommand(cmd)
    
    def id(self):
        self.SendCommand("*IDN?")
        print(self.ReadSingle())

class fg():
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

    def ON(self):
        self.SendCommand("OUTP ON")
    def OFF(self):
        self.SendCommand("OUTP OFF")

    def FGConfig(self,wave,freq,ampl,offset,load = 'INF'):
        wave = wave.upper()
        OFF()
        self.SendCommand(f"FUNC {wave}")
        if freq is not none:
            self.SendCommand(f"FREQ {freq}")
        if ampl is not none:
            self.SendCommand(f"VOLT {ampl}")
        if offset is not none:
            self.SendCommand(f"VOLT:OFFS {offset}")
        self.SendCommand(f"OUTP:LOAD {load}")

    def change_freq(self, freq):
        OFF()
        self.SendCommand(f"FREQ {freq}")
        time.sleep(0.1)
        ON()

    def id(self):
        self.SendCommand("*IDN?")
        print(self.ReadSingle())


dmm = dmm("/dev/ttyUSB0", channel=21)  # HP 34401A
dmm.SendCommand("*IDN?")
print(dmm.ReadSingle().decode().strip())
dmm.SendCommand("CONF:VOLT:DC 1,0.0001")
while(1):
    dmm.SendCommand("READ?")                  # trigger measurement
    value = dmm.ReadSingle()                  # read ASCII result
    print(float(value.decode().strip()))