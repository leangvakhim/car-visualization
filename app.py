# Import
import dash
from dash import dcc, Input, Output, html
import plotly.express as px
import pandas as pd

def load_data():
    data = pd.read_csv('./assets/cars.csv', encoding='latin1')
    data['Company Names'] = data['Company Names'].str.strip().str.upper()
    data['Fuel Types'] = data['Fuel Types'].str.strip().str.upper()

    if 'Total Speed' in data.columns:
        data['Total Speed'] = data['Total Speed'].str.replace(' km/h', '', regex=False) # regex=False mean treats the pattern as plain text
        data['Total Speed'] = pd.to_numeric(data['Total Speed'], errors='coerce') # errors='coerce' if value can't be converted it replace "N/A"
        Q1 = data['Total Speed'].quantile(0.25)
        Q3 = data['Total Speed'].quantile(0.75)
        IQR = Q3 - Q1
        data = data[(data['Total Speed'] >= Q1 - 1.5 * IQR) & (data['Total Speed'] <= Q3 + 1.5 * IQR)]

    if 'Performance(0 - 100 )KM/H' in data.columns:
        data['Performance(0 - 100 )KM/H'] = data['Performance(0 - 100 )KM/H'].str.replace(' sec', '', regex=False)
        data['Performance(0 - 100 )KM/H'] = pd.to_numeric(data['Performance(0 - 100 )KM/H'], errors='coerce')
        Q1 = data['Performance(0 - 100 )KM/H'].quantile(0.25)
        Q3 = data['Performance(0 - 100 )KM/H'].quantile(0.75)
        IQR = Q3 - Q1
        data = data[(data['Performance(0 - 100 )KM/H'] >= Q1 - 1.5 * IQR) & (data['Performance(0 - 100 )KM/H'] <= Q3 + 1.5 * IQR)]

    if 'CC/Battery Capacity' in data.columns:
        def convert_hp(val):
            if pd.isna(val):
                return None
            val = str(val).lower().strip()

            if 'kwh' in val:
                try:
                    return float(val.replace(' kwh', '').split()[0]) * 35529.2376
                except:
                    return None
            if 'cc' in val:
                try:
                    return float(val.split()[0].replace(',', ''))
                except:
                    return None

            if '/' in val:
                parts = val.split('/')
                return (float(parts[0]) + float(parts[1])) / 2

            return None

        data['CC/Battery Capacity'] = data['CC/Battery Capacity'].apply(convert_hp)
        Q1 = data['CC/Battery Capacity'].quantile(0.25)
        Q3 = data['CC/Battery Capacity'].quantile(0.75)
        IQR = Q3 - Q1
        data = data[(data['CC/Battery Capacity'] >= Q1 - 1.5 * IQR) & (data['CC/Battery Capacity'] <= Q3 + 1.5 * IQR)]

    if 'HorsePower' in data.columns:
        data['HorsePower'] = data['HorsePower'].str.replace(' hp', '', regex=False)

        def convert_hp(val):
            if pd.isna(val):
                return None
            val = str(val).lower().strip()

            if 'cc' in val:
                val = val.replace(' cc', '')
                try:
                    return float(val.replace(',', '')) * 0.0667
                except:
                    return None

            if 'hp' in val:
                val = val.replace(' hp', '')

            if '/' in val:
                parts = val.split('/')
                return (float(parts[0]) + float(parts[1])) / 2

            if '~' in val:
                val = val.replace('~', '')

            if ',' in val:
                val = val.replace(',', '')

            if 'up to' in val:
                val = val.replace('up to ', '')

            if '(est.)' in val:
                val = val.replace(' (est.)', '')

            if 'ï¿½' in val:
                parts = val.split('ï¿½')
                return (float(parts[0]) + float(parts[1])) / 2

            if '-' in val:
                parts = val.split('-')
                return (float(parts[0]) + float(parts[1])) / 2

            return float(val)
        data['HorsePower'] = data['HorsePower'].apply(convert_hp)
        Q1 = data['HorsePower'].quantile(0.25)
        Q3 = data['HorsePower'].quantile(0.75)
        IQR = Q3 - Q1
        data = data[(data['HorsePower'] >= Q1 - 1.5 * IQR) & (data['HorsePower'] <= Q3 + 1.5 * IQR)]

    if 'Seats' in data.columns:
        data['Seats'] = data['Seats'].str.strip()

        def convert_hp(val):

            if '+' in val:
                parts = val.split('+')
                return (float(parts[0]) + float(parts[1])) / 2

            if 'ï¿½' in val:
                parts = val.split('ï¿½')
                return (float(parts[0]))

            return float(val)
        data['Seats'] = data['Seats'].apply(convert_hp)

    if 'Cars Prices' in data.columns:
        data['Cars Prices'] = data['Cars Prices'].str.strip().str.replace('$', '', regex=False)

        def convert_price(val):
            if pd.isna(val):
                return None

            if '€' in val:
                val = val.replace('€', '')
                try:
                    return float(val.replace(',', '')) * 1.17
                except:
                    return None

            if '.00' in val:
                val = val.replace('.00', '')

            if '-' in val:
                parts = val.split('-')
                return (float(parts[0].replace(',', '')) + float(parts[1].replace(',', ''))) / 2

            if ',' in val:
                val = val.replace(',', '')

            if '/' in val:
                parts = val.split('/')
                return (float(parts[0].replace(',', '')) + float(parts[1].replace(',', ''))) / 2

            if 'up to' in val:
                val = val.replace('up to ', '')

            if '(est.)' in val:
                val = val.replace(' (est.)', '')

            if 'ï¿½' in val:
                parts = val.split('ï¿½')
                return (float(parts[0]) + float(parts[1])) / 2

            if '-' in val:
                parts = val.split('-')
                return (float(parts[0]) + float(parts[1])) / 2

            return float(val)
        data['Cars Prices'] = data['Cars Prices'].apply(convert_price)
        Q1 = data['Cars Prices'].quantile(0.25)
        Q3 = data['Cars Prices'].quantile(0.75)
        IQR = Q3 - Q1
        data = data[(data['Cars Prices'] >= Q1 - 1.5 * IQR) & (data['Cars Prices'] <= Q3 + 1.5 * IQR)]

    return data
