import serial, time, csv

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

    def config(self, type, mode, range, res):
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
        if range is not None:
            cmd+= f'{range}'
            if res is not None:
                cmd+=f',{res}'
        print("Configuration of DMM is :",cmd)
        self.SendCommand(cmd)
    
    def id(self):
        self.SendCommand("*IDN?")
        print(self.ReadSingle())


class fg():
    def __init__(self, device_file = '/dev/ttyUSB0', channel = 19):
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

    def config(self, wave, freq, ampl, offset = 0.0, load = 'INF'):
        self.reset()
        if not isinstance(wave,str):
            raise TypeError("Wave must be one of : 'SIN', 'SQU', 'TRI', 'RAMP'")
        if freq is None:
            raise TypeError("Frequency can't be None")
        if not isinstance(freq, (int,float)):
            raise TypeError("Frequency is of incorrect type, It must be float or int")
        if not isinstance(ampl, (int,float)):
            raise TypeError("Amplitude is of incorrect type, It must be float")
        if not isinstance(offset, (int, float)):
            raise TypeError("offset must be numeric")


        wave = wave.upper()
        wavetypes = {'SIN', 'SQU', 'TRI', 'RAMP'}
        if wave not in wavetypes:
            raise ValueError(f"Invalid waveform {wave}.\n Wave must be one of : 'SIN', 'SQU', 'TRI', RAMP")
        
        if freq < 0:
            raise ValueError("Frequency can't be negative")
        elif freq > 10e6:
            raise ValueError("Frequency exceeds machine limits of 10 MHz")
        
        if ampl > 10.0:
            raise ValueError("Amplitude exceeds machine limit of 10.0 Volts")
        elif ampl < 0.05:
            raise ValueError("Amplitude must be > 50 mV")

        if abs(offset) + ampl / 2 > 10:
            raise ValueError("offset + Vpp/2 exceeds output compliance")        
            
        self.SendCommand(f"FUNC {wave}")
        self.SendCommand(f"FREQ {freq}")
        self.SendCommand(f"VOLT {ampl} VPP")
        self.SendCommand(f"VOLT:OFFS {offset}")
        self.SendCommand(f"OUTP:LOAD {load}")

        print(f"Configuration Sent: Wave={wave}, Freq={freq}, Ampl={ampl}, Offset={offset}, Load={load}")

    def reset(self):
        self.SendCommand("*RST")

    def change_freq(self, freq):
        self.OFF()
        self.SendCommand(f"FREQ {freq}")
        time.sleep(0.1)
        self.ON()

    def id(self):
        self.SendCommand("*IDN?")
        print(self.ReadSingle())

class lockin():
    def __init__(self, device_file = '/dev/ttyUSB0', channel = 23):
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

if __name__ == "__main__":
    dmm = dmm()
    dmm.id()
    dmm.config("RES",None,10000,0.01)
    with open('temp.csv', mode='w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Ohms'])
        print("Starting measurement loop...")
        start_time = time.time()
        for i in range(100):
            current_time = time.time() - start_time
            resistance = dmm.ReadSingle()
            writer.writerow([current_time, resistance])
            file.flush()
            print(f"Recorded: Time={current_time:.2f}s, R={resistance:.3f}")
            time.sleep(0.5)


