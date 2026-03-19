import math
from collections import Counter

class SymbolicEntropy:
    """
    Computes entropy over symbolic phase distribution to measure diversity and predictability.
    Useful for analyzing agent behavior, cultural drift, or symbolic convergence.
    """
    def __init__(self):
        self.phase_records = []

    def record_phase(self, phase):
        self.phase_records.append(phase)

    def compute_entropy(self):
        if not self.phase_records:
            return 0.0

        counts = Counter(self.phase_records)
        total = len(self.phase_records)
        entropy = -sum((count / total) * math.log2(count / total) for count in counts.values())
        return entropy

    def reset(self):
        self.phase_records = []

    def distribution(self):
        return dict(Counter(self.phase_records))
