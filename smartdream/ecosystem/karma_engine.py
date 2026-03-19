from datetime import datetime

class KarmaEngine:
    """
    Karma engine tracks symbolic integrity, ethical alignment, and feedback loops.
    Agents accumulate karma based on resonance, honesty, and symbolic impact.
    """
    def __init__(self, agent):
        self.agent = agent
        self.karma_score = 0.0
        self.karma_log = []
        self.last_event = None

    def record(self, label, delta, metadata=None):
        self.karma_score += delta
        self.last_event = {
            "label": label,
            "delta": delta,
            "metadata": metadata or {},
            "timestamp": datetime.now(),
            "karma": self.karma_score
        }
        self.karma_log.append(self.last_event)

    def score(self):
        return self.karma_score

    def recent(self, n=5):
        return self.karma_log[-n:]

    def tick(self):
        self.karma_score *= 0.99  # decay
        self.karma_log.append({
            "event": "tick",
            "score": round(self.karma_score, 2),
            "last": self.last_event
        })

    def seal(self):
        self.record("karma_seal", 0.0, {"message": "Final karma checkpoint."})

    def snapshot(self):
        return {
            "karma": self.karma_score,
            "last_event": self.last_event,
            "entries": len(self.karma_log)
        }
