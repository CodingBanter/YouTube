import dash
from dotenv import load_dotenv
from os import environ, path
import dash_bootstrap_components as dbc


#establishes the base directory and loads environment variables
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


#Creating a Dash instance
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
server.config['SECRET_KEY'] = environ.get('SECRET_KEY')
