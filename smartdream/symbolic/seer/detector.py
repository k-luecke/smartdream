import math
from collections import defaultdict
from datetime import datetime

class SeerEngine:
    def __init__(self, memory_window=50):
        self.seer_log = set()
        self.symbol_registry = defaultdict(list)
        self.insight_log = defaultdict(list)  # agent_id -> list of (insight_density, timestamp)
        self.memory_window = memory_window
        self.prediction_logs = defaultdict(list)
        self.seer_scores = defaultdict(lambda: 0.5)  # agent_id -> seer score
        self.alpha = 0.9  # smoothing factor

    def evaluate(self, agent, prediction, outcome, compute_cost, timestamp):
        numeric_pred = prediction.get("numeric", 0)
        numeric_out = outcome.get("numeric", 0)

        # === Agent-defined resonance ===
        resonance = agent.compute_resonance(numeric_pred, numeric_out)

        # === Symbolic similarity ===
        predicted_symbol = prediction.get("symbol")
        symbolic_echoes = outcome.get("symbolic_echoes", [])
        symbolic_score = agent.match_symbolic(predicted_symbol, symbolic_echoes)

        # === Composite insight score ===
        insight_score = (resonance + symbolic_score) / 2
        insight_density = insight_score / (compute_cost + 1e-6)

        self.insight_log[agent.id].append((insight_density, timestamp))
        self._prune_insight_log(agent.id)

        recent_insights = [s for s, _ in self.insight_log[agent.id]]
        avg_density = sum(recent_insights) / len(recent_insights)

        # === Fluid symbolic promotion (no hard threshold) ===
        if agent.should_drift_role("seer", avg_density):
            self.promote_to_seer(agent, predicted_symbol)

        # === Update symbolic seer score ===
        symbolic_pressure = agent.estimate_symbolic_pressure(symbolic_score, resonance)
        previous_score = self.seer_scores[agent.id]
        new_score = self.alpha * previous_score + (1 - self.alpha) * symbolic_pressure
        self.seer_scores[agent.id] = new_score

        log_entry = {
            "timestamp": timestamp or datetime.now(),
            "resonance": resonance,
            "symbolic_score": symbolic_score,
            "insight_score": insight_score,
            "seer_score": new_score,
            "symbol": predicted_symbol
        }

        self.prediction_logs[agent.id].append(log_entry)

        agent.memory.record_event(
            signal="seer_evaluation",
            timestamp=log_entry["timestamp"],
            metadata=log_entry,
            source="seer_engine",
            context=None
        )

    def promote_to_seer(self, agent, symbol):
        if agent.id not in self.seer_log:
            self.seer_log.add(agent.id)
            self.symbol_registry[symbol].append(agent.id)
            agent.status["seer"] = True
            agent.memory.record_event(
                signal="role_promotion",
                timestamp=None,
                metadata={"role": "seer", "symbol": symbol},
                source="seer_engine"
            )

    def _prune_insight_log(self, agent_id):
        self.insight_log[agent_id] = self.insight_log[agent_id][-self.memory_window:]

    def get_active_seers(self):
        return list(self.seer_log)

    def get_predictive_symbols(self):
        return dict(self.symbol_registry)

    def get_prediction_log(self, agent_id):
        return self.prediction_logs[agent_id]

    def get_seer_score(self, agent_id):
        return self.seer_scores[agent_id]
