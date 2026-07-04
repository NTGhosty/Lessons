import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

TINKOFF_TOKEN = os.getenv("TINKOFF_TOKEN", "t.z9PFXH-Gq1TwRENMkEgeU8DNw78JU2ihIsxiq7LIv7jAdjV3X_eOxCubtEcVwfa-SxO5Oc0Yp7qEUOvwyfHjnQ")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7817891315:AAHJApadgirYo7RnR14u5OwrOpO-lj5HMjE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7817891315")

FIGI_LIST = [
    "BBG004731354",  # Роснефть
    "BBG004730N88",  # Сбербанк
    "BBG004S68614",  # Газпром
    "BBG004731032",  # Лукойл
]

# Risk management
MAX_RISK_PER_TRADE = float(os.getenv("MAX_RISK_PER_TRADE", "0.02"))
MAX_RISK_PER_ASSET = float(os.getenv("MAX_RISK_PER_ASSET", "0.05"))
MAX_TOTAL_PORTFOLIO_RISK = float(os.getenv("MAX_TOTAL_PORTFOLIO_RISK", "0.10"))
MAX_DRAWDOWN = float(os.getenv("MAX_DRAWDOWN", "0.15"))
INITIAL_CAPITAL = int(os.getenv("INITIAL_CAPITAL", "1_000_000"))

# Замените на свой account_id (получите через get_accounts)
ACCOUNT_ID = os.getenv("ACCOUNT_ID", "1855784757")

# Таймфреймы для анализа (в минутах)
TIMEFRAMES = {
    "1m": 1,
    "10m": 10,
    "1h": 60,
    "1d": 1440,
}

# Валидация конфигурации
def validate_config():
    """Валидация настроек"""
    errors = []
    
    if not TINKOFF_TOKEN.startswith("t."):
        errors.append("Некорректный токен Tinkoff")
    
    if not TELEGRAM_BOT_TOKEN.startswith("7817891315:"):
        errors.append("Некорректный токен Telegram бота")
    
    for figi in FIGI_LIST:
        if len(figi) != 12:
            errors.append(f"Некорректный FIGI: {figi}")
    
    if MAX_RISK_PER_TRADE > 0.1 or MAX_RISK_PER_TRADE < 0:
        errors.append("Некорректное значение MAX_RISK_PER_TRADE")
    
    if INITIAL_CAPITAL <= 0:
        errors.append("INITIAL_CAPITAL должно быть положительным")
    
    return errors

# Проверка при импорте
config_errors = validate_config()
if config_errors:
    import warnings
    warnings.warn(f"Конфигурация содержит ошибки:\n" + "\n".join(config_errors))