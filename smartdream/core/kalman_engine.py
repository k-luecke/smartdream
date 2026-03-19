import numpy as np

class KalmanEngine:
    """
    Multi-dimensional Kalman engine for SMARTDREAM agents.
    Tracks signal inputs like price, momentum, volatility, and supertrend.
    Computes filtered signal state and detects symbolic fever conditions.
    """

    def __init__(self, process_variance=1e-5, measurement_variance=0.01, fever_threshold=0.05):
        self.dimensions = ["price", "momentum", "volatility", "supertrend"]
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.fever_threshold = fever_threshold

        self.state = {dim: 0.0 for dim in self.dimensions}
        self.variance = {dim: 1.0 for dim in self.dimensions}
        self.delta = {dim: 0.0 for dim in self.dimensions}
        self.previous_state = {dim: None for dim in self.dimensions}

    def update(self, observations):
        """
        Update Kalman state for each input dimension.
        :param observations: dict with keys ['price', 'momentum', 'volatility', 'supertrend']
        :return: dict of filtered states
        """
        filtered = {}
        for dim in self.dimensions:
            z = observations.get(dim, None)
            if z is None:
                continue

            prior = self.state[dim]
            prior_var = self.variance[dim]

            # Kalman Gain
            gain = prior_var / (prior_var + self.measurement_variance)

            # Update estimate
            updated = prior + gain * (z - prior)
            updated_var = (1 - gain) * prior_var + self.process_variance

            self.previous_state[dim] = self.state[dim]
            self.delta[dim] = updated - self.state[dim]

            self.state[dim] = updated
            self.variance[dim] = updated_var
            filtered[dim] = updated

        return filtered

    def detect_fever(self):
        """
        Detect symbolic fever by checking if any delta exceeds threshold.
        :return: bool
        """
        return any(abs(self.delta[dim]) > self.fever_threshold for dim in self.dimensions)

    def summary(self):
        """
        Return symbolic summary of signal states and fever.
        """
        return {
            "state": self.state.copy(),
            "delta": self.delta.copy(),
            "fever": self.detect_fever()
        }
