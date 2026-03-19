class Harvester:
    """
    Gathers symbolic alkaloids from agents using AlkaloidRefiner.
    Interfaces with ExportPipeline to externalize condensed insights.
    """
    def __init__(self, refiner, exporter):
        self.refiner = refiner
        self.exporter = exporter

    def harvest_from_agent(self, agent):
        """
        Scan agent memory for qualifying events and refine them.

        Args:
            agent: symbolic agent with memory

        Returns:
            list: exported file paths
        """
        new_exports = []
        for event in agent.memory.events[-50:]:  # recent window
            alkaloid = self.refiner.refine(agent, event)
            if alkaloid:
                path = self.exporter.export(alkaloid)
                new_exports.append(path)
        return new_exports

    def harvest_population(self, agents):
        """
        Run harvesting across a population.
        """
        all_exports = []
        for agent in agents:
            all_exports.extend(self.harvest_from_agent(agent))
        return all_exports
