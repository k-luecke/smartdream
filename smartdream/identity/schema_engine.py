import random
from identity.clarity import Clarity

class Schema:
    def __init__(self, label, source, features, age=0):
        self.label = label
        self.source = source  # e.g. "symbolic", "developmental"
        self.features = features  # list of symbolic or behavioral traits
        self.age = age
        self.history = []
        self.strength = 1.0  # confidence or salience
        self.context_log = []  # tracks activation context

    def evolve(self, new_features):
        self.history.append(list(self.features))
        self.features = new_features
        self.age += 1
        self.strength *= 0.95  # symbolic entropy or uncertainty over time

    def similarity(self, other):
        shared = set(self.features) & set(other.features)
        total = set(self.features) | set(other.features)
        return len(shared) / len(total) if total else 0.0

    def activate(self, context):
        """
        Contextual activation of schema: boosts strength and logs environment.
        """
        self.context_log.append(context)
        self.strength = min(self.strength + 0.1, 2.0)
        self.age += 1

    def drift(self, clarity=1.0):
        """
        Apply symbolic drift to evolve schema subtly. Clarity dampens mutation.
        """
        if self.features and random.random() > clarity:
            dropped = random.choice(self.features)
            mutated = dropped + "*"
            self.features.remove(dropped)
            self.features.append(mutated)
            self.age += 1
            self.strength *= 0.9

    def should_retire(self, min_strength=0.5, max_age=10):
        """
        Determine if a schema should be retired based on age and low strength.
        """
        return self.strength < min_strength and self.age > max_age


class SchemaEngine:
    def __init__(self, agent):
        self.agent = agent
        self.schemas = []
        self.clarity = Clarity()

    def extract_signals(self):
        return {
            "symbols": ([self.agent.imprint["symbol"]] if self.agent.imprint else []),
            "weights": {self.agent.imprint["symbol"]: 1.0} if self.agent.imprint else {},
            "development": self.agent.developmental_stage,
            "behaviors": self.agent.memory.extract_recent_behaviors(n=30),
            "environment": self.agent.vision.perceive(),
        }

    def generate_schema(self):
        from datetime import datetime
        signals = self.extract_signals()
        weighted_symbols = sorted(signals["weights"].items(), key=lambda x: -x[1])
        top_symbols = [s for s, w in weighted_symbols[:3]]
        traits = list(set(top_symbols + [signals["development"]]))
        schema = Schema(label=f"schema_{len(self.schemas)}",
                        source="auto_generated",
                        features=traits)
        self.schemas.append(schema)
        self.clarity.update(schema.label, schema.strength)
        self.agent.memory.record_event("schema_created", timestamp=datetime.now(), metadata={"label": schema.label})
        return schema

    def activate_matching_schema(self):
        from datetime import datetime
        context = self.agent.vision.perceive()
        best = None
        best_score = 0.0
        for schema in self.schemas:
            score = len(set(context) & set(schema.features))
            if score > best_score:
                best_score = score
                best = schema
        if best:
            schema_context = {
                "symbols": context,
                "recent_behaviors": self.agent.memory.extract_recent_behaviors(n=10),
                "imprint_tags": self.agent.genome.v.get("tags", [])
            }
            best.activate(schema_context)
            self.agent.memory.record_event("schema_activated", timestamp=datetime.now(), metadata={
                "schema": best.label,
                "strength": best.strength,
                "context_tags": schema_context
            })
        return best

    def evolve_all(self):
        from datetime import datetime
        clarity_score = self.clarity.get_clarity()
        updated_schemas = []
        for schema in self.schemas:
            schema.drift(clarity_score)
            if not schema.should_retire():
                updated_schemas.append(schema)
            else:
                self.agent.memory.record_event("schema_retired", timestamp=datetime.now(), metadata={
                    "label": schema.label,
                    "final_strength": schema.strength,
                    "age": schema.age
                })
        self.schemas = updated_schemas

    def compare_to(self, other_agent):
        if not hasattr(other_agent, "schema_engine"):
            return 0.0
        max_similarity = 0.0
        for own_schema in self.schemas:
            for other_schema in other_agent.schema_engine.schemas:
                sim = own_schema.similarity(other_schema)
                max_similarity = max(max_similarity, sim)
        return max_similarity
