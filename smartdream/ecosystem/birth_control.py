class BirthControl:
    """
    Manages symbolic agent population limits, lifecycle policies,
    and reproduction logic within an adaptive system.
    """
    def __init__(self, max_population=100):
        print("🐣 Initializing BirthControl")
        self.max_population = max_population
        self.population = []
        self.total_births = 0

    def register_birth(self):
        self.total_births += 1

    def can_birth(self):
        return self.total_births < self.max_population

    def register(self, agent):
        self.population.append(agent)
        if len(self.population) > self.max_population:
            self.cull_least_fit()

    def cull_least_fit(self):
        self.population.sort(key=lambda a: a.compute_fitness())
        removed = self.population.pop(0)
        removed.memory.record_event("culled", metadata={"reason": "low_fitness"})

    def eligible_for_birth(self, agent):
        return agent.compute_fitness() > 10 and len(self.population) < self.max_population

    def population_summary(self):
        return {
            "count": len(self.population),
            "max": self.max_population,
            "avg_fitness": round(sum(a.compute_fitness() for a in self.population) / max(1, len(self.population)), 2)
        }
