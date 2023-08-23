#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from google.cloud import bigquery
import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px


# In[ ]:


client = bigquery.Client()

query = """
    SELECT
        *
    FROM `roma-immobiliare-395210.dwh_test_dbt.real_estates` 
    LIMIT 1000
"""
# results = client.query(query)
df = pd.read_gbq(query, dialect="standard")
    


# In[ ]:


df_dash = df[[
    'realestate_id',
    'realestate_type',
    'realestate_city',
    'realestate_surface_squaremeter',
    'realestate_number_of_rooms',
    'advert_price'
]].sort_values('advert_price', ascending=False)


# In[ ]:


city_value_counts = df_dash.realestate_city.value_counts().reset_index()
city_value_counts['mapped'] = city_value_counts.apply(lambda x: x[0] if x[1]>10 else 'other' , axis=1)
df_dash['realestate_city_mapped'] = df_dash['realestate_city'].map(dict(city_value_counts[['realestate_city','mapped']].values))


# In[ ]:


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Roma House Prices'),
    html.Hr(),
    dcc.RadioItems(options= ['realestate_surface_squaremeter','realestate_number_of_rooms','advert_price'], value='advert_price', id='controls-and-radio-item'),
    dash_table.DataTable(data=df_dash.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='controls-and-graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df_dash, x='realestate_city_mapped', y=col_chosen, histfunc='avg')
    return fig



# Run the app
if __name__ == '__main__':
    app.run(debug=True)


