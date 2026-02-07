import GPIB, time, csv

def res_to_temp_K(resistance):
    return -0.5137484328065629*resistance+611.2006356099807

def sweep_phase(pbus,csv_file):
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Phase_Deg", "Lockin_Output", "Resistance_Ohm"])
        print(f"Starting sweep. Data saving to {csv_file}...")
        for i in range(1, 360):
            GPIB.lockin_change_phase(pbus, i)
            time.sleep(0.5) 
            raw_lockin = GPIB.lockin_outp(pbus)
            lockin_val = raw_lockin.decode('utf-8') if isinstance(raw_lockin, bytes) else raw_lockin
            resistance_val = GPIB.meas4W(pbus)
            writer.writerow([i, lockin_val, resistance_val])
            f.flush()
            print(f"Phase: {i} | Lockin: {lockin_val} | Resistance: {resistance_val}")

def find_peak_phase(pbus):
    max_phase = 0
    max_val = -1.0
    for i in range(1, 360):
        GPIB.lockin_change_phase(pbus, i)
        time.sleep(0.5)
        raw_lockin = GPIB.lockin_outp(pbus)
        lockin_val = raw_lockin.decode('utf-8') if isinstance(raw_lockin, bytes) else raw_lockin
        if(abs(lockin_val) > max_val):
            max_val = abs(lockin_val)
            max_phase = i
    return max_phase
    
def lockin_vs_temp(pbus,csv_file : str, num_points : int, lockin_phase : int):
    GPIB.lockin_change_phase(pbus, lockin_phase)
    with open(csv_file, mode='w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["lockin","Temp"])
        for i in range(1,num_points):
            time.sleep(0.2) 
            raw_lockin = GPIB.lockin_outp(pbus)
            lockin_val = raw_lockin.decode('utf-8') if isinstance(raw_lockin, bytes) else raw_lockin
            resistance_val = GPIB.meas4W(pbus)
            temperature = res_to_temp_K(resistance=resistance_val)
            writer.writerow([lockin_val, temperature])
            f.flush()
            print(f"entry no: {i} | Lockin: {lockin_val} | Temperature: {temperature}")



if __name__ == "__main__":
    pbus = GPIB.init()
    peak_phase = find_peak_phase(pbus)
    lockin_vs_temp(pbus=pbus,csv_file="1kHz_temp_vs_lockin.csv",num_points=700,lockin_phase=peak_phase)

