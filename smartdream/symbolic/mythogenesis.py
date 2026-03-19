from collections import defaultdict
import uuid
import random

class Myth:
    def __init__(self, core_symbol, origin_agent=None):
        self.id = str(uuid.uuid4())
        self.core = core_symbol
        self.threads = []  # list of narrative fragments
        self.origin = origin_agent.name if origin_agent else "unknown"
        self.mentions = 0
        self.entropy = 1.0  # lower = more stable / repeated

    def add_thread(self, text):
        self.threads.append(text)
        self.mentions += 1
        self.entropy *= 0.95  # repetition reduces novelty

    def get_summary(self):
        return {
            "id": self.id,
            "core": self.core,
            "mentions": self.mentions,
            "entropy": round(self.entropy, 3),
            "threads": self.threads[-3:]  # latest fragments
        }

class MythogenesisEngine:
    def __init__(self):
        self.myths = {}
        self.symbol_index = defaultdict(list)  # symbol -> myth IDs

    def create_myth(self, symbol, agent=None):
        myth = Myth(core_symbol=symbol, origin_agent=agent)
        self.myths[myth.id] = myth
        self.symbol_index[symbol].append(myth.id)
        return myth

    def narrate(self, symbol, text, agent=None):
        """
        Add a new thread to a myth or create one if it doesn’t exist.
        """
        myth_id = self._find_existing_myth(symbol)
        if myth_id:
            self.myths[myth_id].add_thread(text)
        else:
            new_myth = self.create_myth(symbol, agent=agent)
            new_myth.add_thread(text)

    def _find_existing_myth(self, symbol):
        myth_ids = self.symbol_index.get(symbol, [])
        if myth_ids:
            return random.choice(myth_ids)  # nondeterministic continuity
        return None

    def summarize_all(self):
        return [m.get_summary() for m in self.myths.values()]
