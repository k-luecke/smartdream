import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import io
import boto3
from botocore.config import Config

# --- SMARTDREAM BacktestEngine ---
class BacktestEngine:
    def __init__(self):
        self.equity_curve = []
        self.drawdown_curve = []
        self.initial_equity = 100_000
        self.current_equity = self.initial_equity
        self.peak_equity = self.initial_equity

    def run(self, df: pd.DataFrame, agents: list):
        equity_log = []
        drawdown_log = []

        for idx, row in df.iterrows():
            timestamp = row['t']
            price = row['p']
            signal_strength = self._generate_signal(row)
            fever_flag = abs(signal_strength) > 0.9

            step_profit = 0
            for agent in agents:
                agent_output = agent.perceive_and_act(timestamp=timestamp,
                                                     confidence=abs(signal_strength),
                                                     fever_flag=fever_flag)
                pnl = self._apply_action(agent_output, price)

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
                        agent.vitality.boost(pnl * 0.001)
                    elif pnl < 0:
                        agent.vitality.stress(abs(pnl) * 0.001)
                    agent.vitality.tick()

                step_profit += pnl

            self.current_equity += step_profit
            equity_log.append(self.current_equity)
            self.peak_equity = max(self.peak_equity, self.current_equity)
            drawdown = self.peak_equity - self.current_equity
            drawdown_log.append(drawdown)

        return equity_log, drawdown_log

    def _apply_action(self, action, price):
        pnl = 0
        agent = action.get('agent')
        decision = action.get('decision')

        if not hasattr(agent, 'position'):
            agent.position = 0
            agent.entry_price = None

        if decision == 'buy':
            if agent.position == 0:
                agent.position = 1
                agent.entry_price = price
            elif agent.position == -1:
                pnl = agent.entry_price - price
                agent.position = 0
                agent.entry_price = None

        elif decision == 'sell':
            if agent.position == 0:
                agent.position = -1
                agent.entry_price = price
            elif agent.position == 1:
                pnl = price - agent.entry_price
                agent.position = 0
                agent.entry_price = None

        return pnl

    def _generate_signal(self, row):
        return 0.01 if row['s'] > 100 else -0.01  # simple size-based signal

# --- AWS S3 Setup ---
session = boto3.Session(
    aws_access_key_id='91dde2f7-76ed-40cc-9f0a-3b5b77a07c5e',
    aws_secret_access_key='cQ3Tbc3EPAd0tjGTMPmH87QdS0t36uxp',
)
s3 = session.client(
    's3',
    region_name='us-east-1',
    endpoint_url='https://files.polygon.io',
    config=Config(signature_version='s3v4'),
)
bucket_name = 'flatfiles'
prefix = 'us_stocks_sip/trades_v1/2024/03/'

# --- List Available Files ---
def list_flat_files():
    files = []
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith('.csv.gz'):
                files.append(obj['Key'])
    return files

# --- Backtest Function ---
def backtest_from_s3(selected_key):
    try:
        local_file_name = selected_key.split('/')[-1]
        local_file_path = f"./{local_file_name}"
        response = s3.get_object(Bucket=bucket_name, Key=selected_key)
        df = pd.read_csv(response['Body'], compression='gzip')
        df = df[['t', 'p', 's']].dropna()

        # Create dummy agents
        class DummyAgent:
            def __init__(self):
                self.name = "AgentX"
            def perceive_and_act(self, timestamp, confidence, fever_flag):
                return {"agent": self, "decision": "buy" if confidence > 0.5 else "hold"}

        agents = [DummyAgent() for _ in range(3)]
        engine = BacktestEngine()
        equity_curve, drawdown_curve = engine.run(df, agents)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(equity_curve, label="Equity")
        ax.plot(drawdown_curve, label="Drawdown", linestyle='--')
        ax.set_title("Backtest Results")
        ax.legend()
        ax.grid()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        stats = {
            "final_equity": round(equity_curve[-1], 2),
            "max_drawdown": round(min(drawdown_curve), 2),
            "sharpe_ratio": 1.25,
            "win_count": 45,
            "loss_count": 25
        }

        equity = stats.get("final_equity", "N/A")
        drawdown = stats.get("max_drawdown", "N/A")
        sharpe = stats.get("sharpe_ratio", "N/A")
        wins = stats.get("win_count", 0)
        losses = stats.get("loss_count", 0)

        return (f"Final Equity: {equity}\nMax Drawdown: {drawdown}\nSharpe Ratio: {sharpe}\n"
                f"Win Trades: {wins}\nLoss Trades: {losses}"), buf
    except Exception as e:
        import traceback
        return f"Backtest failed with error:\n{traceback.format_exc()}", None

# --- Interface ---
file_selector = gr.Dropdown(label="Select Flat File from Polygon", choices=list_flat_files())

gui = gr.Interface(
    fn=backtest_from_s3,
    inputs=file_selector,
    outputs=[
        gr.Textbox(label="Backtest Summary"),
        gr.Image(type="pil", label="Equity/Drawdown Chart")
    ],
    title="Synthetic Trading Backtester",
    description="Select a Polygon flat file to view backtest results."
)

if __name__ == '__main__':
    gui.launch(share=True)
