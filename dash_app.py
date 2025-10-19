import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load processed data
df = pd.read_csv('data/pink_morsel_sales.csv')

# Ensure Date column is datetime and sorted
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Aggregate sales by date
daily_sales = df.groupby('Date', as_index=False)['Sales'].sum()

# Create line chart
fig = px.line(
    daily_sales,
    x='Date',
    y='Sales',
    title='Pink Morsel Daily Sales Over Time',
    labels={'Date': 'Date', 'Sales': 'Total Sales (USD)'}
)

# Add a vertical line to show the price increase date
price_increase_date = pd.to_datetime("2021-01-15")

# Use add_shape  for better datetime compatibility
fig.add_shape(
    type="line",
    x0=price_increase_date,
    x1=price_increase_date,
    y0=0,
    y1=1,
    yref="paper",
    line=dict(color="red", width=2, dash="dash")
)

# Add annotation for the vertical line
fig.add_annotation(
    x=price_increase_date,
    y=1,
    yref="paper",
    text="Price Increase (Jan 15, 2021)",
    showarrow=False,
    font=dict(size=12, color="red"),
    xanchor="left",
    yshift=10
)

# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1(
        "Pink Morsel Sales Visualizer",
        style={'textAlign': 'center', 'marginBottom': 20, 'color': '#e83e8c'}
    ),

    html.P(
        "Visualising daily sales of Pink Morsels before and after the price increase on Jan 15, 2021.",
        style={'textAlign': 'center', 'fontStyle': 'italic'}
    ),

    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
