from preswald import text, plotly, connect, get_df, table, query, slider
import pandas as pd
import plotly.express as px

text("# Weather Analysis Dashboard")
text("Explore weather patterns using temperature, wind, and precipitation data.")

# Load the CSV
connect()
df = get_df("weather")
if df is None:
    text("Failed to load data. Check dataset 'sample_csv' and preswald.toml.")
    exit()

# ✅ Ensure 'date' column is properly formatted
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])  # Convert to datetime format
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')  # Create a string version for plotting

# Query the dataset
sql = "SELECT * FROM weather WHERE temp_max > 5.0"
filtered_df = query(sql, "weather")

# Temperature Analysis Section
text("## Temperature Analysis")

# Scatter Plot with Wind Size
fig = px.scatter(
    df,
    x='temp_max',
    y='temp_min',
    text='weather',
    color='weather',
    size='wind',
    title='Temp Max vs. Temp Min (Point Size by Wind Speed)',
    labels={'temp_max': 'Max Temperature (°C)', 'temp_min': 'Min Temperature (°C)'}
)
fig.update_traces(textposition='top center')
fig.update_layout(template='plotly_white')
plotly(fig)

# ✅ Time Series Plot (Single Variable) - Using `date_str` for serialization
fig_line = px.line(
    df,
    x='date_str',  # Use the string column
    y='temp_max',
    title='Max Temperature Over Time',
    labels={'date_str': 'Date', 'temp_max': 'Max Temperature (°C)'}
)
fig_line.update_layout(template='plotly_white')
plotly(fig_line)

# ✅ Time Series Plot (Multiple Variables) - Using `date_str`
fig_time_series = px.line(
    df,
    x='date_str',  # Use string column
    y=['temp_max', 'temp_min'],
    title='Temperature Trends Over Time',
    labels={'date_str': 'Date', 'value': 'Temperature (°C)', 'variable': 'Temperature Type'},
    color_discrete_map={'temp_max': 'red', 'temp_min': 'blue'}
)
fig_time_series.update_layout(template='plotly_white')
plotly(fig_time_series)

# Scatter Plots by Weather Type
text("### Scatter Plots by Weather Type")
weather_types = df['weather'].unique()
for weather in weather_types:
    text(f"#### {weather.capitalize()}")
    temp_df = df[df['weather'] == weather]
    fig_weather = px.scatter(
        temp_df,
        x='temp_max',
        y='temp_min',
        text='weather',
        title=f'Temp Max vs. Temp Min ({weather.capitalize()})',
        labels={'temp_max': 'Max Temperature (°C)', 'temp_min': 'Min Temperature (°C)'}
    )
    fig_weather.update_traces(textposition='top center', marker=dict(size=12))
    fig_weather.update_layout(template='plotly_white')
    plotly(fig_weather)

# Data Filtering Section
text("## Interactive Data Exploration")

# Slider for Dynamic Filtering
text("### Filter Data by Temperature Threshold")
threshold = slider("Temperature Threshold (°C)", min_val=-10, max_val=40, default=5)

# Statistical Insights Section
text("## Statistical Insights")

# Histogram
fig_hist = px.histogram(
    df,
    x='temp_max',
    color='weather',
    title='Distribution of Max Temperature by Weather Type',
    labels={'temp_max': 'Max Temperature (°C)', 'count': 'Frequency'},
    marginal='box'
)
fig_hist.update_layout(template='plotly_white')
plotly(fig_hist)

# Correlation Heatmap
corr = df[['precipitation', 'temp_max', 'temp_min', 'wind']].corr()
fig_heatmap = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    title='Correlation Heatmap of Weather Variables'
)
fig_heatmap.update_layout(template='plotly_white')
plotly(fig_heatmap)

# Summary Statistics
avg_temp_by_weather = df.groupby('weather')['temp_max'].mean().round(2).sort_values(ascending=False)
text("#### Average Max Temperature by Weather Type")
for weather, temp in avg_temp_by_weather.items():
    text(f"- **{weather.capitalize()}**: {temp}°C")

# Data Overview Section
text("## Data Overview")

# Filtered Data Table
text("### Filtered Data (Temp Max > 5°C)")
table(filtered_df.head(10), title="Filtered Data")

text("### Raw Data (First 10 Rows)")
table(df.head(10), title="Raw Data")
