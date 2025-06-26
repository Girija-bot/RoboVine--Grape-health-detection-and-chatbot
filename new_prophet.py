import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def run_prophet_forecast(file_path, parameter_name, save_plot=True):
    df = pd.read_csv(file_path)
    print(f"Preview of data for {parameter_name}:")
    print(df.head())

    # Normalize column names to lowercase for consistency
    df.columns = df.columns.str.lower()

    # Try to detect id_vars column (e.g., 'data' or 'unit') + 'thesis'
    possible_id_vars_1 = ['data', 'unit']
    id_var_1 = next((col for col in possible_id_vars_1 if col in df.columns), None)
    id_vars = [id_var_1, 'thesis']

    # Check if these columns actually exist
    missing_cols = [col for col in id_vars if col not in df.columns]
    if missing_cols:
        raise KeyError(f"Missing expected id_vars columns: {missing_cols}")

    # Date columns start from 3rd column onwards (index 2)
    date_cols = df.columns.difference(id_vars)

    # Melt dataframe to long format
    df_melted = df.melt(id_vars=id_vars, value_vars=date_cols, var_name='ds', value_name='y')

    # Convert 'ds' to datetime, drop rows with invalid dates or missing values
    df_melted['ds'] = pd.to_datetime(df_melted['ds'], errors='coerce')
    df_melted = df_melted.dropna(subset=['ds', 'y'])

    # Group by date to get average values
    daily_avg = df_melted.groupby('ds')['y'].mean().reset_index()

    # Fit Prophet model
    model = Prophet()
    model.fit(daily_avg)

    # Create future dataframe for 30 days
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Plot forecast and return figure object without showing it yet
    fig = model.plot(forecast)
    plt.title(f"Prophet Forecast - {parameter_name}")
    plt.xlabel("Date")
    plt.ylabel(parameter_name)
    plt.grid(True)

    if save_plot:
        plt.savefig(f"Forecast_{parameter_name.replace(' ', '_')}.png")

    return fig, forecast


# Run all forecasts and collect figures
fig1, _ = run_prophet_forecast(r"C:\Users\girij\Distributed systems\csv_files\Normalized_daily_transpiration_Normalized.csv", "Normalized Transpiration", save_plot=True)
fig2, _ = run_prophet_forecast(r"C:\Users\girij\Distributed systems\csv_files\Normalized_Gs_canopy_6-7h_Normalized.csv", "Stomatal Conductance 6-7am", save_plot=True)
fig3, _ = run_prophet_forecast(r"C:\Users\girij\Distributed systems\csv_files\Normalized_Gs_canopy_12-13h_Normalized.csv", "Stomatal Conductance 12-1pm", save_plot=True)

# Show all plots at once
plt.show()
