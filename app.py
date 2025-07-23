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
    ], className="w-full mx-4 max-w-8xl")
])


if __name__ == "__main__":
    app.run(debug=True)