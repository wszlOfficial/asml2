from pathlib import Path
import pandas as pd
from plotnine import *

def load_data(df: pd.DataFrame):
    # Check if has all necessary columns
    columns = ['time', 'temperature (C)', 'Volumetric Water Content (%)',
               'Electrical Conductivity (uS/cm)', 'latitude', 'longlitude']
    
    if not set(columns).issubset(df.columns):
        return

    df['time'] = pd.to_datetime(df['time'], errors='coerce')

    df['Volumetric Water Content (%)'] = pd.to_numeric(df['Volumetric Water Content (%)'], errors='coerce')
    df['temperature (C)'] = pd.to_numeric(df['temperature (C)'], errors='coerce')
    df['Electrical Conductivity (uS/cm)'] = pd.to_numeric(df['Electrical Conductivity (uS/cm)'], errors='coerce')
    df = df.dropna(subset=[\
    'temperature (C)',\
    'Volumetric Water Content (%)',\
    'Electrical Conductivity (uS/cm)']).reset_index(drop=True)

    # Remove obvious invalid sensor values and extreme outliers
    df = df[
        df['temperature (C)'].between(-50, 60) &
        df['Volumetric Water Content (%)'].between(0, 100) &
        df['Electrical Conductivity (uS/cm)'].between(0, 7000)
    ].reset_index(drop=True)
    return df
