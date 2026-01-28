import GPIB, time, csv

if __name__ == "__main__":
    pbus = GPIB.PrologixBus()
    pbus.DMM_addr = 20
    pbus.lockin_addr = 23
    
    # Define filename
    csv_file = "phase_sweep_data.csv"

    # Open file context
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        # Write Header
        writer.writerow(["Phase_Deg", "Lockin_Output", "Resistance_Ohm"])
        
        print(f"Starting sweep. Data saving to {csv_file}...")

        for i in range(1, 360):
            GPIB.lockin_change_phase(pbus, i)
            time.sleep(0.5) 
            # Capture data
            # decode() is added to ensure we write strings, not bytes, to the CSV
            raw_lockin = GPIB.lockin_outp(pbus)
            lockin_val = raw_lockin.decode('utf-8') if isinstance(raw_lockin, bytes) else raw_lockin
            resistance_val = GPIB.meas4W(pbus)
            # Write row to CSV
            writer.writerow([i, lockin_val, resistance_val])
            # Flush buffer to ensure data is saved even if script crashes
            f.flush()
            # Print to console (using f-string to prevent TypeError)
            print(f"Phase: {i} | Lockin: {lockin_val} | Resistance: {resistance_val}")