import random
import hashlib

class HoloFractalNode:
    def __init__(self, zoom, seed_vector):
        self.zoom = zoom  # symbolic recursion depth (e.g. 0 = surface, 3 = deep archetype)
        self.seed = seed_vector  # symbolic tags or values (e.g., ["entropy", "hope", "karma"])
        self.signature = self.generate_signature()

    def generate_signature(self):
        key = f"{self.zoom}-{'-'.join(map(str, self.seed))}"
        digest = hashlib.sha256(key.encode()).hexdigest()
        return int(digest[:8], 16)  # truncate for symbolic index

    def sample_echo(self):
        """
        Return a symbolic echo based on vibrational signature.
        """
        return {
            "fold_axis": self.signature % 3,  # 0, 1, 2 (e.g. dimensional reflection)
            "resonance": (self.signature % 100) / 100.0,
            "archetype_seed": self.seed[self.signature % len(self.seed)]
        }


class HoloFractalField:
    """
    🌀 HoloFractalField — the symbolic meta-topology.
    Agents, visions, and symbolic states may trace back to echo collapses
    from this recursive symbolic layer. Self-similar and infinitely generative.
    """

    def __init__(self):
        self.active_nodes = []

    def pulse(self, zoom=1, seed_tags=None):
        """
        Trigger a vibrational echo from the fractal field.
        """
        if seed_tags is None:
            seed_tags = random.sample([
                "pattern", "echo", "phase",
                "collapse", "drift", "edge"
            ], 3)

        node = HoloFractalNode(zoom, seed_tags)
        self.active_nodes.append(node)
        return node.sample_echo()

    def broadcast_summary(self):
        """
        Returns a list of recent symbolic echo samples.
        """
        return [node.sample_echo() for node in self.active_nodes[-5:]]
