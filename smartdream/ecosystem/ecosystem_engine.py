from ecosystem.birth_control import BirthControl

class EcosystemEngine:
    """
    Symbolic ecosystem engine that simulates collective resource tension,
    symbolic niche competition, and mutual feedback loops.
    """
    def __init__(self, max_population=100):
        self.global_energy = 10000.0
        self.population_size = 0
        self.symbolic_pressure_map = {}
        self.symbol_population = {}
        self.birth_control = BirthControl(max_population=max_population)

    def register_agent(self, agent):
        self.population_size += 1
        self.birth_control.register(agent)

    def unregister_agent(self):
        self.population_size = max(0, self.population_size - 1)

    def eligible_for_birth(self, agent):
        return self.birth_control.eligible_for_birth(agent)

    def compute_resource_per_agent(self):
        if self.population_size == 0:
            return 0.0
        return self.global_energy / self.population_size

    def update(self):
        """Simulate energy decay or redistribution."""
        self.global_energy *= 0.999  # decay over time

    def inject_energy(self, amount):
        self.global_energy += amount

    def log_symbolic_pressure(self, symbol, pressure):
        self.symbolic_pressure_map[symbol] = pressure

    def get_symbolic_pressure(self, symbol):
        return self.symbolic_pressure_map.get(symbol, 0.0)

    def track_symbol_population(self, symbol):
        self.symbol_population[symbol] = self.symbol_population.get(symbol, 0) + 1

    def untrack_symbol_population(self, symbol):
        if symbol in self.symbol_population:
            self.symbol_population[symbol] = max(0, self.symbol_population[symbol] - 1)

    def drift_modifier(self, symbol):
        pressure = self.get_symbolic_pressure(symbol)
        return max(0.01, 1.0 - pressure)

    def mutation_modifier(self, symbol):
        population = self.symbol_population.get(symbol, 0)
        modifier = 1.0 / (1.0 + population)
        return max(0.01, modifier)

    
    def tick(self):
    # Symbolic ecosystem logic placeholder
        if hasattr(self, 'last_update'):
            self.last_update += 1
        else:
            self.last_update = 1

    
    
    
    
    
    
    def snapshot(self):
        return {
            "global_energy": self.global_energy,
            "agents": self.population_size,
            "energy_per_agent": self.compute_resource_per_agent(),
            "symbolic_pressure": dict(self.symbolic_pressure_map),
            "symbol_population": dict(self.symbol_population),
            "birth_control": self.birth_control.population_summary()
        }
