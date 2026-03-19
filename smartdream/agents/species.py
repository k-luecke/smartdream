import random

from agents.genome import Genome

# --- Symbolic Generation Cycles ---
# Older Wuxing-style:
wuxing_generation_cycle = {
    "Initiate": "Witness",
    "Witness": "Wanderer",
    "Wanderer": "Unmarked",
    "Unmarked": "Beacon",
    "Beacon": "Initiate"
}

wuxing_overcoming_cycle = {
    "Initiate": "Unmarked",
    "Witness": "Initiate",
    "Wanderer": "Beacon",
    "Unmarked": "Witness",
    "Beacon": "Wanderer"
}

# Current SMARTDREAM cycle:
generation_cycle = {
    "Wanderer": "Initiate",
    "Initiate": "Seeker",
    "Seeker": "Transmitter",
    "Transmitter": "Anchor",
    "Anchor": "Dissolver",
    "Dissolver": "Wanderer"
}

species_templates = {
    "Seraph": {
        "resonance_threshold": 0.03,
        "seer_threshold": 0.08,
        "confidence_modulation": 1.2,
        "entry_threshold": 0.7,
        "exit_threshold": 0.3
    },
    "Mycelid": {
        "resonance_threshold": 0.07,
        "seer_threshold": 0.02,
        "confidence_modulation": 0.9,
        "entry_threshold": 0.5,
        "exit_threshold": 0.2
    },
    "Chorite": {
        "resonance_threshold": 0.1,
        "seer_threshold": 0.04,
        "confidence_modulation": 1.0,
        "entry_threshold": 0.6,
        "exit_threshold": 0.4
    }
}

def assign_species_traits(agent):
    species_name = agent.genome.y.get("species")
    if species_name in species_templates:
        agent.expressed_traits.update(species_templates[species_name])
    else:
        agent.expressed_traits.update({
            "resonance_threshold": random.uniform(0.03, 0.1),
            "seer_threshold": random.uniform(0.01, 0.1),
            "confidence_modulation": random.uniform(0.8, 1.2),
            "entry_threshold": random.uniform(0.5, 0.8),
            "exit_threshold": random.uniform(0.2, 0.5)
        })

def are_symbolically_viable(agent1, agent2):
    s1 = agent1.imprint.get("symbol") if agent1.imprint else None
    s2 = agent2.imprint.get("symbol") if agent2.imprint else None
    if not s1 or not s2:
        return False
    return s2 == generation_cycle.get(s1) or s2 == wuxing_overcoming_cycle.get(s1)

def taoist_mate(agent1, agent2, mutation_rate=0.1):
    from agents.agent import Agent
    if not are_symbolically_viable(agent1, agent2):
        return None
    child_genome = agent1.genome.crossover(agent2.genome)
    child_genome.mutate(rate=mutation_rate)
    return Agent(
        name=f"{agent1.name[:2]}x{agent2.name[:2]}_offspring",
        genome=child_genome
    )


def clone_and_mutate(parent, mutation_rate=0.1):
    from agents.agent import Agent
    new_genome = Genome(
        y=parent.genome.y.copy(),
        x=parent.genome.x.copy(),
        v=parent.genome.v.copy()
    )
    new_genome.mutate(rate=mutation_rate)
    return Agent(genome=new_genome, name=f"{parent.name}_clone")


def sort_by_imprint(population: list["Agent"]) -> list["Agent"]:

    return sorted(population, key=lambda a: a.imprint.get("symbol", "") if a.imprint else "")

def initialize_population(size=10, naming_fn=None):
    from agents.agent import Agent
    agents = []
    for i in range(size):
        genome = Genome.random()
        name = naming_fn(i) if naming_fn else f"Seed_{i}"
        agents.append(Agent(name=name, genome=genome))
    return agents
