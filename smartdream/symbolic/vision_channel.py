import random
from datetime import datetime
from symbolic.vision_field import VisionField
from substrate.core.holo_fractal_field import HoloFractalField

class VisionChannel:
    """
    Agent-facing interface for symbolic perception and broadcast.
    Now includes fractal echoes from the HoloFractalField.
    """
    def __init__(self, agent, field=None, fractal=None):
        self.memory_decay_rate = 0.01
        self.agent = agent
        self.field = field  # shared symbolic environment (VisionField)
        self.fractal = fractal or HoloFractalField()
        self.symbol_memory = []  # local cache of perceived symbols

    def perceive(self):
        """
        Pull symbolic inputs from the shared VisionField and fractal field.
        Logs fractal echo into agent memory and includes echo in perception.

        Returns:
            list[str]: symbols perceived this cycle
        """
        perceived = []

        if self.field:
            perceived += self.field.emit_to(self.agent)
        else:
            perceived += random.choices(
                ["form", "break", "noise", "flow", "phase", "edge"], k=2
            )

        fractal_echo = self.fractal.pulse(zoom=random.choice([0, 1, 2]))

        self.agent.memory.record_event(
            "fractal_echo",
            timestamp=datetime.now(),
            metadata=fractal_echo
        )

        self.agent.memory.record_event(
            "fractal_perception",
            timestamp=datetime.now(),
            metadata={"symbols": [fractal_echo["archetype_seed"]]}
        )

        perceived.append(fractal_echo["archetype_seed"])
        self.symbol_memory.extend(perceived)
        return perceived

    def broadcast(self, symbols):
        """
        Push symbolic output to the field (e.g. rituals, insight).

        Args:
            symbols (list[str]): tags to emit
        """
        if self.field:
            self.field.receive_from(self.agent, symbols)

    def tick(self):
        """
        Apply memory decay to simulate symbolic forgetting.
        """
        for i in range(len(self.symbol_memory)):
            if random.random() < self.memory_decay_rate:
                self.symbol_memory[i] = None
        self.symbol_memory = [s for s in self.symbol_memory if s is not None]

    def get_recent(self, n=10):
        """
        Retrieve recent symbolic perceptions for logging or reflection.

        Args:
            n (int): how many symbols to return

        Returns:
            list[str]: recent symbols
        """
        return self.symbol_memory[-n:]
