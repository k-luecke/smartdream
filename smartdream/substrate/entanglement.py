import random

class EntangledPair:
    """
    Represents a nonlocal symbolic connection between two agents, events, or symbolic masses.
    Changes to one side of the pair can instantly reflect or influence the other.
    Can decohere over time or through environmental noise.
    """
    def __init__(self, id1, id2, stability=1.0, decoherence_rate=0.01):
        self.agent_a = id1
        self.agent_b = id2
        self.state = {}  # Shared symbolic state
        self.history = []
        self.stability = stability  # Probability [0-1] of remaining coherent
        self.decoherence_rate = decoherence_rate
        self.coherent = True

    def update_state(self, key, value):
        """
        Update shared entangled state.

        Args:
            key (str): state key
            value (any): state value
        """
        if self.coherent:
            self.state[key] = value
            self.history.append((key, value))

    def get_state(self):
        """
        Return a copy of the current shared state if coherent.

        Returns:
            dict: shared state or empty dict if decohered
        """
        return dict(self.state) if self.coherent else {}

    def reflect(self, agent_id):
        """
        Determine which entangled agent reflects the given ID.

        Args:
            agent_id (str): one of the two IDs

        Returns:
            str or None: the other agent ID if still coherent
        """
        if not self.coherent:
            return None
        if agent_id == self.agent_a:
            return self.agent_b
        elif agent_id == self.agent_b:
            return self.agent_a
        else:
            return None

    def trace_history(self):
        """
        Get the update history of the entangled pair.

        Returns:
            list: (key, value) update records
        """
        return list(self.history) if self.coherent else []

    def tick_decoherence(self):
        """
        Progress decoherence over time. Probability-based collapse.
        """
        if self.coherent:
            if random.random() < self.decoherence_rate * (1.0 - self.stability):
                self.coherent = False

    def is_coherent(self):
        """
        Check if the entangled pair is still coherent.

        Returns:
            bool: True if entanglement persists
        """
        return self.coherent
