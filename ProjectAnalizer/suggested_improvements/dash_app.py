import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import asyncio
from datetime import datetime, timedelta, timezone
from t_tech.invest import AsyncClient, CandleInterval
from config import TINKOFF_TOKEN, FIGI_LIST

app = dash.Dash(__name__)
app.title = "Tinkoff Market Monitor"

# Сопоставление таймфреймов с интервалами Tinkoff
TIMEFRAME_MAP = {
    "1м": CandleInterval.CANDLE_INTERVAL_1_MIN,
    "5м": CandleInterval.CANDLE_INTERVAL_5_MIN,
    "30м": CandleInterval.CANDLE_INTERVAL_30_MIN,
    "1ч": CandleInterval.CANDLE_INTERVAL_HOUR,
    "4ч": CandleInterval.CANDLE_INTERVAL_4_HOUR,
    "1д": CandleInterval.CANDLE_INTERVAL_DAY,
    "1н": CandleInterval.CANDLE_INTERVAL_WEEK,
    "1М": CandleInterval.CANDLE_INTERVAL_MONTH if hasattr(CandleInterval, 'CANDLE_INTERVAL_MONTH') else None,
}

# Макс. периоды (в днях) для каждого таймфрейма
MAX_PERIOD_DAYS = {
    "1м": 1,
    "5м": 7,
    "30м": 30,
    "1ч": 60,
    "4ч": 180,
    "1д": 365,
    "1н": 730,
    "1М": 1825 if TIMEFRAME_MAP.get("1М") else None,
}

# Кэш для хранения данных графиков
graph_cache = {}


def quote_to_float(q):
    """Конвертация цены из объекта Tinkoff"""
    return q.units + q.nano / 1e9


async def fetch_candles(figi, timeframe, days):
    """Получение свечей с обработкой ошибок"""
    try:
        interval = TIMEFRAME_MAP[timeframe]
        if not interval:
            raise ValueError(f"Неподдерживаемый таймфрейм: {timeframe}")
        
        async with AsyncClient(TINKOFF_TOKEN) as client:
            moscow_tz = timezone(timedelta(hours=3))
            now = datetime.now(moscow_tz)
            from_time = now - timedelta(days=days)
            
            candles = await client.market_data.get_candles(
                figi=figi,
                from_=from_time,
                to=now,
                interval=interval
            )
            
            data = []
            for c in candles.candles:
                data.append({
                    'time': c.time,
                    'close': quote_to_float(c.close),
                    'high': quote_to_float(c.high),
                    'low': quote_to_float(c.low),
                    'open': quote_to_float(c.open),
                    'volume': c.volume
                })
            
            return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception as e:
        print(f"Ошибка получения свечей для {figi}: {e}")
        return pd.DataFrame()


async def fetch_current_price(figi):
    """Получение текущей цены с обработкой ошибок"""
    try:
        async with AsyncClient(TINKOFF_TOKEN) as client:
            moscow_tz = timezone(timedelta(hours=3))
            now = datetime.now(moscow_tz)
            
            candles = await client.market_data.get_candles(
                figi=figi,
                from_=now - timedelta(minutes=2),
                to=now,
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN
            )
            
            return quote_to_float(candles.candles[-1].close) if candles.candles else None
    except Exception as e:
        print(f"Ошибка получения текущей цены для {figi}: {e}")
        return None


# === LAYOUT ===
app.layout = html.Div(
    style={
        'fontFamily': '"Segoe UI", sans-serif',
        'padding': '20px',
        'backgroundColor': '#f9f9f9'
    },
    children=[
        html.H1("📈 Tinkoff Market Monitor", style={'textAlign': 'center', 'marginBottom': '20px'}),

        html.Div([
            html.Div([
                html.Label("Актив:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='figi-selector',
                    options=[{'label': figi, 'value': figi} for figi in FIGI_LIST],
                    value=FIGI_LIST[0] if FIGI_LIST else "",
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '45%', 'display': 'inline-block'}),

            html.Div([
                html.Label("Таймфрейм:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='timeframe-selector',
                    options=[
                        {"label": "1 минута", "value": "1м"},
                        {"label": "5 минут", "value": "5м"},
                        {"label": "30 минут", "value": "30м"},
                        {"label": "1 час", "value": "1ч"},
                        {"label": "4 часа", "value": "4ч"},
                        {"label": "1 день", "value": "1д"},
                        {"label": "1 неделя", "value": "1н"},
                    ],
                    value="1ч",
                    clearable=False,
                    style={'width': '100%'}
                )
            ], style={'width': '45%', 'display': 'inline-block', 'marginLeft': '5%'})
        ], style={'marginBottom': '20px'}),

        dcc.Graph(id='live-graph',
                  style={'height': '65vh', 'borderRadius': '8px', 'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'}),

        html.Div(id='current-price', style={'textAlign': 'center', 'fontSize': '1.5rem', 'marginTop': '15px'}),

        dcc.Interval(id='interval-component', interval=10_000, n_intervals=0)
    ]
)


@app.callback(
    [Output('live-graph', 'figure'),
     Output('current-price', 'children')],
    [Input('figi-selector', 'value'),
     Input('timeframe-selector', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph_and_price(selected_fig, timeframe, n_intervals):
    """Обновление графика и цены с обработкой ошибок"""
    if not selected_fig or not timeframe:
        fig = go.Figure()
        fig.update_layout(title="Выберите актив и таймфрейм")
        return fig, "Ожидание выбора"

    days = MAX_PERIOD_DAYS.get(timeframe)
    if not days:
        fig = go.Figure()
        fig.update_layout(title=f"Неподдерживаемый таймфрейм: {timeframe}")
        return fig, f"Ошибка: неподдерживаемый таймфрейм {timeframe}"

    try:
        # Используем event loop из main thread
        loop = asyncio.get_event_loop()
        
        df = loop.run_until_complete(fetch_candles(selected_fig, timeframe, days))
        current_price = loop.run_until_complete(fetch_current_price(selected_fig))
        
        loop.close()
    except Exception as e:
        print(f"Ошибка в callback: {e}")
        fig = go.Figure()
        fig.update_layout(title=f"Ошибка загрузки данных: {str(e)}")
        return fig, "Ошибка загрузки данных"

    fig = go.Figure()

    if not df.empty:
        fig.add_trace(go.Candlestick(
            x=df['time'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Цена'
        ))

    # Текущая цена (только для краткосрочных таймфреймов)
    short_term_timeframes = ["1м", "5м", "30м", "1ч", "4ч"]
    if current_price and timeframe in short_term_timeframes:
        moscow_tz = timezone(timedelta(hours=3))
        now = datetime.now(moscow_tz)
        fig.add_trace(go.Scatter(
            x=[now],
            y=[current_price],
            mode='markers',
            marker=dict(color='red', size=8),
            name='Текущая цена'
        ))
        price_text = f"Текущая цена: {current_price:,.0f}"
    else:
        price_text = "Цена недоступна"

    fig.update_layout(
        title=f"Актив: {selected_fig} | Таймфрейм: {timeframe}",
        xaxis_title="Время",
        yaxis_title="Цена",
        hovermode='x unified',
        showlegend=False,
        margin=dict(l=50, r=30, t=50, b=50),
        xaxis_rangeslider_visible=False,
        dragmode='zoom'
    )

    return fig, price_text


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8050, debug=True)