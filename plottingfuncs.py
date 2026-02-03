import pandas as pd
import matplotlib.pyplot as plt
import TempCal

def plot_phase_sweep(csv_filename):
    try:
        # Load the data
        df = pd.read_csv(csv_filename)
        res = sum(df['Resistance_Ohm']) / len(df)
        temperature = TempCal.res_to_temp_K(res)
        # Verify columns exist to prevent KeyError
        if 'Phase_Deg' not in df.columns or 'Lockin_Output' not in df.columns:
            print("Error: CSV does not contain required columns 'Phase_Deg' and 'Lockin_Output'")
            return
        # Plot Phase (X) vs Lockin Output (Y)
        plt.plot(df['Phase_Deg'], df['Lockin_Output'], marker='o', 
                 linestyle='-', markersize=2, label='Lock-in Output')
        # Temperature annotation in a text box
        # Positioned at top-left (0.05, 0.95) in axis coordinates
        stats_text = f'$T = {temperature:.2f}\\ K$'
        plt.text(0.05, 0.95, stats_text, transform=plt.gca().transAxes, 
                 fontsize=12, verticalalignment='top', 
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        # Formatting
        plt.title('Phase Sweep: Output Voltage vs Phase Angle')
        plt.xlabel('Phase (Degrees)')
        plt.ylabel('Lock-in Output ($V$)')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.legend()
        # Save output
        plt.tight_layout()
        plt.savefig('phase_sweep_plot_non_sc.png')
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
    plot_phase_sweep('csv/phase_sweep_data_non_sc.csv')
    # timevsres('csv/temperature-resistance.csv', 'Time_vs_res.png')