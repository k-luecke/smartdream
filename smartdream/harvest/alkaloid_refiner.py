from collections import defaultdict
import uuid

class AlkaloidRefiner:
    """
    Extracts symbolic alkaloids (condensed insight) from agent outputs.
    Used to synthesize meaningful, high-potency symbolic patterns
    for storage, distribution, or reward-based harvesting.
    """
    def __init__(self):
        self.storage = defaultdict(list)  # symbol -> list of alkaloids
        self.registry = {}  # id -> alkaloid metadata

    def refine(self, agent, event):
        """
        Condense a meaningful event into a symbolic alkaloid if criteria are met.

        Args:
            agent: the source agent
            event (dict): a memory event with type and metadata

        Returns:
            dict or None: refined alkaloid record
        """
        if event["event_type"] not in ["vision_broadcast", "schema_activated", "seer_evaluation"]:
            return None

        metadata = event.get("metadata", {})
        symbols = metadata.get("symbols") or [metadata.get("symbol")]
        if not symbols:
            return None

        alkaloid = {
            "id": str(uuid.uuid4()),
            "source": agent.name,
            "event_type": event["event_type"],
            "symbolic_payload": symbols,
            "clarity": agent.imprint.get_clarity(),
            "schema_count": len(agent.schema_engine.schemas),
            "stage": getattr(agent.path_training, "stage", "unknown")
        }

        for sym in symbols:
            self.storage[sym].append(alkaloid)
        self.registry[alkaloid["id"]] = alkaloid
        return alkaloid

    def extract_top(self, symbol, top_n=5):
        """
        Retrieve highest clarity alkaloids for a given symbol.
        """
        return sorted(
            self.storage.get(symbol, []),
            key=lambda x: -x["clarity"]
        )[:top_n]

    def summarize(self):
        return {
            "total_alkaloids": len(self.registry),
            "symbol_count": len(self.storage),
            "top_symbols": sorted(self.storage, key=lambda k: -len(self.storage[k]))[:5]
        }
