import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import logging
from flask import Flask, send_from_directory

app = dash.Dash(__name__, external_stylesheets=["assets/bootstrap.css"])

if __name__ == '__main__':
    app.run_server(host='10.206.100.41',port=8050)
   # webbrowser.open('http://10.206.100.41:8050/',autoraise=True)

app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.title = 'TINQAD'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

server = Flask(__name__)
app = dash.Dash(server=server)


