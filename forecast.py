import pandas as pd
import os
from prophet import Prophet
import matplotlib.pyplot as plt

# Load your CSV
df = pd.read_csv("simulation_log.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
print(df.head())
print(df.dtypes)

# Directory for results
output_dir = "selected_forecasts"
os.makedirs(output_dir, exist_ok=True)

# Columns you asked to forecast
target_columns = [
    "Mean_Biomass_Gain",
    "Mean_Transpiration_Rate",
    "Mean_Daily_Transpiration"
]

for col in target_columns:
    print(f"🔮 Forecasting: {col}")
    df_prophet = df[['timestamp', col]].rename(columns={'timestamp': 'ds', col: 'y'}).dropna()
    print(f"Rows after dropna for {col}: {len(df_prophet)}")
    if len(df_prophet) < 10:
        print(f"⚠️ Not enough data for {col}. Skipping.")
        continue
    try:
        # Increased changepoint_prior_scale for more flexibility in trend
        model = Prophet(changepoint_prior_scale=0.5, interval_width=0.8)
        model.fit(df_prophet)
    except Exception as e:
        print(f"Error fitting Prophet model for {col}: {e}")
        continue

    future = model.make_future_dataframe(periods=30, freq='H')
    forecast = model.predict(future)
    print(f"Forecast rows for {col}: {len(forecast)}")

    # Plot and save forecast
    fig = model.plot(forecast)
    plt.title(f"Forecast for {col}")
    plt.xlabel("Time")
    plt.ylabel(col)
    plot_path = os.path.join(output_dir, f"{col}_forecast.png")
    fig.savefig(plot_path)
    plt.close()

    # Save future forecast CSV
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(
        os.path.join(output_dir, f"{col}_forecast.csv"), index=False
    )
    print(f"✅ Saved: {plot_path}")

print("\n🎯 All selected forecasts are saved in 'selected_forecasts' folder.")
