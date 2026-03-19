from datetime import datetime

class Dose:
    """
    Represents symbolic/statistical modulation for an agent's decision-making logic.
    This version supports dual weights, context-aware adjustment, and dose history tracking.
    """
    def __init__(self, symbolic=0.5, statistical=None):
        self.symbolic = max(0.0, min(1.0, symbolic))
        self.statistical = 1.0 - self.symbolic if statistical is None else max(0.0, min(1.0, statistical))
        self.history = []

    def symbolic_weight(self):
        return self.symbolic

    def statistical_weight(self):
        return self.statistical

    def adjust(self, delta):
        old_ratio = self.symbolic
        self.symbolic = max(0.0, min(1.0, self.symbolic + delta))
        self.statistical = 1.0 - self.symbolic
        self.history.append((datetime.now(), old_ratio, self.symbolic))

    def adjust_by_context(self, context):
        symbolic_pressure = context.get("symbolic_pressure", 0)
        statistical_clarity = context.get("statistical_clarity", 0)
        shift = 0.05 if symbolic_pressure > statistical_clarity else -0.05
        self.adjust(shift)

    def is_balanced(self):
        return abs(self.symbolic - 0.5) < 0.1

    def __repr__(self):
        return f"Dose(symbolic={self.symbolic:.2f}, statistical={self.statistical:.2f})"
