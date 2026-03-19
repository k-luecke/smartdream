class ImmuneResponse:
    """
    Symbolic immune system that responds to fever conditions and high symbolic entropy.
    It triggers protective actions to maintain agent coherence.
    """

    def __init__(self, fever_threshold=0.05, entropy_threshold=1.5):
        self.fever_triggered = False
        self.entropy_triggered = False
        self.fever_threshold = fever_threshold
        self.entropy_threshold = entropy_threshold

    def evaluate(self, kalman_delta, drift_entropy):
        """
        Determine whether the agent is in a fever or symbolic crisis state.
        :param kalman_delta: dict of signal deltas from KalmanEngine
        :param drift_entropy: float entropy score from SymbolicDrift
        :return: dict indicating fever and entropy status
        """
        self.fever_triggered = any(abs(delta) > self.fever_threshold for delta in kalman_delta.values())
        self.entropy_triggered = drift_entropy > self.entropy_threshold
        return {
            "fever": self.fever_triggered,
            "entropy": self.entropy_triggered,
            "crisis": self.fever_triggered or self.entropy_triggered
        }

    def respond(self, agent):
        """
        Apply symbolic defenses or resets based on agent condition.
        :param agent: reference to the agent being evaluated
        """
        if not agent.alive:
            return

        if self.fever_triggered:
            agent.ritual.start_ritual("fever", "cooldown", agent.age)
            agent.dose.adjust(-0.1)

        if self.entropy_triggered:
            agent.energy -= 10.0
            agent.symbol_interpretation_map = {}  # purge symbolic assumptions
            agent.memory.record_event("immune_response", metadata={"action": "entropy_correction"})

        if agent.energy <= 0:
            agent.reset_agent()
