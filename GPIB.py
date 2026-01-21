import serial

#class agilent(GPIB):
    """
    Manage analogue input from the DAQ board.
    """
#    def __init__(self, channel=21, device_file="/dev/ttyUSB0"):
#        GPIB.__init__(self, device_file, channel)
#        self.Commandlist = {"Frequency":"FREQ", "Amplitude":"AMPL", "Waveform":"WAVE", "Amplitude":"AMPLT", "DC Offset":"DCOFFS"}

#    def Query(self, command):
#        if command in  self.Commandlist:
#            self.SendCommand(self.Commandlist[command]+"?")
#            return self.ReadSingle()

#    def Command(self, command, value):
#        if command in  self.Commandlist:
#            self.SendCommand(self.Commandlist[command] + " " + str(value))

class GPIB:
    def __init__(self, device_file='/dev/ttyUSB0', channel=21):
        self.ser = serial.Serial(device_file, timeout = 3)
        self.ser.flushOutput()
        self.ser.flushInput()
        self.ser.write("++mode 1\r".encode())
        self.ser.write("++auto 0\r".encode())
        self.ser.write("++eoi 1\r".encode())
        self.channel = -1
        self._change_channel(channel)

    def _change_channel (self, channel):
        if (channel != self.channel):
            #Clean up the input and output
            self.channel=channel
            addr_string = "++addr "+str(self.channel)+"\r"
            self.ser.write (addr_string.encode())
            self.ser.flushOutput()
            self.ser.flushInput()


    def SendCommand(self, commandString):
        command_str = commandString + "\r"
        self.ser.write(command_str.encode())

    def ReadSingle(self):
        self.ser.write("++read eoi\r".encode())
        value = self.ser.readline()
        self.ser.flushInput()
        self.ser.flushOutput()
        return value


class DMM:
    """
    Control HP 34401A Digital Multimeter via RS-232 (SCPI).
    """

    CONFIG = {
        "VDC": "CONF:VOLT:DC",
        "VAC": "CONF:VOLT:AC",
        "IDC": "CONF:CURR:DC",
        "IAC": "CONF:CURR:AC",
        "RES": "CONF:RES",
        "FRES": "CONF:FRES",
    }

    def __init__(
        self,
        port="/dev/ttyUSB0",
        baudrate=9600,
        timeout=1,
    ):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout,
        )
        self.clear()

    def clear(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def send(self, cmd):
        self.ser.write((cmd + "\n").encode("ascii"))

    def query(self, cmd):
        self.send(cmd + "?")
        return self.ser.readline().decode("ascii").strip()

    # -------------------------------
    # Identification
    # -------------------------------

    def identify(self):
        return self.query("*IDN")

    # -------------------------------
    # Configuration
    # -------------------------------

    def configure(self, mode, range_val=None, resolution=None):
        """
        mode: VDC, VAC, IDC, IAC, RES, FRES
        """
        if mode not in self.CONFIG:
            raise ValueError("Invalid configuration mode")

        cmd = self.CONFIG[mode]

        if range_val is not None:
            cmd += f" {range_val}"
            if resolution is not None:
                cmd += f", {resolution}"

        self.send(cmd)

    # -------------------------------
    # Measurements
    # -------------------------------

    def read(self):
        self.send("READ?")
        return float(self.ser.readline().decode("ascii").strip())

    def fetch(self):
        self.send("FETC?")
        return float(self.ser.readline().decode("ascii").strip())


    def measure(self, mode):
        if mode not in self.CONFIG:
            raise ValueError("Invalid measurement mode")
        return float(self.query(f"MEAS:{self.CONFIG[mode].split(':')[1]}"))

    # -------------------------------
    # Utility
    # -------------------------------

    def reset(self):
        self.send("*RST")

    def close(self):
        self.ser.close()

class agilent:
    """
    Control Agilent 33120A Function Generator via RS-232 (SCPI).
    """

    SCPI = {
        "frequency": "FREQ",
        "amplitude": "VOLT",
        "offset": "VOLT:OFFS",
        "waveform": "FUNC",
        "output": "OUTP",
    }

    def __init__(
        self,
        port="/dev/ttyUSB0",
        baudrate=9600,
        timeout=1,
    ):
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout,
        )
        self.clear()

    def clear(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def send(self, cmd):
        full_cmd = cmd + "\n"
        self.ser.write(full_cmd.encode("ascii"))

    def query(self, cmd):
        self.send(cmd + "?")
        return self.ser.readline().decode("ascii").strip()

    # -------------------------------
    # High-level parameter setters
    # -------------------------------

    def set_frequency(self, hz):
        self.send(f"{self.SCPI['frequency']} {hz}")

    def get_frequency(self):
        return self.query(self.SCPI["frequency"])

    def set_amplitude(self, volts_pp):
        self.send(f"{self.SCPI['amplitude']} {volts_pp}")

    def get_amplitude(self):
        return self.query(self.SCPI["amplitude"])

    def set_offset(self, volts):
        self.send(f"{self.SCPI['offset']} {volts}")

    def get_offset(self):
        return self.query(self.SCPI["offset"])

    def set_waveform(self, waveform):
        waveform = waveform.upper()
        valid = {"SIN", "SQU", "RAMP", "PULS", "NOIS", "DC"}
        if waveform not in valid:
            raise ValueError(f"Invalid waveform: {waveform}")
        self.send(f"{self.SCPI['waveform']} {waveform}")

    def get_waveform(self):
        return self.query(self.SCPI["waveform"])

    def output_on(self):
        self.send("OUTP ON")

    def output_off(self):
        self.send("OUTP OFF")

    def identify(self):
        return self.query("*IDN")

    def close(self):
        self.ser.close()

def test():
    dmm = DMM("/dev/ttyUSB0")

    print(dmm.identify())

    dmm.configure("VDC", range_val=10, resolution=1e-6)
    value = dmm.read()
    print(value)

    dmm.close()

if __name__ == "__main__":
    test()