import pandas as pd

class BacktestEngine:
    def __init__(self):
        self.equity_curve = []
        self.drawdown_curve = []
        self.initial_equity = 100_000
        self.current_equity = self.initial_equity
        self.peak_equity = self.initial_equity

    def run(self, df: pd.DataFrame, agents: list):
        """
        Runs a SMARTDREAM-compatible backtest over time-indexed OHLCV data.
        Each row is treated as a timestep; agents update and respond sequentially.
        """
        equity_log = []
        drawdown_log = []

        for idx, row in df.iterrows():
            timestamp = row['timestamp']
            price = row['close']
            signal_strength = self._generate_signal(row)
            fever_flag = abs(signal_strength) > 0.9

            step_profit = 0
            for agent in agents:
                agent_output = agent.perceive_and_act(timestamp=timestamp,
                                                     confidence=abs(signal_strength),
                                                     fever_flag=fever_flag)
                pnl = self._apply_action(agent_output, price)

                # Update agent memory or fitness here
                if hasattr(agent, 'memory'):
                    agent.memory.record_event(
                        signal=agent_output,
                        timestamp=timestamp,
                        metadata={
                            "signal_strength": signal_strength,
                            "price": price,
                            "pnl": pnl
                        },
                        tags=["backtest"],
                        source="BacktestEngine",
                        context={"timestep": idx}
                    )
                if hasattr(agent, 'vitality'):
                    if pnl > 0:
                        agent.vitality.boost(pnl * 0.001)  # reward vitality
                    elif pnl < 0:
                        agent.vitality.stress(abs(pnl) * 0.001)  # penalize vitality
                    agent.vitality.tick()

                step_profit += pnl

            self.current_equity += step_profit
            equity_log.append(self.current_equity)
            self.peak_equity = max(self.peak_equity, self.current_equity)
            drawdown = self.peak_equity - self.current_equity
            drawdown_log.append(drawdown)

        return equity_log, drawdown_log

    def _apply_action(self, action, price):
        """
        Agent-driven logic: agents maintain their own position state.
        Profit/loss is realized only when positions are closed or reversed.
        """
        pnl = 0
        agent = action.get('agent')  # Must pass agent reference in action dict
        decision = action.get('decision')  # 'buy', 'sell', 'hold'

        if not hasattr(agent, 'position'):
            agent.position = 0  # 0 = flat, 1 = long, -1 = short
            agent.entry_price = None

        if decision == 'buy':
            if agent.position == 0:
                agent.position = 1
                agent.entry_price = price
            elif agent.position == -1:  # Closing short
                pnl = agent.entry_price - price
                agent.position = 0
                agent.entry_price = None

        elif decision == 'sell':
            if agent.position == 0:
                agent.position = -1
                agent.entry_price = price
            elif agent.position == 1:  # Closing long
                pnl = price - agent.entry_price
                agent.position = 0
                agent.entry_price = None

        elif decision == 'hold':
            pass  # no position change

        return pnl

    def _generate_signal(self, row):
        """Replace with signal logic or external hook."""
        return (row['close'] - row['open']) / row['open']
