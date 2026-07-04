import pandas as pd
import numpy as np

def simple_backtest(signals_df, capital=1_000_000):
    """Простой бэктест с обработкой ошибок"""
    if signals_df.empty:
        return pd.DataFrame()
    
    signals_df = signals_df.copy()
    
    # Валидация данных
    required_cols = ['prob', 'tp', 'price', 'sl', 'position_size']
    missing_cols = [col for col in required_cols if col not in signals_df.columns]
    if missing_cols:
        raise ValueError(f"Отсутствуют колонки: {missing_cols}")
    
    # Защита от деления на ноль
    price_sl_diff = signals_df['price'] - signals_df['sl']
    signals_df['return'] = (
        signals_df['prob'] * (signals_df['tp'] - signals_df['price']) / 
        np.where(price_sl_diff != 0, price_sl_diff, 1)
    ) - (1 - signals_df['prob'])
    
    # Валидация размера позиции
    signals_df['position_size'] = signals_df['position_size'].clip(lower=0.01, upper=0.5)
    
    signals_df['pnl'] = signals_df['return'] * capital * signals_df['position_size']
    signals_df['cum_pnl'] = signals_df['pnl'].cumsum()
    
    # Добавление метрик
    signals_df['win_rate'] = (signals_df['pnl'] > 0).mean()
    signals_df['total_return'] = signals_df['cum_pnl'].iloc[-1] / capital if not signals_df.empty else 0
    
    return signals_df


def calculate_max_drawdown(cumulative_returns):
    """Расчет максимальной просадки"""
    peak = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - peak) / peak
    max_dd = drawdown.min()
    return max_dd


def analyze_backtest(signals_df, capital=1_000_000):
    """Анализ результатов бэктеста"""
    if signals_df.empty:
        return pd.DataFrame()
    
    backtest_results = {
        'total_trades': len(signals_df),
        'winning_trades': (signals_df['pnl'] > 0).sum(),
        'losing_trades': (signals_df['pnl'] < 0).sum(),
        'win_rate': round((signals_df['pnl'] > 0).mean() * 100, 2),
        'total_pnl': signals_df['cum_pnl'].iloc[-1],
        'total_return_pct': round(signals_df['cum_pnl'].iloc[-1] / capital * 100, 2),
        'max_drawdown': calculate_max_drawdown(signals_df['cum_pnl']),
        'avg_win': signals_df[signals_df['pnl'] > 0]['pnl'].mean(),
        'avg_loss': abs(signals_df[signals_df['pnl'] < 0]['pnl'].mean()),
        'profit_factor': round(
            (signals_df[signals_df['pnl'] > 0]['pnl'].sum() / 
             abs(signals_df[signals_df['pnl'] < 0]['pnl'].sum())) if not signals_df.empty else 0, 2
        )
    }
    
    return pd.DataFrame([backtest_results])