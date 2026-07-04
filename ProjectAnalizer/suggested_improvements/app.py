import streamlit as st
import sqlite3
import pandas as pd
from functools import lru_cache
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Tinkoff Trading Dashboard", layout="wide")
st.title("📊 Tinkoff Trading Dashboard")

# Инициализация подключения к БД с контекстным менеджером
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect('trading.db')
            cls._instance.conn.row_factory = sqlite3.Row
        return cls._instance
    
    def close(self):
        if self.conn:
            self.conn.close()

@lru_cache(maxsize=10)
def get_signals(limit=20):
    """Получение сигналов с кэшированием"""
    try:
        conn = DatabaseConnection()
        signals = pd.read_sql(
            "SELECT * FROM signals ORDER BY timestamp DESC LIMIT ?", 
            conn.conn, 
            params=(limit,)
        )
        return signals
    except Exception as e:
        logger.error(f"Ошибка получения сигналов: {e}")
        return pd.DataFrame()

@lru_cache(maxsize=10)
def get_operations(limit=20):
    """Получение операций с кэшированием"""
    try:
        conn = DatabaseConnection()
        ops = pd.read_sql(
            "SELECT * FROM operations ORDER BY timestamp DESC LIMIT ?", 
            conn.conn, 
            params=(limit,)
        )
        return ops
    except Exception as e:
        logger.error(f"Ошибка получения операций: {e}")
        return pd.DataFrame()

@lru_cache(maxsize=10)
def get_portfolio():
    """Получение портфеля с кэшированием"""
    try:
        conn = DatabaseConnection()
        portfolio = pd.read_sql("SELECT * FROM portfolio", conn.conn)
        return portfolio
    except Exception as e:
        logger.error(f"Ошибка получения портфеля: {e}")
        return pd.DataFrame()

def get_performance():
    """Получение истории просадки"""
    try:
        conn = DatabaseConnection()
        perf = pd.read_sql("SELECT * FROM performance ORDER BY timestamp", conn.conn)
        return perf
    except Exception as e:
        logger.error(f"Ошибка получения данных о просадке: {e}")
        return pd.DataFrame()

# Сигналы
st.subheader("Последние сигналы")
signals = get_signals()
if not signals.empty:
    st.dataframe(signals)
else:
    st.info("Нет доступных сигналов")

# Операции
st.subheader("Последние операции")
ops = get_operations()
if not ops.empty:
    st.dataframe(ops)
else:
    st.info("Нет доступных операций")

# Портфель
st.subheader("Портфель")
portfolio = get_portfolio()
if not portfolio.empty:
    st.dataframe(portfolio)
else:
    st.info("Нет данных о портфеле")

# Просадка
st.subheader("История просадки")
perf = get_performance()
if not perf.empty:
    try:
        fig = st.line_chart(
            perf.set_index('timestamp')[['drawdown']], 
            height=300
        )
        current_dd = perf['drawdown'].iloc[-1]
        st.metric("Текущая просадка", f"{current_dd:.2%}")
    except Exception as e:
        logger.error(f"Ошибка отображения графика просадки: {e}")
        st.error(f"Ошибка отображения графика: {str(e)}")
else:
    st.info("Нет данных о просадке")

# Кнопка сброса кэша (для разработки)
if st.sidebar.button("🔄 Сбросить кэш"):
    get_signals.cache_clear()
    get_operations.cache_clear()
    get_portfolio.cache_clear()
    st.success("Кэш сброшен")