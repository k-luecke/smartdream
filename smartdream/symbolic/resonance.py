from collections import defaultdict
import math

class SymbolicResonance:
    """
    Tracks symbolic overlap and resonance intensity between agents.
    Used to detect affinity, echo patterns, or symbolic harmonics.
    """
    def __init__(self):
        self.resonance_map = defaultdict(lambda: defaultdict(float))  # A -> B -> score

    def update_resonance(self, agent_a, agent_b, shared_symbols):
        """
        Increase resonance score based on shared symbols.

        Args:
            agent_a (str): ID or name of first agent
            agent_b (str): ID or name of second agent
            shared_symbols (list[str]): overlapping symbols
        """
        score = len(shared_symbols) / max(1, len(set(shared_symbols)))
        self.resonance_map[agent_a][agent_b] += score
        self.resonance_map[agent_b][agent_a] += score

    def get_resonance(self, agent_a, agent_b):
        return self.resonance_map[agent_a][agent_b]

    def decay_all(self, rate=0.01):
        """
        Gradually decay resonance scores to reflect symbolic drift.
        """
        for a in self.resonance_map:
            for b in self.resonance_map[a]:
                self.resonance_map[a][b] *= (1 - rate)

    def top_resonances(self, agent, top_n=3):
        """
        Return top N symbolic affinities for the given agent.
        """
        others = self.resonance_map[agent]
        return sorted(others.items(), key=lambda x: -x[1])[:top_n]
