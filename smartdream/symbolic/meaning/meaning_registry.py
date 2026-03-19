# symbolic/drift/meaning_registry.py

import random
from collections import defaultdict
from datetime import datetime
import numpy as np

class SymbolicMeaningRegistry:
    def __init__(self):
        # Stores evolving meaning vectors for each symbol over time
        self.symbol_meanings = defaultdict(list)  # symbol → list of historical meaning vectors
        # Optional environmental influence pushing meaning evolution
        self.environmental_pressures = defaultdict(lambda: [0.0, 0.0, 0.0])
        # Tracks when each meaning update occurred
        self.symbol_timestamps = defaultdict(list)

    def get_current_meaning(self, symbol):
        # Returns the most recent meaning vector for a symbol
        if symbol not in self.symbol_meanings or not self.symbol_meanings[symbol]:
            return self._default_vector(symbol)
        return self.symbol_meanings[symbol][-1]

    def update_meaning(self, symbol, pressure_vector=None):
        # Updates the meaning of a symbol by applying cultural/environmental drift
        current = self.get_current_meaning(symbol)
        pressure = pressure_vector or self.environmental_pressures[symbol]
        new_vector = self._blend(current, pressure)
        self.symbol_meanings[symbol].append(new_vector)
        self.symbol_timestamps[symbol].append(datetime.now())

    def _default_vector(self, symbol):
        # Creates a stable random vector based on the symbol name
        seed = sum(ord(c) for c in symbol)
        random.seed(seed)
        return [random.uniform(-1, 1) for _ in range(3)]

    def _blend(self, old, pressure, drift_rate=0.05):
        # Blends an old vector toward a pressure vector using a fixed drift rate
        return [
            old[i] + drift_rate * (pressure[i] - old[i])
            for i in range(len(old))
        ]

    def get_all_symbols(self):
        # Returns list of all tracked symbols
        return list(self.symbol_meanings.keys())

    def get_symbol_history(self, symbol):
        # Returns the full history of a symbol’s meanings
        return self.symbol_meanings[symbol]

    def get_symbol_timestamps(self, symbol):
        # Returns the list of timestamps when each meaning update occurred
        return self.symbol_timestamps[symbol]

    def set_environmental_pressure(self, symbol, vector):
        # Manually defines environmental pressure for a given symbol
        self.environmental_pressures[symbol] = vector

    def calculate_entropy(self, symbol):
        # Calculates average stepwise change (volatility) in a symbol’s meaning over time
        history = self.symbol_meanings[symbol]
        if len(history) < 2:
            return 0.0
        diffs = [
            np.linalg.norm(
                np.array(history[i + 1]) - np.array(history[i])
            ) for i in range(len(history) - 1)
        ]
        return sum(diffs) / len(diffs) if diffs else 0.0

    def calculate_alignment_error(self, symbol, personal_vector):
        # Measures Euclidean distance between global meaning and agent’s personal interpretation
        global_vector = self.get_current_meaning(symbol)
        return np.linalg.norm(np.array(global_vector) - np.array(personal_vector))

    def calculate_alignment_oscillation(self, symbol, personal_vector, planck=0.1):
        # Models symbolic alignment as an oscillating signal (absorption or emission)
        global_vector = self.get_current_meaning(symbol)
        delta = np.array(global_vector) - np.array(personal_vector)
        frequency = np.linalg.norm(delta)
        energy_transfer = planck * frequency  # symbolic energy transfer
        return {
            "symbol": symbol,
            "frequency": frequency,           # how different the vectors are
            "energy": energy_transfer,        # symbolic analog to Planck-Energy
            "alignment_state": "absorption" if np.dot(global_vector, personal_vector) > 0 else "emission"
        }
