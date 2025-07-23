# Import
import dash
from dash import dcc, Input, Output, html
import plotly.express as px
import pandas as pd

def load_data():
    data = pd.read_csv('./assets/cars.csv', encoding='latin1')
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

# print(len(data['Company Names'].unique())) # 37
# print(len(data))
# print("len of Toyota is: ", len(data[data["Company Names"] == "TOYOTA"]))
# print(data[data['Company Names'] == 'TOYOTA']['Fuel Types'].count())
# print("Seats is: ", data[data['Company Names'] == 'TOYOTA']['Seats'].count())
# print("Fuel Types is: ", data[data['Company Names'] == 'TOYOTA']['Fuel Types'].count())
# print("Engines is: ", len(data[data['Company Names'] == 'TOYOTA']['Engines'].unique()))
# print("Fuel Types is: ", len(data[data['Company Names'] == 'TOYOTA']['Fuel Types'].unique()))
# print(len(data.groupby(['Company Names'] == 'TOYOTA').agg({'Fuel Types': 'count'})))

car_type = data['Company Names'].value_counts().reset_index()
car_type.columns = ['Car Categorical', 'Amount of Car']

app.layout = html.Div([
    html.H1("Car Dashboard", className="text-center my-5 text-3xl"),

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

    html.Div([
        html.Div([
            html.H4("Fuel Type base on the Car's category", className="text-2xl font-semibold my-4 text-center"),
            html.Div([
                dcc.Dropdown(
                    id='car-fuel-filter',
                    options=[{"label": name, "value": name} for name in data['Company Names'].dropna().unique()],
                    value='Ford',
                    style={'width': '900px'}
                )
            ], className="flex justify-center mb-4"),
            html.Div([
                dcc.Graph(id='car-fuel-distribution', style={'width': '900px'})
            ], className="flex justify-center")
        ])
    ], className="w-full mx-4 max-w-8xl")
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
































if __name__ == "__main__":
    app.run(debug=True)