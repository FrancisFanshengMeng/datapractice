# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC_40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC_4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC_39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC_40', 'value': 'CCAFS SLC-40'},
                                                    ],
                                                value='ALL',
                                                placeholder="Select site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    print("***********Start Pie *************")
    print(entered_site)
    filtered_df = spacex_df
    data = filtered_df.groupby(['Launch Site'])['class'].sum().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:   
        #filtered_df.set_index('Launch Site',inplace=True,append=True)
        print("!!!!!index changed, Launch Site disappeare")
        print(spacex_df.columns)
        #success = filtered_df.loc[entered_site,'class'].mean()
        success = filtered_df[(filtered_df['Launch Site'] == entered_site)]['class'].mean()
        #filtered_df = filtered_df.reset_index().rename_axis(None, axis=1)    
        print("!!!!!index reset, Lanch Site recovered ????") 
        print(spacex_df.columns)   
        print(success)
        fig = px.pie(values=[success, 1-success], names=['Success', 'Failure'])
        #fig.show()
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property="value")])
def get_sucess_payload_chart(entered_site,payload):
    print("*******Start Scatter *******")
    print(entered_site)
    print(payload)
    if entered_site == 'ALL':
        filtered = spacex_df[(spacex_df['Payload Mass (kg)'] >  payload[0]) & (spacex_df['Payload Mass (kg)'] <  payload[1])]
        fig = px.scatter(filtered, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title="Correlation between Payload and Success to all Sites",
                         labels={"x": "Payload Mass(kg)", "y": "Y Axis Label"},
                         range_x=[0, 10000], range_y=[-1.2, 1.2])
        #fig.show()
        #fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        return fig
    else:
        #filtered1 = spacex_df
        #filtered1.set_index('Launch Site', inplace=True)
        #filtered1.loc[entered_site] 
        print(spacex_df.columns)
        data1 = spacex_df[(spacex_df['Payload Mass (kg)'] >  payload[0]) & (spacex_df['Payload Mass (kg)'] <  payload[1])
                           & (spacex_df['Launch Site'] ==  entered_site)]
        #filtered1.head()
             
        fig = px.scatter(data1, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title= f"Correlation between Payload and Success to {entered_site}",
                         labels={"x": "Payload Mass(kg)", "y": "Y Axis Label"},
                         range_x=[0, 10000], range_y=[-1.2, 1.2])
        
        #fig.show()
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
