import pandas as pd
import uuid
from datetime import datetime

class Memory:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.events = []

    def record_event(self, signal: str, timestamp: datetime, metadata: dict, tags=None, source=None, context=None):
        event = {
            "agent_id": self.agent_id,
            "timestamp": timestamp,
            "signal": signal,
            "tags": tags or [],
            "source": source or "unspecified",
            "context": context or {},
            "metadata": metadata
        }
        self.events.append(event)

    def to_dataframe(self):
        return pd.DataFrame(self.events)

    def summarize(self):
        df = self.to_dataframe()
        summary = df["signal"].value_counts().to_dict()
        return {
            "agent_id": self.agent_id,
            "event_count": len(self.events),
            "signal_distribution": summary
        }

    def extract_recent_behaviors(self, n=30):
        return [
            e["metadata"]["chosen_action"]
            for e in self.events[-n:]
            if e["signal"] == "action" and "chosen_action" in e["metadata"]
        ]

    def save(self, path: str):
        df = self.to_dataframe()
        df.to_csv(path, index=False)

    def clear(self):
        self.events = []
