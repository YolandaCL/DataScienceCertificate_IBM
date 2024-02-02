# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import folium

# Create a dash application
app = dash.Dash(__name__)

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = int(spacex_df['Payload Mass (kg)'].max())
min_payload = int(spacex_df['Payload Mass (kg)'].min())

# Get the unique launch sites from the DataFrame
launch_sites = spacex_df['Launch Site'].unique()

# Create options for the dropdown based on the unique launch sites
site_options = [{'label': site, 'value': site} for site in launch_sites]

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
           style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    # Create the dropdown component
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                 ] + site_options,  # Add the site options here
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True
                 ),


    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload,
                    max=max_payload,
                    step=1000,
                    marks={i: str(i) for i in range(min_payload, max_payload + 1, 1000)},
                    value=[min_payload, max_payload]
                    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Define the callback function for success-pie-chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # If 'ALL' sites selected, use all data
        fig = px.pie(spacex_df, names='class', title='Total Success Launches')
    else:
        # Filter data for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Create a pie chart for the selected site
        fig = px.pie(filtered_df, names='class', title=f'Success Launches at {selected_site}')

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        # Filter spacex_df according to the selected payload range
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (
                spacex_df['Payload Mass (kg)'] <= payload_range[1])]

        # Create the scatter plot with all booster versions and label the points by booster version category

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Launch Outcomes'
        )
    else:
        # Filter spacex_df for the specific selected site and within the payload range
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) & (
                spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (
                                           spacex_df['Payload Mass (kg)'] <= payload_range[1])]

        # Create the scatter plot and label the points by booster version category
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Launch Outcomes for {selected_site}'
        )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(port=8050)