data = load_data()

app = dash.Dash(__name__)
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Cars Dashboard</title>
        <link rel="icon" type="image/x-icon" href="/assets/vehicle.png">
        {%css%}
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

car_type = data['Company Names'].value_counts().reset_index()
car_type.columns = ['Car Categorical', 'Amount of Car']

app.layout = html.Div([
    html.H1("Car Dashboard", className="text-center my-5 text-3xl"),

    # barplot
    html.Div([
        html.Div([
            html.H4("Car Category", className="text-2xl font-semibold my-4 text-center"),
            html.Div([
                dcc.Graph(
                    id='car-pie',
                    figure=px.bar(
                        car_type,
                        x='Car Categorical',
                        y='Amount of Car',
                    ),
                    style={'width': '900px'}
                )
            ], className="flex justify-center")
        ])
    ], className="w-full mx-4 max-w-8xl"),

    # piechart
    html.Div([
        html.Div([
            html.H4("Fuel Type base on the Car's category", className="text-2xl font-semibold my-4 text-center"),
            html.Div([
                dcc.Dropdown(
                    id='car-fuel-filter',
                    options=[{"label": name, "value": name} for name in data['Company Names'].dropna().unique()],
                    value='FORD',
                    style={'width': '900px'}
                )
            ], className="flex justify-center mb-4"),
            html.Div([
                dcc.Graph(id='car-fuel-distribution', style={'width': '900px'})
            ], className="flex justify-center")
        ])
    ], className="w-full mx-4 max-w-8xl"),

    # scatterplot
    html.Div([
        html.Div([
            html.H4("Car's information base on the category", className="text-2xl font-semibold my-4 text-center"),
            html.Div([
                dcc.Dropdown(
                    id='car-information-filter',
                    options=[
                        {"label": "CC/Battery Capacity", "value": "CC/Battery Capacity"},
                        {"label": "HorsePower", "value": "HorsePower"},
                        {"label": "Total Speed", "value": "Total Speed"},
                        {"label": "Performance(0 - 100 )KM/H", "value": "Performance(0 - 100 )KM/H"},
                        {"label": "Seats", "value": "Seats"}
                    ],
                    value='Total Speed',
                    style={'width': '900px'}
                )
            ], className="flex justify-center mb-4"),
            html.Div([
                dcc.Graph(id='car-information-distribution', style={'width': '900px', 'height': '600px'})
            ], className="flex justify-center")
        ])
    ], className="w-full mx-4 max-w-8xl"),

    # bubbleplot
    html.Div([
        html.Div([
            html.H4("Car's price base on the speed", className="text-2xl font-semibold my-4 text-center"),
            html.Div([
                html.Div([
                    dcc.RangeSlider(
                        id='car-price-filter',
                        min=data['Cars Prices'].min(),
                        max=data['Cars Prices'].max(),
                        value=[data['Cars Prices'].min(), data['Cars Prices'].max()],
                        marks={
                            int(value): f"${int(value):,}"
                            for value in data["Cars Prices"].quantile([0, 1]).values
                        },
                        tooltip={
                            "placement": "bottom",
                            "always_visible": True,
                        },
                        step=int((data['Cars Prices'].max() - data['Cars Prices'].min()) / 100)
                    )
                ], style={
                    'width': '100%',
                    'padding': '0 10%'
                })
            ], className="flex justify-center"),
            html.Div([
                dcc.Graph(id='car-price-distribution', style={'width': '900px', 'height': '600px'})
            ], className="flex justify-center")
        ])
    ], className="w-full mx-4 max-w-8xl"),
])

