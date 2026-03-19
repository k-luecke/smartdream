from collections import defaultdict
import random

class ImprintingEngine:
    """
    Tracks symbolic imprints acquired during an agent's development.
    Symbol strength, clarity, and volatility affect memory and schema formation.
    """
    def __init__(self):
        self.symbol_weights = defaultdict(float)  # symbol -> weight
        self.age = 0

    def imprint(self, symbol, strength=1.0):
        """
        Reinforce a symbolic tag.

        Args:
            symbol (str): symbolic content
            strength (float): imprinting intensity
        """
        self.symbol_weights[symbol] += strength

    def decay(self, rate=0.01):
        """
        Apply global decay to all symbols.

        Args:
            rate (float): decay factor per tick
        """
        for sym in list(self.symbol_weights):
            self.symbol_weights[sym] *= (1 - rate)
            if self.symbol_weights[sym] < 0.01:
                del self.symbol_weights[sym]

    def get_dominant_symbols(self, top_n=3):
        sorted_syms = sorted(self.symbol_weights.items(), key=lambda x: -x[1])
        return [s for s, w in sorted_syms[:top_n]]

    def get_symbol_weights(self):
        return dict(self.symbol_weights)

    def get_clarity(self):
        """
        Return a clarity score between 0 and 1 representing symbolic coherence.
        """
        if not self.symbol_weights:
            return 0.0
        weights = list(self.symbol_weights.values())
        max_w = max(weights)
        total_w = sum(weights)
        return max_w / total_w if total_w > 0 else 0.0

    def imprint_batch(self, symbols):
        for sym in symbols:
            self.imprint(sym, strength=random.uniform(0.5, 1.0))
