
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from backtest.engine import BacktestEngine  # Ensure this has run() method
from gui.polygon_api import fetch_polygon_data  # You'll create this

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

        # Run backtest button
        self.run_button = tk.Button(master, text="Run Backtest", command=self.run_backtest)
        self.run_button.grid(row=3, columnspan=2, pady=10)

        # Chart area
        self.chart_frame = tk.Frame(master)
        self.chart_frame.grid(row=4, column=0, columnspan=2)

    def run_backtest(self):
        ticker = self.ticker_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Format Error", "Please use YYYY-MM-DD format.")
            return

        try:
            data = fetch_polygon_data(ticker, start_date, end_date)
            equity, drawdown = BacktestEngine().run(data)

            # Clear old chart
            for widget in self.chart_frame.winfo_children():
                widget.destroy()

            # Plot
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

        except Exception as e:
            messagebox.showerror("Backtest Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = BacktestApp(root)
    root.mainloop()
