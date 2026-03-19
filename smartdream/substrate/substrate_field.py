class SubstrateField:
    """
    The SubstrateField represents the symbolic terrain on which all agents, events,
    and mass-energy interactions are mapped. Each point can accumulate symbolic mass
    and be queried for density. This forms the base layer of the symbolic universe.
    """
    def __init__(self, dark_matter_ratio=5.66):
        # Key: (x, y) coordinate tuple, Value: symbolic mass (float)
        self.visible_grid = {}
        self.dark_grid = {}
        self.dark_matter_ratio = dark_matter_ratio

    def register_mass(self, location, mass):
        """
        Add symbolic mass to a specific coordinate.

        Args:
            location (tuple): (x, y) coordinate.
            mass (float): symbolic mass to add.
        """
        if location in self.visible_grid:
            self.visible_grid[location] += mass
            self.dark_grid[location] += mass * self.dark_matter_ratio
        else:
            self.visible_grid[location] = mass
            self.dark_grid[location] = mass * self.dark_matter_ratio

    def query_density(self, location):
        """
        Return the total symbolic mass (visible + dark) at a given coordinate.

        Args:
            location (tuple): (x, y) coordinate.

        Returns:
            float: total symbolic mass at the location.
        """
        visible = self.visible_grid.get(location, 0.0)
        dark = self.dark_grid.get(location, 0.0)
        return visible + dark

    def field_snapshot(self):
        """
        Return the full symbolic mass field (visible + dark).

        Returns:
            dict: copy of the combined grid.
        """
        snapshot = {}
        all_keys = set(self.visible_grid) | set(self.dark_grid)
        for key in all_keys:
            snapshot[key] = self.visible_grid.get(key, 0.0) + self.dark_grid.get(key, 0.0)
        return snapshot

    def decay_field(self, decay_rate=0.01):
        """
        Optionally apply decay to simulate symbolic entropy.

        Args:
            decay_rate (float): proportion to decay each coordinate's mass.
        """
        for loc in list(self.visible_grid.keys()):
            self.visible_grid[loc] *= (1 - decay_rate)
            if self.visible_grid[loc] < 1e-6:
                del self.visible_grid[loc]  # Remove near-zero entries to prevent clutter and improve performance

        for loc in list(self.dark_grid.keys()):
            self.dark_grid[loc] *= (1 - decay_rate)
            if self.dark_grid[loc] < 1e-6:
                del self.dark_grid[loc]

    def apply_symbolic_drift(self, drift_function):
        """
        Apply symbolic drift across the field using a user-defined function.
        This simulates symbolic migration or reallocation across the substrate.

        Args:
            drift_function (callable): function with signature (location, mass) -> (new_location, new_mass)
        """
        new_visible = {}
        for location, mass in self.visible_grid.items():
            new_location, new_mass = drift_function(location, mass)
            if new_location in new_visible:
                new_visible[new_location] += new_mass
            else:
                new_visible[new_location] = new_mass
        self.visible_grid = new_visible

        new_dark = {}
        for location, mass in self.dark_grid.items():
            new_location, new_mass = drift_function(location, mass)
            if new_location in new_dark:
                new_dark[new_location] += new_mass
            else:
                new_dark[new_location] = new_mass
        self.dark_grid = new_dark
