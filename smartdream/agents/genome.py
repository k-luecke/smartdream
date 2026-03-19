import random

class Genome:
    def __init__(self, y=None, x=None, v=None):
        self.y = y or {}
        self.x = x or {}
        self.v = v or {}

    @staticmethod
    def random():
        return Genome(
            y={"species": random.choice(["Seraph", "Mycelid", "Chorite"])},
            x={"entry_threshold": random.uniform(0.5, 0.8)},
            v={"sensitivity": random.random()}
        )

    def express(self):
        return {
            "entry_threshold": self.x.get("entry_threshold", 0.7),
            "exit_threshold": 0.3
        }

    def mutate(self, rate=0.1):
        if random.random() < rate:
            self.x["entry_threshold"] = random.uniform(0.5, 0.8)

    def crossover(self, other):
        new_y = self.y.copy()
        new_x = {k: (self.x[k] + other.x.get(k, self.x[k])) / 2 for k in self.x}
        new_v = self.v.copy()
        return Genome(new_y, new_x, new_v)
