import pandas as pd 
import matplotlib.pyplot as plt

# Load the dataframe
df = pd.read_csv('csv/temperature-resistance.csv')

room_temp = (21.1+21.7+21.6+21.6)/4+273.15 # K

high_temp_df = df.nsmallest(400, 'Ohms')
mean_res_ht = high_temp_df['Ohms'].mean()
std_res_ht = high_temp_df['Ohms'].std()

# print("================================")
# print(f"Mean Resistance: {mean_res_ht}")
# print(f"Standard Deviation: {std_res_ht}")
# print("================================")


liq_nit_temp = 77.4 #K

low_temp_df = df.nlargest(400, 'Ohms')
mean_res_lt = low_temp_df['Ohms'].mean()
std_res_lt = low_temp_df['Ohms'].std()

# print("================================")
# print(f"Mean Resistance: {mean_res_lt}")
# print(f"Standard Deviation: {std_res_lt}")
# print("================================")

slope = (room_temp-liq_nit_temp)/(mean_res_ht-mean_res_lt)
intercept = room_temp-(slope*mean_res_ht)

print(slope, intercept)

def res_to_temp_K(resistance):
    return slope*resistance+intercept

# print("Testing resistance function")
# print(str(res_to_temp_K(mean_res_ht)) + " " + str(room_temp))
# print(str(res_to_temp_K(mean_res_lt)) + " " + str(liq_nit_temp))