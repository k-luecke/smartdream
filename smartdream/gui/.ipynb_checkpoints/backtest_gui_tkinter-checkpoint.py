import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import boto3
from botocore.config import Config
import pandas as pd
import io
import os

from backtest.engine import BacktestEngine  # Now implemented to support equity/drawdown + agent memory
from gui.polygon_api import fetch_polygon_data
from gui.csv_backtest_helper import run_sequential_csv_backtest, load_flat_file

class BacktestApp:
    def __init__(self, master):
        self.master = master
        master.title("SMARTDREAM Backtest GUI")

        # Ticker input
        tk.Label(master, text="Ticker Symbol:").grid(row=0, column=0, sticky='e')
        self.ticker_entry = tk.Entry(master)
        self.ticker_entry.insert(0, "SPY")
        self.ticker_entry.grid(row=0, column=1)

        # Start date
        tk.Label(master, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, sticky='e')
        self.start_date_entry = tk.Entry(master)
        self.start_date_entry.insert(0, "2024-01-01")
        self.start_date_entry.grid(row=1, column=1)

        # End date
        tk.Label(master, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='e')
        self.end_date_entry = tk.Entry(master)
        self.end_date_entry.insert(0, "2024-01-31")
        self.end_date_entry.grid(row=2, column=1)

        # Run backtest (Polygon.io) button
        self.run_button = tk.Button(master, text="Run Polygon Backtest", command=self.run_polygon_backtest)
        self.run_button.grid(row=3, columnspan=2, pady=5)

        # Run backtest (CSV) button
        self.csv_button = tk.Button(master, text="Run Backtest on CSV Files",
                                    command=self.run_csv_backtest)
        self.csv_button.grid(row=4, columnspan=2, pady=5)

        # Run backtest from S3 button
        self.s3_button = tk.Button(master, text="Run Backtest from S3 Bucket", command=self.run_s3_backtest)
        self.s3_button.grid(row=5, columnspan=2, pady=5)

        # Chart area
        self.chart_frame = tk.Frame(master)
        self.chart_frame.grid(row=6, column=0, columnspan=2)

    def run_polygon_backtest(self):
        ticker = self.ticker_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Format Error", "Please use YYYY-MM-DD format.")
            return

        try:
            data = fetch_polygon_data(ticker, start_date, end_date)
            from agents.agent import Agent
            agent_pool = [Agent(name=f"Agent_{i}") for i in range(5)]
            equity, drawdown = BacktestEngine().run(data, agent_pool)
            self.plot_results(equity, drawdown)

        except Exception as e:
            messagebox.showerror("Backtest Error", str(e))

    def run_csv_backtest(self):
        try:
            from agents.agent import Agent
            agent_count = 5  # Configurable number of agents
            agent_pool = [Agent(name=f"Agent_{i}") for i in range(agent_count)]
            result = run_sequential_csv_backtest(agent_pool)
            if result:
                equity, drawdown = result
                self.plot_results(equity, drawdown)
        except Exception as e:
            messagebox.showerror("CSV Backtest Error", str(e))

    def run_s3_backtest(self):
        try:
            session = boto3.Session(
                aws_access_key_id=os.getenv("polygon_aws_access_key_id"),
                aws_secret_access_key=os.getenv("polygon_aws_secret_access_key"),
            )

            s3 = session.client(
                's3',
                endpoint_url='https://files.polygon.io',
                config=Config(signature_version='s3v4')
            )

            bucket_name = 'flatfiles'
            prefix = filedialog.askstring("S3 Prefix", "Enter folder or prefix path:")

            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.csv') or obj['Key'].endswith('.csv.gz')]

            from agents.agent import Agent
            agent_pool = [Agent(name=f"Agent_{i}") for i in range(5)]

            all_equity, all_drawdown = [], []
            for key in sorted(files):
                obj = s3.get_object(Bucket=bucket_name, Key=key)
                try:
                    df = pd.read_csv(io.BytesIO(obj['Body'].read()), compression='infer', parse_dates=['timestamp'])
                except Exception as e:
                    messagebox.showwarning("CSV Schema Error", f"Could not load {key}: {e}")
                    continue
                df = df.sort_values('timestamp')
                equity, drawdown = BacktestEngine().run(df, agent_pool)
                all_equity.extend(equity)
                all_drawdown.extend(drawdown)

            self.plot_results(all_equity, all_drawdown)

        except Exception as e:
            messagebox.showerror("S3 Backtest Error", str(e))

    def plot_results(self, equity, drawdown):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(2, 1, figsize=(6, 5), dpi=100)
        ax[0].plot(equity, label='Equity')
        ax[0].set_title('Equity Curve')
        ax[0].legend()

        ax[1].plot(drawdown, color='red', label='Drawdown')
        ax[1].set_title('Drawdown Curve')
        ax[1].legend()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = BacktestApp(root)
    root.mainloop()