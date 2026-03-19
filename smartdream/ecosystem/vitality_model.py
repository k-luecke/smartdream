class VitalityModel:
    """
    Tracks symbolic vitality, energetic decay, and potential for self-renewal.
    Influences agent energy, burnout, and revival capacity.
    """
    def __init__(self, agent):
        self.agent = agent
        self.max_vitality = 100.0
        self.vitality = 100.0
        self.decay_rate = 0.5
        self.regen_rate = 0.2
        self.history = []

    def tick(self, timestamp=None):
        if self.agent.alive:
            delta = -self.decay_rate + (self.regen_rate if self.agent.energy > 50 else 0)
            self.vitality = max(0.0, min(self.max_vitality, self.vitality + delta))
            self.history.append(self.vitality)
            if self.vitality == 0:
                self.agent.die("vitality_depleted")

    def boost(self, amount):
        self.vitality = min(self.max_vitality, self.vitality + amount)

    def stress(self, amount):
        self.vitality = max(0.0, self.vitality - amount)

    def snapshot(self):
        return {
            "vitality": self.vitality,
            "max": self.max_vitality,
            "history": self.history[-10:]
        }
