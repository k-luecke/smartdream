from datetime import datetime

class PathTrainingEngine:
    """
    Guides symbolic development by tracking learning pressure, depth,
    and context-sensitive advancement across flexible symbolic stages.
    """

    def __init__(self, agent):
        self.agent = agent
        self.stage = "initiated"
        self.score = 0.0
        self.failed_attempts = 0
        self.history = []

    def reset(self):
        self.stage = "initiated"
        self.score = 0.0
        self.failed_attempts = 0
        self.history.clear()

    def tick(self):
        self.evaluate_progress()

    def evaluate_progress(self):
        """
        Determine whether symbolic advancement is warranted
        based on engagement, pattern recognition, and clarity.
        """
        memory_count = len(self.agent.memory.events)
        clarity = self.agent.schema_engine.clarity.get_clarity()
        schema_count = len(self.agent.schema_engine.schemas)

        if self.stage == "initiated" and memory_count > 5:
            self.advance("emergent")
        elif self.stage == "emergent" and memory_count > 15 and clarity > 0.5:
            self.advance("proficient")
        elif self.stage == "proficient" and schema_count >= 5:
            self.advance("symbolic")
        elif self.stage == "symbolic" and clarity > 0.7 and self.agent.compute_fitness() > 10:
            self.advance("adaptive")

    def advance(self, new_stage):
        self.history.append((self.stage, new_stage))
        self.agent.memory.record_event(
            "promotion",
            timestamp=datetime.now(),
            metadata={"from": self.stage, "to": new_stage}
        )
        self.stage = new_stage

    def summarize(self):
        return {
            "current_stage": self.stage,
            "score": round(self.score, 2),
            "history": self.history
        }
