from agents.agent import Agent
import random

def generate_signal():
    """Simulate a synthetic signal stream with trend + noise."""
    return random.uniform(-1, 1) + 0.2 * random.choice([-1, 1])

def run_simulation(steps=10):
    agents = [Agent(name=f"Agent_{i}") for i in range(3)]

    for t in range(steps):
        signal = generate_signal()
        timestamp = f"Step_{t}"

        for agent in agents:
            confidence = abs(signal)
            fever_flag = abs(signal) > 0.8
            action = agent.perceive_and_act(timestamp=timestamp, confidence=confidence, fever_flag=fever_flag)
            print(f"{timestamp} | {agent.name} | Action: {action} | Dose: {agent.dose.ratio:.2f}")

if __name__ == "__main__":
    run_simulation(steps=20)


# main.py
from simulation.controller import Controller
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "simulate":
        try:
            population_size = int(sys.argv[2]) if len(sys.argv) > 2 else 9
            num_cycles = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        except ValueError:
            print("Usage: python main.py simulate [population_size] [num_cycles] [--debug]")
            sys.exit(1)

        controller = Controller(population_size=population_size)
        controller.simulate(num_cycles=num_cycles)
        if '--debug' in sys.argv:
            print("\n[DEBUG] Final snapshot:")
            print(controller.__dict__)
    else:
        print("Usage: python main.py simulate [population_size] [num_cycles]")
