"""
This code takes the sample files of a Honri air particle counter and process it to see the evolution of the air cleanliness
per turn in the clean rooms of AGP Colombia
"""
import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt, timedelta
import os
import streamlit as st

error_string = ""
ahora = dt.now().strftime('%d-%m-%y')

# Setting the file paths. To run the code, the code must have access to AGP's network

# FOLDER_PATH = r'C:\Users\Juan\Documents\GitHub\muestras-contaminacion\data\Registros'
FOLDER_PATH_COMPLEX = "C:/Users/datosplanta/OneDrive - AGP GROUP/Muestras contaminacion/Muestras particulas complex/Registro particulas complex"
# Usage of glob to find recursively all the samples for each shift
registrosComplex = glob.glob(FOLDER_PATH_COMPLEX + '/*.csv')


df_ultimos = pd.DataFrame()

# Empty lists to be used to concatenate every dataframe created
df_listComplex = []
for file in registrosComplex:
    try:
        df_buffer = pd.read_csv(file, skiprows=2, encoding= 'unicode_escape')
    except:
        error_string = 'Empty file detected'
    else:
        df_buffer.drop(['Cycles', 'Period', 'Environment', 'Address'], axis=1, inplace=True)
        try:
            df_buffer = df_buffer[:5]
        except KeyError:
            #print('Index not found. Skipping')
            pass
        finally:
            df_buffer['Date'] = pd.to_datetime(df_buffer['Date'])
            df_buffer = df_buffer[['Name', 'Date', '5.0um']]
            df_buffer = df_buffer.rename({'0.5um': 'Measurement'}, axis=1)
            df_listComplex.append(df_buffer)

df_registrosComplex = pd.concat(df_listComplex)

# Complex dataset

df_c_mesa1 = df_registrosComplex[df_registrosComplex['Name'] == 'C_E_MESA1'].sort_values('Date').tail(20)
df_ultimos = df_ultimos.append(df_c_mesa1[-1:], ignore_index=False)

df_c_pvb = df_registrosComplex[df_registrosComplex['Name'] == 'C_E_CUARTPVB'].sort_values('Date').tail(20)
df_ultimos = df_ultimos.append(df_c_pvb [-1:], ignore_index=False)

# RETROFIT
FOLDER_PATH_RETROFIT = "C:/Users/datosplanta/OneDrive - AGP GROUP/Muestras contaminacion/Muestras particulas retrofit/Registro"

# Usage of glob to find recursively all the samples for each shift
registrosRetrofit = glob.glob(FOLDER_PATH_RETROFIT + '/*.csv')

# Empty lists to be used to concatenate every dataframe created
df_listRetrofit = []
for file in registrosRetrofit:
    try:
        df_buffer = pd.read_csv(file, skiprows=2, encoding= 'unicode_escape')
    except:
        error_string = 'Empty file detected'
    else:
        df_buffer.drop(['Cycles', 'Period', 'Environment', 'Address'], axis=1, inplace=True)
        try:
            df_buffer = df_buffer[:5]
        except KeyError:
            #print('Index not found. Skipping')
            pass
        finally:
            df_buffer['Date'] = pd.to_datetime(df_buffer['Date'])
            df_buffer = df_buffer[['Name', 'Date', '5.0um']]
            df_buffer = df_buffer.rename({'0.5um': 'Measurement'}, axis=1)
            df_listRetrofit.append(df_buffer)

df_registrosRETROFIT = pd.concat(df_listRetrofit)

# Retrofit dataset
df_r_mesa = df_registrosRETROFIT[df_registrosRETROFIT['Name'] == 'R_E_MESA_1'].sort_values('Date').tail(20)
df_ultimos = df_ultimos.append(df_r_mesa [-1:], ignore_index=False)

df_r_pvb = df_registrosRETROFIT[df_registrosRETROFIT['Name'] == 'R_E_CUARTPVB'].sort_values('Date').tail(20)
df_ultimos = df_ultimos.append(df_r_pvb [-1:], ignore_index=False)

df_r_pu = df_registrosRETROFIT[df_registrosRETROFIT['Name'] == 'R_E_CUARTOPU'].sort_values('Date').tail(20)
df_ultimos = df_ultimos.append(df_r_pu [-1:], ignore_index=False)

df_ultimos.drop('Date', inplace=True, axis=1)
# """
# Plotting
t1_color = "#23A6E0"

