import math

class SymbolicGravity:
    """
    Computes attractive or repulsive forces between symbolic bodies based on
    symbolic mass and spatial distance. Used for clustering, dispersion,
    or symbolic gravitational effects, including black hole pull and white hole push.
    """

    def __init__(self, gravitational_constant=1.0):
        """
        Initialize the symbolic gravity system.

        Args:
            gravitational_constant (float): Tunable constant for symbolic force strength.
        """
        self.G = gravitational_constant

    def force(self, mass1, mass2, distance, polarity=1):
        """
        Compute symbolic gravitational force with polarity.

        Args:
            mass1 (float): symbolic mass of body A.
            mass2 (float): symbolic mass of body B.
            distance (float): Euclidean distance between the two bodies.
            polarity (int): +1 for attractive (default), -1 for repulsive

        Returns:
            float: symbolic force value
        """
        if distance == 0:
            return float('inf')
        return polarity * self.G * (mass1 * mass2) / (distance ** 2)

    def distance(self, pos1, pos2):
        """
        Compute Euclidean distance between two 2D coordinates.

        Args:
            pos1 (tuple): (x1, y1)
            pos2 (tuple): (x2, y2)

        Returns:
            float: Euclidean distance
        """
        return math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)

    def directional_pull(self, pos1, pos2):
        """
        Return directional vector from pos1 to pos2.

        Args:
            pos1 (tuple): origin
            pos2 (tuple): destination

        Returns:
            tuple: direction vector (dx, dy)
        """
        return (pos2[0] - pos1[0], pos2[1] - pos1[1])

    def total_force_from_field(self, field, origin, target):
        """
        Compute total gravitational force from substrate mass.

        Args:
            field (SubstrateField): substrate grid
            origin (tuple): observing position
            target (tuple): attracting position

        Returns:
            float: symbolic force
        """
        distance = self.distance(origin, target)
        mass = field.query_density(target)
        observer_mass = field.query_density(origin)
        return self.force(observer_mass, mass, distance)

    def apply_blackhole_gravity(self, blackhole, origin, observer_mass=1.0):
        """
        Compute gravitational force from a black hole's mass effect.

        Args:
            blackhole (BlackHole): black hole instance
            origin (tuple): position of the observer
            observer_mass (float): mass of the observer

        Returns:
            float: attractive force toward black hole
        """
        distance = self.distance(origin, blackhole.location)
        return self.force(observer_mass, blackhole.mass_effect(), distance, polarity=+1)

    def apply_whitehole_push(self, whitehole, origin, observer_mass=1.0):
        """
        Compute repulsive symbolic force from a white hole.

        Args:
            whitehole (WhiteHole): white hole instance
            origin (tuple): position of the observer
            observer_mass (float): mass of the observer

        Returns:
            float: repulsive force away from white hole
        """
        distance = self.distance(origin, whitehole.location)
        return self.force(observer_mass, whitehole.intensity, distance, polarity=-1)
