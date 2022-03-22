# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 07:51:47 2022

@author: Toyin
"""

# Import required libraries
import pandas as pd
import dash
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# loading dataset to be used
df = pd.read_csv('crowdfunding.csv')

# Create a dash application
app = Dash(__name__)
server = app.server
app.layout = html.Div(children=[html.H1('Crowdfunding Marketing',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                # dropdown for selecting what criteria you will like to visualize
                                dcc.Dropdown(id='criteria-dropdown', 
                                                options = [{'label':'category','value':'category'},
                                                           {'label':'device','value':'device'},
                                                           {'label':'age', 'value':'age'}],
                                                placeholder = 'Select a criteria to be used',
                                              	value = 'category',
                                                searchable = True
                                            ),                                
                                html.Br(),
                                
                                # Graph
                                html.Div(dcc.Graph(id='criteria-bar-chart')),
                                html.Br()]
                     )
                      
# Add a callback function for `site-dropdown` as input, `criteria-bar-chart` as output
@app.callback(Output(component_id='criteria-bar-chart', component_property='figure'),
                Input(component_id='criteria-dropdown', component_property='value')
                )

    
def bar_chart(criteria):
    # creating chart
    grouping = df.groupby(criteria)[['amount']].sum()
    if criteria == 'category':
        sorted_grouping = grouping.sort_values(by = 'amount', ascending = False).iloc[:3]
        title = f"Top three {criteria}"
        fig = px.bar(x = sorted_grouping.index, y = sorted_grouping.amount, title = title)
        fig.update_yaxes(range = [160000, 170000])
        return fig
    else:
        sorted_grouping = grouping.sort_values(by = 'amount', ascending = False)
        title = f"Bar Chart by {criteria}"
        fig = px.bar(x = sorted_grouping.index, y = sorted_grouping.amount, title = title)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()