class Clarity:
    """
    Tracks and computes symbolic clarity — coherence of an agent's imprint structure.
    Useful for regulating schema stability, drift, and trust in symbolic reasoning.
    """
    def __init__(self):
        self.weights = {}  # symbol -> strength (float)

    def update(self, symbol, strength):
        if symbol in self.weights:
            self.weights[symbol] = 0.7 * self.weights[symbol] + 0.3 * strength
        else:
            self.weights[symbol] = strength

    def get_clarity(self):
        if not self.weights:
            return 1.0
        values = list(self.weights.values())
        max_val = max(values)
        total = sum(values)
        return max_val / total if total > 0 else 1.0

    def get_dominant_symbol(self):
        if not self.weights:
            return None
        return max(self.weights.items(), key=lambda x: x[1])[0]

    def decay(self, rate=0.01):
        for key in list(self.weights):
            self.weights[key] *= (1 - rate)
            if self.weights[key] < 0.01:
                del self.weights[key]

    def reset(self):
        self.weights = {}
