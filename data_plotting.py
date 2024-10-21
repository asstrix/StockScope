import plotly.graph_objects as go
from pathlib import Path
from data_download import period_spell
import os


# Export charts as png
def create_and_save_plot(logger, data, ticker, period):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['MA'], mode='lines', name='Moving Average'))
    fig.update_layout(title={'text': f"Цены закрытия за {period_spell(period)}", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    path = Path(__file__).parent
    try:
        os.makedirs(f"{path}/charts", exist_ok=True)
        fig.write_image(f"{path}/charts/{ticker}{period}.png")
        logger.debug(f"График сохранен в {path}/charts")
    except Exception as e:
        logger.debug(f"Ошибка сохранения графика: {e}")
