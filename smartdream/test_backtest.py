import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
from backtest.engine import BacktestEngine
from agents.agent import Agent



# Create mock OHLCV data
df = pd.DataFrame({
    'timestamp': pd.date_range(start='2024-01-01', periods=20, freq='min'),
    'open': [100 + i for i in range(20)],
    'close': [100 + i + (1 if i % 2 == 0 else -1) for i in range(20)],
    'high': [105 for _ in range(20)],
    'low': [95 for _ in range(20)],
    'volume': [1000 for _ in range(20)]
})

# Initialize a few basic agents
agents = [Agent(name=f"Agent_{i}") for i in range(3)]

# Run the SMARTDREAM backtest engine
engine = BacktestEngine()
equity, drawdown = engine.run(df, agents)

# Print final results
print("Final Equity:", equity[-1])
print("Max Drawdown:", max(drawdown))
