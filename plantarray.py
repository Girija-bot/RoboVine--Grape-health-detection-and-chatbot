import pandas as pd
import numpy as np

# Load your separate datasets
df_transpiration = pd.read_csv(r"C:\Users\girij\Distributed systems\csv_files\Normalized_daily_transpiration_Normalized.csv")
df_gs_morning = pd.read_csv(r"C:\Users\girij\Distributed systems\csv_files\Normalized_Gs_canopy_6-7h_Normalized.csv")
df_gs_noon = pd.read_csv(r"C:\Users\girij\Distributed systems\csv_files\Normalized_Gs_canopy_12-13h_Normalized.csv")

# Ensure all columns (except IDs if present) are numeric
df_transpiration = df_transpiration.apply(pd.to_numeric, errors='coerce')
df_gs_morning = df_gs_morning.apply(pd.to_numeric, errors='coerce')
df_gs_noon = df_gs_noon.apply(pd.to_numeric, errors='coerce')

# Drop any rows with completely NaN values (optional but recommended)
df_transpiration.dropna(how='all', inplace=True)
df_gs_morning.dropna(how='all', inplace=True)
df_gs_noon.dropna(how='all', inplace=True)

# Step 1: Initial Weight → assume it's in first column of morning Gs
initial_weight = df_gs_morning.iloc[:, 0]

# Step 2: Biomass Gain → using difference across columns in morning Gs
biomass_gain = df_gs_morning.diff(axis=1)

# Step 3: Transpiration Rate = first derivative of df_transpiration
transpiration_rate = df_transpiration.diff(axis=1)

# Step 4: Daily Transpiration → already in df_transpiration as normalized values
mean_dt = df_transpiration.mean(axis=1)

# Step 5: Canopy Stomatal Conductance (average of both times)
VPD = 1.2
P_atm = 101.3
GS_avg = (df_gs_morning.mean(axis=1) + df_gs_noon.mean(axis=1)) / 2
GS = GS_avg / (VPD * P_atm)

# Step 6: Water Use Efficiency (WUE)
WUE = biomass_gain.mean(axis=1) / mean_dt.replace(0, np.nan)

# Step 7: Theta crit → Assume unavailable
theta_crit = pd.Series([np.nan] * len(df_transpiration), index=df_transpiration.index)

# Step 8: Stress Degree (first vs last transpiration value)
DT_start = df_transpiration.iloc[:, 0]
DT_end = df_transpiration.iloc[:, -1]
stress_degree = (DT_start - DT_end) / DT_start.replace(0, np.nan)

# Step 9: Resilience Rate
def compute_slope(row):
    x = np.arange(len(row))
    y = row.values
    if np.isnan(y).all():
        return np.nan
    try:
        slope, _ = np.polyfit(x, y, 1)
        return slope
    except:
        return np.nan

resilience_rate = df_transpiration.apply(compute_slope, axis=1)

# Combine all features into a DataFrame
features_df = pd.DataFrame({
    'Initial_Weight': initial_weight,
    'Mean_Biomass_Gain': biomass_gain.mean(axis=1),
    'Mean_Transpiration_Rate': transpiration_rate.mean(axis=1),
    'Mean_Daily_Transpiration': mean_dt,
    'Canopy_Stomatal_Conductance': GS,
    'Water_Use_Efficiency': WUE,
    'Theta_Crit': theta_crit,
    'Stress_Degree': stress_degree,
    'Resilience_Rate': resilience_rate
})

print(features_df.head())
