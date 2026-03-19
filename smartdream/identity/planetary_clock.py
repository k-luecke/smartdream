import math
from datetime import datetime, timedelta

class PlanetaryClock:
    def __init__(self, seed_time=None):
        self.seed_time = seed_time or datetime.utcnow()
        self.orbital_periods = {
            "planet1": 60,   # in ticks (e.g., days)
            "planet2": 90
        }

    def get_signature(self, tick):
        angle1 = self._calculate_orbital_angle(tick, self.orbital_periods["planet1"])
        angle2 = self._calculate_orbital_angle(tick, self.orbital_periods["planet2"])
        angle_diff = abs(angle1 - angle2) % 360
        if angle_diff > 180:
            angle_diff = 360 - angle_diff

        planet_relation = (angle2 - angle1 + 360) % 360

        return {
            "planet1_angle": round(angle1, 2),
            "planet2_angle": round(angle2, 2),
            "angle_diff": round(angle_diff, 2),
            "planet_relation_angle": round(planet_relation, 2)
        }

    def _calculate_orbital_angle(self, tick, period):
        # Complete orbit = 360 degrees
        return (tick % period) / period * 360
