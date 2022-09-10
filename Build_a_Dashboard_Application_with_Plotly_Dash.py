# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 11:32:47 2022

@author: emers
"""

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import seaborn as sns

# Read the airline data into pandas dataframe
link = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(link)
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
                                                      options=[{'label': 'All Sites', 'value': 'ALL'}, 
                                                               {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
                                                               {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}, 
                                                               {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                                               {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},],
                                                      value='ALL', 
                                                      placeholder="Select a Launch Site here",
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
                                                marks={0: '0', 100: '100'}, 
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
####______________
@app.callback([Output(component_id='success-pie-chart', component_property='figure'), 
               Output(component_id='success-payload-scatter-chart', component_property='figure')],
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])


# Place to define the callback function

def get_pie_chart(entered_site, Range):
    if entered_site == 'ALL':
        fig1 = px.pie(spacex_df, values = 'class', names='Launch Site', title = 'Total Success Launch by Sites')
        
        fig2 = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(Range[0],Range[1])], 
                          x="Payload Mass (kg)", y="class", 
                          color="Booster Version",
                          title = 'Correlation Between Payload and Success for All Sites')
        
    else:
        dt = pd.get_dummies(spacex_df[spacex_df['Launch Site'] == entered_site]['class']).sum()
        fig1 = px.pie(dt, values = dt.values, names=dt.index, title = 'Total Success Launch in: '+ entered_site)
        
        dt2 = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig2 = px.scatter(dt2[dt2['Payload Mass (kg)'].between(Range[0],Range[1])], 
                          x="Payload Mass (kg)", y="class", 
                          color="Booster Version",
                          title = 'Correlation Between Payload and Success for: '+ entered_site)
    

    return fig1,fig2

        # return the outcomes piechart for a selected site
#[dcc.Graph(figure=fig)]
####_________________

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()