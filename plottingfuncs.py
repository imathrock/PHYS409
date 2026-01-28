import pandas as pd
import matplotlib.pyplot as plt

def plot_phase_sweep(csv_filename):
    try:
        # Load the data
        df = pd.read_csv(csv_filename)
        
        # verify columns exist to prevent KeyError
        if 'Phase_Deg' not in df.columns or 'Lockin_Output' not in df.columns:
            print("Error: CSV does not contain required columns 'Phase_Deg' and 'Lockin_Output'")
            return

        # Setup the plot
        plt.figure(figsize=(10, 6))
        
        # Plot Phase (X) vs Lockin Output (Y)
        plt.plot(df['Phase_Deg'], df['Lockin_Output'], marker='o', linestyle='-', markersize=2, label='Lock-in Output')
        
        # Formatting
        plt.title('Phase Sweep: Output Voltage vs Phase Angle')
        plt.xlabel('Phase (Degrees)')
        plt.ylabel('Lock-in Output (V)')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.legend()
        
        # Display
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{csv_filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    plot_phase_sweep('phase_sweep_data.csv')