from datetime import datetime

class ImprintingEngine:
    """
    Encodes symbolic imprinting events — linking experience to symbolic identity.
    Used during early memory formation or peak insight events.
    Now supports neutral symbolic codes, reversibility, and clarity-weighted strength.
    """
    def imprint(self, agent, action, confidence, fever_flag):
        symbol, strength = self.derive_symbol_and_strength(action, confidence, fever_flag)
        agent.imprint = {
            "symbol": symbol,
            "confidence": confidence,
            "fever_flag": fever_flag,
            "timestamp": datetime.now(),
            "imprint_strength": strength,
            "sensitivity_type": "orchid"
        }
        if hasattr(agent, 'ecosystem') and agent.ecosystem:
            agent.ecosystem.track_symbol_population(symbol)

    def derive_symbol_and_strength(self, action, confidence, fever_flag):
        """Assign a neutral symbol code and derive imprint strength from clarity."""
        if fever_flag:
            return "sym-001", 0.3 + confidence * 0.2
        elif action == "buy" and confidence > 0.7:
            return "sym-002", 0.5 + confidence * 0.3
        elif action == "exit" and confidence < 0.3:
            return "sym-003", 0.4
        return "sym-004", 0.2 + confidence * 0.2

    def clear_imprint(self, agent):
        if agent.imprint and hasattr(agent, 'ecosystem'):
            agent.ecosystem.untrack_symbol_population(agent.imprint.get("symbol"))
        agent.imprint = None
