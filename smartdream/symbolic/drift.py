import numpy as np

class SymbolicDrift:
    """
    Tracks symbolic reinterpretation, entropy, and drift rate for agents.
    This helps define internal symbolic instability and alignment potential.
    """

    def __init__(self):
        self.last_symbol = None
        self.symbol_history = []
        self.entropy_score = 0.0
        self.drift_rate = 0.0

    def update(self, current_symbol):
        """
        Update drift history with the current symbolic imprint.
        :param current_symbol: string label of agent's symbolic identity
        """
        if self.last_symbol is not None and current_symbol != self.last_symbol:
            self.symbol_history.append(current_symbol)

        # Update entropy (how frequently the symbol changes)
        unique, counts = np.unique(self.symbol_history, return_counts=True)
        probabilities = counts / np.sum(counts)
        entropy = -np.sum(probabilities * np.log2(probabilities)) if len(probabilities) > 0 else 0.0

        self.entropy_score = entropy
        self.drift_rate = len(self.symbol_history) / (1 + len(set(self.symbol_history)))
        self.last_symbol = current_symbol

    def summary(self):
        return {
            "current_symbol": self.last_symbol,
            "entropy_score": self.entropy_score,
            "drift_rate": self.drift_rate,
            "symbol_history": self.symbol_history[-10:]  # recent drift trail
        }
