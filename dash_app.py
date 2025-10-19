import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load processed data
df = pd.read_csv('data/pink_morsel_sales.csv')

# Ensure Date column is datetime and sorted
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Initialize Dash app
app = Dash(__name__)

# Define color palette
colors = {
    'background': '#F8F9FA',
    'text': '#343A40',
    'accent': '#E83E8C'
}

# Layout
app.layout = html.Div(
    style={
        'backgroundColor': colors['background'],
        'fontFamily': 'Arial, sans-serif',
        'padding': '30px'
    },
    children=[
        html.H1(
            "Pink Morsel Sales Visualizer",
            style={
                'textAlign': 'center',
                'marginBottom': '15px',
                'color': colors['accent'],
                'fontWeight': 'bold',
                'fontSize': '2.2em'
            }
        ),

        html.P(
            "Explore regional sales of Pink Morsels before and after the January 15, 2021 price increase.",
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'fontStyle': 'italic',
                'marginBottom': '25px'
            }
        ),

        html.Div(
            style={'textAlign': 'center', 'marginBottom': '25px'},
            children=[
                html.Label(
                    "Select Region:",
                    style={'fontWeight': 'bold', 'fontSize': '16px', 'marginRight': '10px'}
                ),
                dcc.RadioItems(
                    id='region-selector',
                    options=[
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'},
                        {'label': 'All', 'value': 'all'},
                    ],
                    value='all',
                    inline=True,
                    inputStyle={'marginRight': '6px'},
                    labelStyle={
                        'marginRight': '20px',
                        'fontSize': '15px',
                        'color': colors['text']
                    }
                ),
            ]
        ),

        html.Div(
            dcc.Graph(id='sales-line-chart'),
            style={
                'border': f'2px solid {colors["accent"]}',
                'borderRadius': '10px',
                'boxShadow': '2px 2px 10px rgba(0, 0, 0, 0.1)',
                'padding': '15px',
                'backgroundColor': 'white'
            }
        )
    ]
)


# Callback to update chart based on selected region
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-selector', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['Region'].str.lower() == selected_region]

    # Aggregate sales by date
    daily_sales = filtered_df.groupby('Date', as_index=False)['Sales'].sum()

    # Create line chart
    fig = px.line(
        daily_sales,
        x='Date',
        y='Sales',
        title=f"Pink Morsel Daily Sales — Region: {selected_region.capitalize()}",
        labels={'Date': 'Date', 'Sales': 'Total Sales (USD)'},
        template='plotly_white'
    )

    # Add vertical line for price increase
    price_increase_date = pd.to_datetime("2021-01-15")
    fig.add_shape(
        type="line",
        x0=price_increase_date,
        x1=price_increase_date,
        y0=0,
        y1=1,
        yref="paper",
        line=dict(color="red", width=2, dash="dash")
    )

    # Add annotation for the line
    fig.add_annotation(
        x=price_increase_date,
        y=1,
        yref="paper",
        text="Price Increase (Jan 15, 2021)",
        showarrow=False,
        font=dict(size=16, color="red"),
        xanchor="left",
        yshift=10
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text']),
        title_x=0.5
    )

    return fig


# Run the server
if __name__ == '__main__':
    app.run(debug=True)
