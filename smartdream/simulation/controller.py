from datetime import datetime
import random

from agents.agent import Agent
from memory.memory import Memory
from seer.seer_engine import SeerEngine
from symbolic.vision_channel import global_vision
from identity.planetary_clock import PlanetaryClock
from ecosystem.birth_control import BirthControl

class TimeContext:
    def __init__(self, tick, cycle, epoch="", phase_tag="", planetary_signature=None):
        self.tick = tick
        self.cycle = cycle
        self.epoch = epoch
        self.phase_tag = phase_tag
        self.planetary_signature = planetary_signature or {}

class Controller:
    def __init__(self, population_size):
        self.tick = 0
        self.cycle = 0
        self.birth_control = BirthControl(max_population=population_size)
        self.agents = []
        for _ in range(population_size):
            agent = Agent()
            self.agents.append(agent)
            self.birth_control.register(agent)
        self.planetary_clock = PlanetaryClock(seed_time=datetime.utcnow())

    def run_cycle(self):
        self.tick += 1
        self.cycle += 1

        planetary_signature = self.planetary_clock.get_signature(self.tick)

        time_context = TimeContext(
            tick=self.tick,
            cycle=self.cycle,
            epoch=self.identify_epoch(),
            phase_tag=self.generate_phase_tag(),
            planetary_signature=planetary_signature
        )

        for agent in self.agents:
            agent.perceive(time_context)
            prediction = agent.predict()
            global_vision.broadcast(agent.id, prediction)
            feedback = self.get_environment_feedback(prediction)
            agent.learn(feedback)
            agent.update_energy(feedback)
            agent.drift_or_adapt()

        # Optional pruning for long-run balance
        self.birth_control.cull_least_fit()

    def identify_epoch(self):
        return f"{self.cycle // 10:04d}"

    def generate_phase_tag(self):
        return f"{(self.cycle // 5) % 4:04d}"

    def get_environment_feedback(self, prediction):
        return {
            "accuracy": random.uniform(0, 1),
            "symbolic_clarity": random.choice(["clear", "ambiguous", "obscured"]),
            "impact": random.randint(-5, 5)
        }

    def simulate(self, num_cycles):
        for _ in range(num_cycles):
            self.run_cycle()
