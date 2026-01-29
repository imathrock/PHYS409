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

def timevsres(csv_filename, save_path):
    df = pd.read_csv(csv_filename)
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time'],df['Ohms'], marker='o', linestyle='-', markersize=2, label='resistance vs time')
    plt.title('Caliberation of room temp to liquid nitrogen ')
    plt.xlabel('Time')
    plt.ylabel('4 wire resistance')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    if save_path:
        plt.savefig(save_path, dpi=300) # dpi=300 ensures high resolution
        print(f"Plot saved to {save_path}")
    plt.show()


if __name__ == "__main__":
    # plot_phase_sweep('csv/phase_sweep_data.csv')
    timevsres('csv/temperature-resistance.csv', 'Time_vs_res.png')