class RegimeClassifier:
    """
    A symbolic-statistical regime classifier that uses planetary alignment
    and emergent multi-agent feedback to track and label regime transitions.
    """
    def __init__(self):
        self.history = []
        self.symbols = ["r-001", "r-002", "r-003", "r-004"]  # neutral regime labels

    def classify(self, context, agents):
        sig = context.planetary_signature or {}
        angle_diff = sig.get("angle_diff", 0)
        relation = sig.get("planet_relation_angle", 0)

        clarity_levels = []
        symbolic_weights = []

        for agent in agents:
            clarity = agent.memory.to_dataframe()["metadata"].apply(lambda m: m.get("symbolic_clarity", 0)).mean()
            clarity_levels.append(clarity)
            symbolic_weights.append(agent.dose.symbolic_weight())

        avg_clarity = sum(clarity_levels) / len(clarity_levels) if clarity_levels else 0
        avg_symbolic = sum(symbolic_weights) / len(symbolic_weights) if symbolic_weights else 0

        # Symbol-neutral rule space
        if angle_diff < 30 and avg_clarity > 0.6:
            return self.symbols[0]  # r-001
        elif 60 < angle_diff < 120 and avg_symbolic > 0.5:
            return self.symbols[1]  # r-002
        elif angle_diff > 150:
            return self.symbols[2]  # r-003

        return self.symbols[3]  # r-004 (baseline)

    def update(self, context, agents):
        regime = self.classify(context, agents)
        self.history.append((context.tick, regime))

        for agent in agents:
            agent.memory.record_event(
                signal="regime_detected",
                timestamp=datetime.now(),
                metadata={"regime": regime},
                source="regime_classifier",
                context={"tick": context.tick}
            )

            if agent.imprint:
                agent.imprint["regime_phase"] = regime

        return regime

    def recent_regimes(self, n=10):
        return self.history[-n:]