# Create our Callbacks
@app.callback(
    Output('car-fuel-distribution', 'figure'),
    Input('car-fuel-filter', 'value')
)

def update_car_fuel_distribution(selected_car):
    if selected_car:
        filtered_df = data[data['Company Names'] == selected_car]
    else:
        filtered_df = data

    fuel_counts = filtered_df['Fuel Types'].value_counts().reset_index()
    fuel_counts.columns = ['Fuel Types', 'Count']

    fig = px.pie(
        fuel_counts,
        values='Count',
        names='Fuel Types',
        title=f'Fuel Type Distribution for {selected_car}'
    )

    return fig

@app.callback(
    Output('car-information-distribution', 'figure'),
    Input('car-information-filter', 'value')
)

def update_car_information_distribution(selected_info):

    filtered_df = data.copy()

    avg_df = filtered_df[['Company Names', selected_info]].dropna()

    if selected_info == 'CC/Battery Capacity' :
        ylabel_title = "CC/Battery Capacity in cc"
    elif selected_info == 'HorsePower':
        ylabel_title = "HorsePower in hp"
    elif selected_info == 'Total Speed':
        ylabel_title = "Total Speed in km/h"
    elif selected_info == 'Performance(0 - 100 )KM/H':
        ylabel_title = "Performance(0 - 100 )KM/H as sec"
    elif selected_info == 'Seats':
        ylabel_title = "Amount of Seats"
    else :
        ylabel_title = "Invalid"

    fig = px.scatter(
        avg_df,
        x='Company Names',
        y=selected_info,
        title=f'{selected_info} per Car Brand'
    )

    fig.update_layout(
        xaxis_title="Car Brand",
        yaxis_title=ylabel_title
    )

    return fig

@app.callback(
    Output('car-price-distribution', 'figure'),
    Input('car-price-filter', 'value')
)
def update_car_price_distribution(selected_price):
    filtered_data = data[
        (data['Cars Prices'] >= selected_price[0]) &
        (data['Cars Prices'] <= selected_price[1])
    ]
    fig = px.scatter(
        filtered_data,
        x='Cars Prices',
        y='Total Speed',
        size="Seats",
        color='Company Names',
        log_x=True,
        custom_data=[
            'Cars Names', 'HorsePower', 'Seats', 'Engines', 'Company Names', 'Fuel Types', "Performance(0 - 100 )KM/H"
        ]
    )


    fig.update_traces(
        hovertemplate="<b>Name:%{customdata[0]}</b><br>" +
                    "HorsePower: %{customdata[1]:.0f} hp<br>" +
                    "Seats: %{customdata[2]}<br>" +
                    "Engine: %{customdata[3]}<br>" +
                    "Model: %{customdata[4]}<br>" +
                    "Fuel Type: %{customdata[5]}<br>" +
                    "Performance (0-100)km/h: %{customdata[6]} sec<br>" +
                    "Price: %{x:$,.0f}<br>" +
                    "Speed: %{y} km/h"
    )

    fig.update_layout(
        xaxis_title="Car Prices in dollars($)",
        yaxis_title="Speed in km per hour"
    )

    return fig





























if __name__ == "__main__":
    app.run(debug=True)