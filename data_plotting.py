import plotly.graph_objects as go
from pathlib import Path
from data_download import period_spell
import os, pandas as pd


# Export charts as png
def create_and_save_plot(logger, data, ticker, period):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MA'], mode='lines', name='Moving Average'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['RSI'], mode='lines', name='RSI', yaxis='y2'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MACD'], mode='lines', name='MACD', yaxis='y3'))
    fig.update_layout(
        title={'text': f"Цена закрытия за {period_spell(period)}", 'x': 0.5, 'xanchor': 'center',
               'yanchor': 'top'},
        yaxis=dict(title='Close Price, MACD', ticklabelposition='outside left'),
        yaxis2=dict(title='RSI', overlaying='y', side='right', range=[0, 100]),
        yaxis3=dict(overlaying='y', side='left', ticklabelposition='inside'),
        width=1200,
        height=800,
        legend=dict(x=0, y=-0.25)
    )
    path = Path(__file__).parent
    try:
        os.makedirs(f"{path}/charts", exist_ok=True)
        fig.write_image(f"{path}/charts/{ticker}{period}.png")
        logger.debug(f"График сохранен в {path}\\charts")
    except Exception as e:
        logger.debug(f"Ошибка сохранения графика: {e}")
