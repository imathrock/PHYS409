import GPIB, time, csv

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