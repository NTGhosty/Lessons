import sqlite3
from datetime import datetime
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Контекстный менеджер для работы с БД"""
    
    def __init__(self, db_path='trading.db'):
        self.db_path = db_path
        self._conn = None
    
    @property
    def conn(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn
    
    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для подключения к БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            logger.error(f"Ошибка при работе с БД: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def init_db(self):
        """Инициализация таблиц"""
        with self.get_connection() as conn:
            c = conn.cursor()
            
            c.execute('''
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    figi TEXT,
                    price REAL,
                    signal TEXT,
                    prob REAL,
                    position_size REAL,
                    tp REAL,
                    sl REAL
                )
            ''')
            
            c.execute('''
                CREATE TABLE IF NOT EXISTS operations (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    figi TEXT,
                    operation_type TEXT,
                    price REAL,
                    quantity INTEGER,
                    status TEXT
                )
            ''')
            
            c.execute('''
                CREATE TABLE IF NOT EXISTS portfolio (
                    figi TEXT PRIMARY KEY,
                    name TEXT,
                    quantity INTEGER,
                    avg_price REAL,
                    current_price REAL,
                    pnl REAL
                )
            ''')
            
            c.execute('''
                CREATE TABLE IF NOT EXISTS performance (
                    timestamp TEXT,
                    balance REAL,
                    peak_balance REAL,
                    drawdown REAL
                )
            ''')
            
            conn.commit()
            logger.info("База данных инициализирована")


def init_db():
    """Инициализация БД"""
    db = DatabaseManager()
    db.init_db()


def save_signal(signal):
    """Сохранение сигнала в БД"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute('''
                INSERT INTO signals (timestamp, figi, price, signal, prob, position_size, tp, sl)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                signal['figi'],
                signal['price'],
                signal['signal'],
                signal['prob'],
                signal['position_size'],
                signal['tp'],
                signal['sl']
            ))
            logger.info(f"Сигнал сохранен: {signal['figi']}")
        except Exception as e:
            logger.error(f"Ошибка сохранения сигнала: {e}")


def save_operation(op):
    """Сохранение операции в БД"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute('''
                INSERT OR REPLACE INTO operations (id, timestamp, figi, operation_type, price, quantity, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                op['id'],
                op['timestamp'],
                op['figi'],
                op['operation_type'],
                op['price'],
                op['quantity'],
                op.get('status', 'completed')
            ))
            logger.info(f"Операция сохранена: {op['id']}")
        except Exception as e:
            logger.error(f"Ошибка сохранения операции: {e}")


def update_portfolio(figi, name, quantity, avg_price, current_price):
    """Обновление портфеля"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        c = conn.cursor()
        try:
            pnl = (current_price - avg_price) * quantity
            c.execute('''
                INSERT OR REPLACE INTO portfolio (figi, name, quantity, avg_price, current_price, pnl)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (figi, name, quantity, avg_price, current_price, pnl))
            logger.info(f"Портфель обновлен: {figi}")
        except Exception as e:
            logger.error(f"Ошибка обновления портфеля: {e}")


def get_total_pnl():
    """Получение общей PnL"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("SELECT SUM(pnl) as total_pnl FROM portfolio")
            result = c.fetchone()
            return result['total_pnl'] if result and result['total_pnl'] is not None else 0
        except Exception as e:
            logger.error(f"Ошибка получения общей PnL: {e}")
            return 0


def get_performance_history(days=30):
    """Получение истории просадки"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        c = conn.cursor()
        try:
            cutoff_date = (datetime.now() - __import__('datetime').timedelta(days=days)).isoformat()
            c.execute('''
                SELECT * FROM performance 
                WHERE timestamp >= ? 
                ORDER BY timestamp DESC
            ''', (cutoff_date,))
            return c.fetchall()
        except Exception as e:
            logger.error(f"Ошибка получения истории просадки: {e}")
            return []


def get_signals(limit=20):
    """Получение последних сигналов"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute('''
                SELECT * FROM signals 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            return c.fetchall()
        except Exception as e:
            logger.error(f"Ошибка получения сигналов: {e}")
            return []


def get_operations(limit=20):
    """Получение последних операций"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute('''
                SELECT * FROM operations 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            return c.fetchall()
        except Exception as e:
            logger.error(f"Ошибка получения операций: {e}")
            return []


def get_portfolio():
    """Получение портфеля"""
    db = DatabaseManager()
    
    with db.get_connection() as conn:
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM portfolio")
            return c.fetchall()
        except Exception as e:
            logger.error(f"Ошибка получения портфеля: {e}")
            return []


# Инициализация при импорте
init_db()