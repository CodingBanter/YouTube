import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from Apps import home, about, coinInfo


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/home':
        return home.home_layout
    if pathname == '/about':
        return about.about_layout
    if '/coin-info/' in pathname:
        coin = pathname.split('/')[-1]
        return coinInfo.create_layout(coin)
    else:
        return '404'



#starts the Dash server
if __name__ == '__main__':
    app.run_server(debug=True)
