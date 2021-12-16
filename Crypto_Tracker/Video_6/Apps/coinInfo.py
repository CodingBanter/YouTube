import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pycoingecko import CoinGeckoAPI
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import time
import dash
from app import app


#layout that gets return to index.py when user clicks on crypto item
def create_layout(coin):
    return  html.Div([
                        dcc.Store(id='coinId_memory', data = coin),
                        html.Div(id="coinInfo_container", className="coinInfo_container"),
                        dcc.Loading(
                            id='loading_container',
                            type='graph',
                            children=html.Div([
                                dbc.Row([
                                    dbc.Col(
                                    dcc.Graph(id="coin_main_chart"), className='graph_col', width=8
                                    ),
                                    dbc.Col(
                                    dbc.Table(id="price_statistics", striped=True, borderless=True, hover=True, size='sm'), 
                                    className='table_col', width=4
                                    )
                                ], className='row_container'),
                            ], id="chart_stats_container")
                        ),
                        dcc.Interval(id="coinInfo_refresh_interval", interval=300000, n_intervals=0),
                    ], className="coinInfo_main_container")  

        
    
#configures each row for the table comp 
def configure_table(title, api_string, stat_data):
    try:
        row = html.Tr([html.Td(f"{title}:"), html.Td(f"{api_string[1]}{'{:,}'.format(stat_data[0][api_string[0]])}")])
    except:
        row = html.Tr([html.Td(title), html.Td(f"N/A")])
    return row

#constructs the table comp. returns to callback to be output
def price_Statistics(stat_data):
    time.sleep(1)
    #dict defining titles, cg apis, and prefix for display
    table_dict = {'Market Rank': ['market_cap_rank', '#'], 'Market Cap': ['market_cap', '$'], 'Total Volume': ['total_volume', '$'],
                  '24hr High': ['high_24h', '$'], '24hr Low': ['low_24h', '$'], 'Total Supply': ['total_supply', ''], 'Max Supply': ['max_supply', ''],
                  'Circulating Supply': ['circulating_supply', '']}
    arrRow = []
    #loops through dict and configure each row
    for key, value in table_dict.items():
        row = configure_table(key, value, stat_data)   
        arrRow.append(row)

    table_body = [html.Tbody(arrRow)]
    table_header = [html.Thead(html.Th(f"{stat_data[0]['symbol'].upper()} Price Statistics", colSpan="2"), className='text-center')]
    table = table_body + table_header
    return table




@app.callback(
    Output('coinInfo_container', 'children'),
    Output('coin_main_chart', 'figure'),
    Output('price_statistics', 'children'),
    [Input('coinInfo_refresh_interval', 'n_intervals'), Input('coinId_memory', 'data')])
def display_coinInfo(refresh, data):
    cg = CoinGeckoAPI()

    #Get current data (name, price, market, ... including exchange tickers) for a coin.
    coin_ID_data = cg.get_coins_markets(ids=data, vs_currency = 'usd', price_change_percentage="1h,24h,7d,14d,30d")

    #Get historical market data include price, market cap, and 24h volume (granularity auto)
    main_chart_data = cg.get_coin_market_chart_by_id(id=data, vs_currency='usd', days='max', interval='daily')

    #strip out time and price list from df to be plotted
    df = pd.DataFrame(main_chart_data)
    arrTime = []
    arrRecorded_price = []
    for price in df["prices"]:
        time, recorded_price = price
        arrTime.append(time)
        arrRecorded_price.append(recorded_price)
    #creating new df with time and price seperated out
    main_chart_df = pd.DataFrame({"Time": arrTime, "Price": arrRecorded_price})
    main_chart_df['Time'] = pd.to_datetime(main_chart_df['Time'],unit='ms')

    fig = px.line(main_chart_df, x="Time", y="Price", title=f"{coin_ID_data[0]['name'].upper()} to USD Chart")
    fig.update_layout({
        'font_color': 'white',
        'plot_bgcolor': 'white',
        'paper_bgcolor': '#343a40',
        'hovermode':'y unified'
        })

    return (
        html.Div([
            html.H1(f"{coin_ID_data[0]['name']} ({coin_ID_data[0]['symbol'].upper()})"),
            html.H4(f"Current Price: ${'{:,}'.format(coin_ID_data[0]['current_price'])}"),
            # html.P(coin_ID_data['description']['en']),
        ], className="coinInfo_return_container"), 
        fig, 
        price_Statistics(coin_ID_data))