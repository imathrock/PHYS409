import GPIB, time, csv, TempCal

def sweep_phase():
    pbus = GPIB.PrologixBus()
    csv_file = "phase_sweep_data.csv"
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Phase_Deg", "Lockin_Output", "Resistance_Ohm"])
        print(f"Starting sweep. Data saving to {csv_file}...")
        for i in range(1, 400):
            GPIB.lockin_change_phase(pbus, i)
            time.sleep(0.5) 
            raw_lockin = GPIB.lockin_outp(pbus)
            lockin_val = raw_lockin.decode('utf-8') if isinstance(raw_lockin, bytes) else raw_lockin
            resistance_val = GPIB.meas4W(pbus)
            writer.writerow([i, lockin_val, resistance_val])
            f.flush()
            print(f"Phase: {i} | Lockin: {lockin_val} | Resistance: {resistance_val}")
    
def lockin_vs_temp():
    pbus = GPIB.PrologixBus()
    csv_file = "lockin_vs_temp.csv"
    with open(csv_file, mode='w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["lockin","Temp"])
        for i in range(1,2500):
            GPIB.lockin_change_phase(pbus, 90)
            time.sleep(0.5) 
            raw_lockin = GPIB.lockin_outp(pbus)
            lockin_val = raw_lockin.decode('utf-8') if isinstance(raw_lockin, bytes) else raw_lockin
            resistance_val = GPIB.meas4W(pbus)
            temperature = TempCal.res_to_temp_K(resistance=resistance_val)
            writer.writerow([lockin_val, temperature])
            f.flush()
            print(f"entry no: {i} | Lockin: {lockin_val} | Temperature: {temperature}")

if __name__ == "__main__":
    pass