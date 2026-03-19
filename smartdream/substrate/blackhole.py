import math
import random

class BlackHole:
    """
    A BlackHole acts as a symbolic sink, absorbing information, mass, and symbolic structure
    that crosses its event horizon. Some data may re-emerge as Hawking radiation.
    """

    def __init__(self, location, radius=3.0, radiation_chance=0.05):
        """
        Initialize the black hole at a fixed coordinate.

        Args:
            location (tuple): (x, y) coordinate of the singularity center.
            radius (float): radius of influence for absorption.
            radiation_chance (float): probability that absorbed data is radiated back.
        """
        self.location = location
        self.radius = radius
        self.radiation_chance = radiation_chance
        self.event_horizon = []
        self.absorption_log = []
        self.radiation_log = []

    def absorb(self, data, position, substrate=None):
        """
        Absorb symbolic data into the singularity if within range.

        Args:
            data (any): symbolic payload, agent, or event data
            position (tuple): (x, y) coordinate of the data
            substrate (SubstrateField, optional): substrate from which to void mass

        Returns:
            any: data if radiated back, None otherwise
        """
        if self._within_radius(position):
            self.event_horizon.append(data)
            self.absorption_log.append({"data": data, "type": type(data).__name__})

            if substrate:
                # Void both visible and dark mass at this location
                if position in substrate.visible_grid:
                    del substrate.visible_grid[position]
                if position in substrate.dark_grid:
                    del substrate.dark_grid[position]

            if random.random() < self.radiation_chance:
                self.radiation_log.append(data)
                return data  # Simulate Hawking radiation
            return None
        return data  # Not absorbed

    def _within_radius(self, position):
        """
        Check if a coordinate is within the absorption radius.

        Args:
            position (tuple): (x, y)

        Returns:
            bool: True if within radius
        """
        dx = position[0] - self.location[0]
        dy = position[1] - self.location[1]
        return math.sqrt(dx**2 + dy**2) <= self.radius

    def mass_effect(self):
        """
        Return symbolic mass equivalent based on entropy absorbed.

        Returns:
            float: symbolic mass of the black hole
        """
        return len(self.event_horizon) * 1.0

    def peek_singularity(self):
        """
        Experimental: peek at the last absorbed object (if allowed by simulation mode).

        Returns:
            any: last item absorbed or None
        """
        return self.event_horizon[-1] if self.event_horizon else None

    def log(self):
        """
        Return the absorption log (metadata only).

        Returns:
            list: list of dictionaries describing absorbed items
        """
        return list(self.absorption_log)

    def emitted_radiation(self):
        """
        Return symbolic packets radiated back into the substrate.

        Returns:
            list: previously emitted data
        """
        return list(self.radiation_log)
