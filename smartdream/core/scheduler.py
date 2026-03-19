from datetime import datetime, timedelta

class Scheduler:
    """
    Scheduler for managing symbolic agent cycles, rituals, and regime-aware timing.
    Supports programmable phases, temporal skips, and conditional triggers.
    """
    def __init__(self, tick_interval=1, planetary_clock=None):
        self.tick = 0
        self.tick_interval = tick_interval
        self.start_time = datetime.now()
        self.schedule_log = []
        self.planetary_clock = planetary_clock

    def advance(self):
        """Advance the system tick and return current datetime."""
        self.tick += self.tick_interval
        now = self.start_time + timedelta(minutes=self.tick)
        self.schedule_log.append((self.tick, now))
        return self.tick, now

    def current_time(self):
        return self.start_time + timedelta(minutes=self.tick)

    def get_tick(self):
        return self.tick

    def log_event(self, label):
        self.schedule_log.append((self.tick, label))

    def recent_log(self, n=10):
        return self.schedule_log[-n:]

    def should_trigger(self, frequency):
        return self.tick % frequency == 0

    def trigger_agent_rituals(self, agents):
        for agent in agents:
            if agent.ritual and agent.ritual.is_in_ritual(agent.age):
                agent.perceive_symbolic_echoes()

    def get_planetary_signature(self):
        if self.planetary_clock:
            return self.planetary_clock.get_signature(self.tick)
        return {}

    def symbolic_phase(self):
        """
        Returns a neutral symbolic label based on the tick cycle.
        Divides time into repeating segments, bias-free.
        """
        phase_labels = ["s-001", "s-002", "s-003", "s-004"]
        return phase_labels[(self.tick // 1000) % len(phase_labels)]

    def fixed_phase(self):
        """
        Returns a fixed-tick symbolic label for agents to track artificial periodicity.
        """
        fixed_labels = ["fx-a", "fx-b", "fx-c", "fx-d"]
        return fixed_labels[(self.tick // 500) % len(fixed_labels)]

    def assign_symbolic_phase_to_agents(self, agents):
        planetary_phase = self.symbolic_phase()
        fixed_phase = self.fixed_phase()

        for agent in agents:
            agent.memory.record_event(
                signal="symbolic_phase",
                timestamp=datetime.now(),
                metadata={"planetary": planetary_phase, "fixed": fixed_phase},
                source="scheduler",
                context={"tick": self.tick}
            )
            if agent.imprint is not None:
                agent.imprint["symbolic_phase"] = planetary_phase
                agent.imprint["fixed_cycle"] = fixed_phase
