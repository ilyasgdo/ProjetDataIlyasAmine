# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import os

app = Dash()

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

CLEANED_DATA_PATH = os.path.join("data","cleaned", "cleaned.xlsx")
print(CLEANED_DATA_PATH)
print(CLEANED_DATA_PATH)
 
df = pd.read_excel(CLEANED_DATA_PATH)


#print(df)

fig = px.bar(df, x="Code du département", y="% Abs/Ins")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
