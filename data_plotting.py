import plotly.graph_objects as go
import pandas as pd


# def create_and_save_plot(data, ticker, period, filename=None):
def create_and_save_plot(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MA'], mode='lines', name='Moving Average'))
    fig.update_layout(title='Цена акций с течением времени')
    fig.show()