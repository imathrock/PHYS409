from typing import Union
import serial, time, csv


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
            self.channel = addr
            addrstr = "++addr" + str(addr) + "\r"
            self.serial.write(addrstr.encode())
        cmdstr = command + "\r"
        self.serial.write(cmdstr.encode())

    def ReadSingle(self, addr : int) -> str:
        if(self.channel != addr):
            self.channel = addr
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

def lockin_outp(pbus : PrologixBus) -> float:
    pbus.SendCommand(pbus.lockin_addr,"Q")
    return pbus.ReadSingle(pbus.lockin_addr).strip()

def lockin_change_phase(pbus : PrologixBus, i : int) -> None:
    pbus.SendCommand(pbus.lockin_addr,("P"+str(i)))


if __name__ == "__main__":
    pbus = PrologixBus()
    pbus.DMM_addr = 20
    #config DMM
    pbus.SendCommand(pbus.DMM_addr,"MEAS:FRES? 10000, 001")

    data_buffer = []
    print("Starting measurement loop...")
    start_time = time.time()
    for i in range(0,7500):
        current_time = time.time() - start_time
        resistance = meas4W
        data_buffer.append([current_time,resistance])
        print(f"Recorded: Time={current_time:.2f}s, R={resistance}")
        time.sleep(0.1)

    with open('temperature-resistance.csv', mode='w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Ohms'])
        writer.writerows(data_buffer)


    # # Define filename
    # csv_file = "phase_sweep_data.csv"

    # # Open file context
    # with open(csv_file, mode='w', newline='') as f:
    #     writer = csv.writer(f)
    #     # Write Header
    #     writer.writerow(["Phase_Deg", "Lockin_Output", "Resistance_Ohm"])
        
    #     print(f"Starting sweep. Data saving to {csv_file}...")

    #     for i in range(1, 360):
    #         lockin_change_phase(pbus, i)
    #         time.sleep(0.1) 
    #         # Capture data
    #         # decode() is added to ensure we write strings, not bytes, to the CSV
    #         raw_lockin = lockin_outp(pbus)
    #         lockin_val = raw_lockin.decode('utf-8') if isinstance(raw_lockin, bytes) else raw_lockin
    #         resistance_val = meas4W(pbus)
    #         # Write row to CSV
    #         writer.writerow([i, lockin_val, resistance_val])
    #         # Flush buffer to ensure data is saved even if script crashes
    #         f.flush()
    #         # Print to console (using f-string to prevent TypeError)
    #         print(f"Phase: {i} | Lockin: {lockin_val} | Resistance: {resistance_val}")
    
