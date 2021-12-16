import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pycoingecko import CoinGeckoAPI
import dash_bootstrap_components as dbc
import dash
from app import app


home_layout = html.Div([
                            html.Div(id="crypto_container", className="crypto_container",),
                            dcc.Interval(id="refresh_interval", interval=300000, n_intervals=0),
                        ], className="home_container")



def generate_crypto_item(crypto_iter):
    return_statement = html.Div([
                                    html.A(
                                    dbc.Card(
                                        [
                                            dbc.CardImg(src=crypto_iter["image"], top=True, className="crypto_img"),
                                            html.H5(children=str(crypto_iter["name"]),
                                            className="crypto_title",
                                            id=str(crypto_iter["name"])),
                                            html.H6(children= f"${'{:,}'.format(crypto_iter['current_price'])}",
                                            className="crypto_title",
                                            id=str(crypto_iter["current_price"])),
                                        ], className="card_container"), 

                                        href=f"/coin-info/{crypto_iter['id']}"),

                                ], className="crypto_item_container")
    
    return return_statement



@app.callback(
    Output('crypto_container', 'children'),
    Input('refresh_interval', 'n_intervals'))
def display_value(refresh):
    cg = CoinGeckoAPI()
    dataList = cg.get_coins_markets(vs_currency='usd')

    all_crypto = html.Div(
        id="crypto_return_container",
        className="crypto_return_container",
        children=[generate_crypto_item(i) for i in dataList]
        )

    return all_crypto