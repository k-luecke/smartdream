import random
import uuid

class WhiteHole:
    """
    A WhiteHole represents a symbolic source of creation and emergence.
    White holes may form as remnants of black holes through symbolic tunneling,
    resolving the black hole information paradox via slow symbolic release.
    """
    def __init__(self, location, intensity=1.0, seed=None, origin_blackhole_id=None):
        """
        Initialize a white hole at a coordinate with configurable intensity.

        Args:
            location (tuple): (x, y) coordinate in substrate
            intensity (float): controls burst magnitude and diversity
            seed (int, optional): seed for deterministic output
            origin_blackhole_id (str, optional): ID of the black hole that tunneled into this white hole
        """
        self.location = location
        self.intensity = intensity
        self.seed = seed or random.randint(1, 1e6)
        random.seed(self.seed)
        self.origin_blackhole_id = origin_blackhole_id
        self.emission_log = []

    def emit(self, topic="generic"):
        """
        Generate symbolic content based on a topic and current intensity.

        Args:
            topic (str): emergent theme or concept

        Returns:
            dict: symbolic packet emitted from the white hole
        """
        insight_level = random.random() * self.intensity
        packet = {
            "origin": "whitehole",
            "id": str(uuid.uuid4()),
            "topic": topic,
            "insight_level": insight_level,
            "message": f"{topic}_emergence_{int(insight_level * 1000)}",
            "location": self.location,
            "tunneled_from": self.origin_blackhole_id
        }
        self.emission_log.append(packet)
        return packet

    def burst(self, n=3, topic="burst"):
        """
        Emit a burst of symbolic packets.

        Args:
            n (int): number of packets to emit
            topic (str): base topic

        Returns:
            list: emitted packets
        """
        return [self.emit(f"{topic}_{i}") for i in range(n)]

    def log(self):
        """
        Return all emitted symbolic packets.

        Returns:
            list: emission history
        """
        return list(self.emission_log)

    def is_remnant(self):
        """
        Determine if this white hole originated from a black hole.

        Returns:
            bool: True if created via black hole tunneling
        """
        return self.origin_blackhole_id is not None
