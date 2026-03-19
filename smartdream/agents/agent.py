import random
from datetime import datetime

from symbolic.seer.detector import SeerEngine
from core.dose import Dose
from core.kalman_engine import KalmanEngine
from symbolic.drift import SymbolicDrift
from ecosystem.immune_response import ImmuneResponse

from memory.memory import Memory

from symbolic.ritual import RitualEngine

from symbolic.vision import global_vision
from identity.schema_engine import SchemaEngine
from identity.imprinting import ImprintingEngine
from ecosystem.vitality_model import VitalityModel

from identity.path_training import PathTrainingEngine
from ecosystem.karma_engine import KarmaEngine
from ecosystem.ecosystem_engine import EcosystemEngine
from agents.species import assign_species_traits, generation_cycle
from agents.genome import Genome
from symbolic.vision_channel import VisionChannel


class Agent:
    def __init__(self, name=None, genome=None, agent_id=None):
        self.genome = genome or Genome.random()
        self.expressed_traits = self.genome.express()
        self.agent_id = self._generate_id if agent_id is not None else self._generate_id()
        self.name = name or f"Agent_{self.agent_id}"
        self.age = 0
        self.developmental_stage = "infant"

        self.memory = Memory(agent_id=self.agent_id)
        self.ritual = RitualEngine()
        self.schema_engine = SchemaEngine(self)
        self.vitality = VitalityModel(self)
        self.path_training = PathTrainingEngine(self)
        self.karma = KarmaEngine(self)
        self.ecosystem = EcosystemEngine(self)
        self.alive = True

        self.imprint = None
        self.identity_schema = None
        self.assigned_role = None
        self.symbol_interpretation_map = {}

        self.dose = Dose()
        self.energy = 100.0

        self.seer_engine = SeerEngine()
        self.kalman = KalmanEngine()
        self.drift = SymbolicDrift()
        self.immunity = ImmuneResponse()

        self.last_prediction = None
        self.last_outcome = None
        self.status = {}

        self.position = 0  # Flat
        self.entry_price = None

        assign_species_traits(self)
        self.vision = VisionChannel(agent=self)

    def _generate_id(self):
        return self.genome.y.get("species", "")[:2].upper() + "_" + str(hash(str(self.genome.x)))[:6]

    def log_dose_action(self, timestamp, confidence, fever_flag, action):
        self.memory.record_event(
            signal="action",
            timestamp=timestamp,
            metadata={
                "confidence": confidence,
                "fever_flag": fever_flag,
                "chosen_action": action
            }
        )

    def perceive_and_act(self, timestamp: datetime, confidence: float, fever_flag: bool):
        if confidence is None or fever_flag is None or timestamp is None:
            return

        traits = self.expressed_traits
        if self.ritual.is_in_ritual(self.age):
            traits = self.ritual.apply_ritual_effects(traits)

        modulated_confidence = confidence * traits.get("confidence_modulation", 1.0)

        if self.imprint:
            symbol = self.imprint.get("symbol")
            if symbol == "Wanderer":
                modulated_confidence *= 0.95
            elif symbol == "Initiate":
                modulated_confidence *= 1.05

        if fever_flag:
            action = "wait"
        elif modulated_confidence > traits["entry_threshold"]:
            action = "buy"
        elif modulated_confidence < traits["exit_threshold"]:
            action = "sell"
        else:
            action = "hold"

        self.log_dose_action(timestamp, modulated_confidence, fever_flag, action)

        if self.imprint is None and len(self.memory.events) == 1:
            ImprintingEngine().imprint(self, action, modulated_confidence, fever_flag)

        if self.seer_engine and self.last_prediction and self.last_outcome:
            self.seer_engine.evaluate(
                agent=self,
                prediction=self.last_prediction,
                outcome=self.last_outcome,
                compute_cost=self.expressed_traits.get("compute_used", 1.0),
                timestamp=timestamp
            )

        self.update_development()

        return {"agent": self, "decision": action}

    def evaluate_outcome(self, success: bool):
        direction = 1 if success else -1
        delta = 0.01 * (2 * self.dose.symbolic_weight() - 1)
        self.dose.adjust(direction * delta)

        self.memory.record_event(
            signal="dose_feedback",
            timestamp=datetime.now(),
            metadata={
                "symbolic_weight": self.dose.symbolic_weight(),
                "statistical_weight": self.dose.statistical_weight(),
                "fever": self.kalman.detect_fever(),
                "price_delta": abs(self.kalman.delta["price"]),
                "action_outcome": success
            },
            source="dose_adjustment",
            context=None
        )

        if success:
            self.energy += 5.0 * self.dose.symbolic_weight()
        else:
            self.energy -= 5.0 * self.dose.symbolic_weight()

        self.energy = max(0.0, self.energy)

        if self.imprint and success:
            self.imprint['dose_bias'] = self.dose.symbolic_weight()

        if self.energy == 0.0:
            self.reset_agent()

    def perceive_symbolic_echoes(self):
        if not self.ritual.is_in_ritual(self.age):
            return
        echoes = global_vision.perceive(self)
        self.memory.record_event("vision", timestamp=None, metadata={"symbolic_echoes": echoes})

    def update_identity_schema(self):
        self.identity_schema = self.schema_engine.generate_schema()

    def update_role(self, path_engine):
        if not self.identity_schema:
            self.update_identity_schema()
        self.assigned_role = path_engine.assign_role(self)

    def update_symbol_interpretations(self, global_registry):
        self.symbol_interpretation_map = {
            symbol: self.compute_personal_interpretation(symbol, global_registry)
            for symbol in global_registry.get_all_symbols()
        }

    def compute_personal_interpretation(self, symbol, global_registry):
        global_vec = global_registry.get_current_meaning(symbol)
        age_weight = 1 / (1 + self.age / 100)
        memory_bias = self.memory.get_symbol_bias(symbol) if hasattr(self.memory, 'get_symbol_bias') else [0.0, 0.0, 0.0]
        return [age_weight * gv + (1 - age_weight) * mb for gv, mb in zip(global_vec, memory_bias)]

    def symbolic_drift(self, global_registry):
        if not self.imprint:
            return
        current = self.imprint.get("symbol")
        if not current or current not in generation_cycle:
            return
        base_chance = 0.02
        if self.age > 100:
            base_chance += 0.08
        if self.compute_fitness() < 5:
            base_chance += 0.10
        if random.random() < base_chance:
            new_symbol = generation_cycle.get(current)
            self.imprint["symbol"] = new_symbol
            self.ritual.start_ritual(current, new_symbol, self.age)
            self.update_symbol_interpretations(global_registry)

    def update_development(self):
        self.age += 1
        total_events = len(self.memory.events)
        if self.age < 10:
            self.developmental_stage = "infant"
        elif total_events < 50:
            self.developmental_stage = "juvenile"
        else:
            self.developmental_stage = "mature"
        if self.age % 20 == 0:
            self.symbolic_drift(global_registry=None)
        if self.ritual.is_in_ritual(self.age):
            global_vision.broadcast(self.agent_id, self.imprint["symbol"], self.age)
        self.ritual.resolve_ritual(self.age)
        self.update_identity_schema()
        self.path_training.tick()
        self.karma.tick()
        self.ecosystem.tick()

    def compute_fitness(self):
        df = self.memory.to_dataframe()
        if "confidence" not in df.columns:
            return 0.0
        base_fitness = df["confidence"].mean() * len(df)
        if self.imprint:
            strength = self.imprint.get("imprint_strength", 0.5)
            type_mod = 1.2 if self.imprint.get("sensitivity_type") == "orchid" else 0.9
            return base_fitness * (1 + strength * type_mod)
        return base_fitness

    def reset_agent(self):
        self.energy = 50.0
        self.dose = Dose(0.5)
        self.update_symbol_interpretations(global_registry=None)

    def modulate_dose(self, direction):
        self.dose.adjust(0.1 * direction)

    def recall(self):
        return self.memory.to_dataframe()

    def export_summary(self):
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "age": self.age,
            "stage": self.developmental_stage,
            "identity_schema": self.identity_schema,
            "assigned_role": self.assigned_role,
            "imprint": self.imprint if self.imprint else {},
            "traits": self.expressed_traits,
            "genome": {
                "Y": self.genome.y,
                "X": self.genome.x,
                "V": self.genome.v
            },
            **self.memory.summarize()
        }

    def die(self, reason="unknown"):
        self.karma.seal()
        self.memory.record_event("death", timestamp=datetime.now(), metadata={"reason": reason})
        self.alive = False

    def save_memory(self, path=None):
        import os
        path = path or f"generations/{self.name}_log.csv"
        os.makedirs("generations", exist_ok=True)
        self.memory.save(path)
