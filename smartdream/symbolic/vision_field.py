from collections import defaultdict
import random

class VisionField:
    """
    Shared symbolic environment for agent perception and broadcast.
    Agents using VisionChannel can receive from and emit to this field.
    Symbolic decay, spatial range, or tagging can be added modularly.
    """
    def __init__(self):
        self.channel_data = defaultdict(list)

    def receive_from(self, agent, symbols):
        """
        Agents send symbolic tags into the global field.

        Args:
            agent: agent object (must have unique ID or name)
            symbols (list): list of symbolic tags to emit
        """
        self.channel_data[agent.name].extend(symbols)

    def emit_to(self, agent, n=3):
        """
        Agent requests perception input from the field.

        Args:
            agent: requesting agent
            n (int): number of symbols to randomly sample

        Returns:
            list[str]: sampled symbolic impressions from other agents
        """
        symbols = []
        for name, stream in self.channel_data.items():
            if name != agent.name:
                symbols.extend(stream[-5:])  # take most recent
        return random.sample(symbols, min(n, len(symbols))) if symbols else []

    def clear(self):
        """
        Clears the field (e.g., at the end of a symbolic time cycle).
        """
        self.channel_data.clear()
