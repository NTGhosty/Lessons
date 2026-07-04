# data.py
import pandas as pd
from datetime import datetime, timedelta, timezone
from t_tech.invest import AsyncClient, CandleInterval
from config import Config, FIGI_LIST

class DataFetcher:
    """Класс для загрузки данных с Tinkoff и из БД."""
    
    def __init__(self):
        self.config = Config()
        self.client = None
    
    async def get_client(self):
        """Получение клиента Tinkoff (создается один раз)."""
        if not self.client:
            self.client = AsyncClient(self.config.TINKOFF_TOKEN)
        return self.client

    def quote_to_float(self, q):
        """Преобразование цены из объекта Quote в float."""
        return q.units + q.nano / 1e9

    async def fetch_candles(self, figi: str, timeframe: str, days: int):
        """Загрузка свечей с Tinkoff."""
        client = await self.get_client()
        
        # Исправленный маппинг таймфреймов (12ч -> 4 часа)
        TIMEFRAME_MAP = {
            "1м": CandleInterval.CANDLE_INTERVAL_1_MIN,
            "5м": CandleInterval.CANDLE_INTERVAL_5_MIN,
            "30м": CandleInterval.CANDLE_INTERVAL_30_MIN,
            "1ч": CandleInterval.CANDLE_INTERVAL_HOUR,
            "4ч": CandleInterval.CANDLE_INTERVAL_4_HOUR,  # Исправлено с 30мин на 4 часа
            "1д": CandleInterval.CANDLE_INTERVAL_DAY,
            "1н": CandleInterval.CANDLE_INTERVAL_WEEK,
            "1М": CandleInterval.CANDLE_INTERVAL_MONTH,
        }

        interval = TIMEFRAME_MAP.get(timeframe)
        if not interval:
            raise ValueError(f"Неизвестный таймфрейм: {timeframe}")

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
                'close': self.quote_to_float(c.close),
                'high': self.quote_to_float(c.high),
                'low': self.quote_to_float(c.low),
                'open': self.quote_to_float(c.open),
                'volume': c.volume
            })
        return pd.DataFrame(data)

    async def fetch_current_price(self, figi: str):
        """Загрузка текущей цены."""
        client = await self.get_client()
        
        moscow_tz = timezone(timedelta(hours=3))
        now = datetime.now(moscow_tz)
        
        candles = await client.market_data.get_candles(
            figi=figi,
            from_=now - timedelta(minutes=2),
            to=now,
            interval=CandleInterval.CANDLE_INTERVAL_1_MIN
        )
        
        return self.quote_to_float(candles.candles[-1].close) if candles.candles else None

    def get_db_signals(self, limit: int = 20):
        """Загрузка сигналов из БД."""
        import db as db_module
        with db_module.get_db_connection(self.config.DB_PATH) as conn:
            return db_module.get_signals(conn, limit=limit)

    def get_db_operations(self, limit: int = 20):
        """Загрузка операций из БД."""
        import db as db_module
        with db_module.get_db_connection(self.config.DB_PATH) as conn:
            return db_module.get_operations(conn, limit=limit)

    def get_db_portfolio(self):
        """Загрузка портфеля из БД."""
        import db as db_module
        with db_module.get_db_connection(self.config.DB_PATH) as conn:
            return db_module.get_portfolio(conn)

    def get_db_performance(self, limit: int = 100):
        """Загрузка истории просадки из БД."""
        import db as db_module
        with db_module.get_db_connection(self.config.DB_PATH) as conn:
            return db_module.get_performance(conn, limit=limit)