# Setting up the plot for Complex

fig, axs = plt.subplots(2)
fig.set_figheight(8)
fig.set_figwidth(15)

axs[0].plot(df_c_mesa1['Date'], df_c_mesa1['5.0um'], marker='o', color=t1_color, label="Medición")
axs[0].hlines(y=129, xmin=df_c_mesa1['Date'].min(), xmax=df_c_mesa1['Date'].max(), linewidth=2, color='y', label='Alerta amarilla')
axs[0].hlines(y=194, xmin=df_c_mesa1['Date'].min(), xmax=df_c_mesa1['Date'].max(), linewidth=2, color='r', label='Alerta roja')
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
axs[0].xaxis.set_major_locator(mdates.DayLocator(interval=1))
axs[0].set_ylabel('Particulado 5.0um')

axs[1].plot(df_c_pvb['Date'], df_c_pvb['5.0um'], marker='o', color=t1_color, label="Medición")
axs[1].hlines(y=102, xmin=df_c_pvb['Date'].min(), xmax=df_c_pvb['Date'].max(), linewidth=2, color='y', label='Alerta amarilla')
axs[1].hlines(y=153, xmin=df_c_pvb['Date'].min(), xmax=df_c_pvb['Date'].max(), linewidth=2, color='r', label='Alerta roja')
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
axs[1].xaxis.set_major_locator(mdates.DayLocator(interval=1))
axs[1].set_ylabel('Particulado 5.0um')

fig.tight_layout(pad=3.0)
axs[0].title.set_text('Estado de contaminación - Cuarto ensamble complex')
axs[1].title.set_text('Estado de contaminación - Cuarto PVB complex')

for i in range(len(axs)):
    axs[i].grid()
    axs[i].legend()

st.pyplot(plt.show())


# Setting up the plot for Retrofit
fig, axs = plt.subplots(3)
fig.set_figheight(12)
fig.set_figwidth(15)

axs[0].plot(df_r_mesa['Date'], df_r_mesa['5.0um'], marker='o', color=t1_color, label="Medición")
axs[0].hlines(y=784, xmin=df_r_mesa['Date'].min(), xmax=df_r_mesa['Date'].max(), linewidth=2, color='y', label='Alerta amarilla')
axs[0].hlines(y=1569, xmin=df_r_mesa['Date'].min(), xmax=df_r_mesa['Date'].max(), linewidth=2, color='r', label='Alerta roja')
axs[0].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
axs[0].xaxis.set_major_locator(mdates.DayLocator(interval=1))
axs[0].set_ylabel('Particulado 5.0um')

axs[1].plot(df_r_pvb['Date'], df_r_pvb['5.0um'], marker='o', color=t1_color, label="Medición")
axs[1].hlines(y=296, xmin=df_r_pvb['Date'].min(), xmax=df_r_pvb['Date'].max(), linewidth=2, color='y', label='Alerta amarilla')
axs[1].hlines(y=593, xmin=df_r_pvb['Date'].min(), xmax=df_r_pvb['Date'].max(), linewidth=2, color='r', label='Alerta roja')
axs[1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
axs[1].xaxis.set_major_locator(mdates.DayLocator(interval=1))
axs[1].set_ylabel('Particulado 5.0um')

axs[2].plot(df_r_pu['Date'], df_r_pu['5.0um'], marker='o', color=t1_color, label="Medición")
axs[2].hlines(y=3429, xmin=df_r_pu['Date'].min(), xmax=df_r_pu['Date'].max(), linewidth=2, color='y', label='Alerta amarilla')
axs[2].hlines(y=6858, xmin=df_r_pu['Date'].min(), xmax=df_r_pu['Date'].max(), linewidth=2, color='r', label='Alerta roja')
axs[2].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
axs[2].xaxis.set_major_locator(mdates.DayLocator(interval=1))
axs[2].set_ylabel('Particulado 5.0um')

fig.tight_layout(pad=3.0)
axs[0].title.set_text('Estado de contaminación - Cuarto ensamble retrofit')
axs[1].title.set_text('Estado de contaminación - Cuarto PVB retrofit')
axs[2].title.set_text('Estado de contaminación - Cuarto PU retrofit')

for i in range(len(axs)):
    axs[i].grid()
    axs[i].legend()

st.pyplot(plt.show())
