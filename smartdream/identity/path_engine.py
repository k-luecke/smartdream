import random
from collections import defaultdict

class PathEngine:
    """
    Assigns roles to agents based on schema-derived affinity, symbolic diversity,
    and emergent system needs, with flexibility and minimal fixed archetypal bias.
    """
    def __init__(self, society_roles=None):
        self.required_roles = society_roles or {
            "Seer": 1,
            "Synthesist": 2,
            "Observer": 2,
            "Tuner": 2,
            "Forager": 2,
        }
        self.current_role_counts = defaultdict(int)
        self.role_assignments = {}

    def assign_role(self, agent):
        """
        Assign a symbolic role based on agent schema traits and system needs.
        """
        schema = getattr(agent, "identity_schema", None) or "undefined"
        candidate_roles = self._schema_to_roles(schema)

        # Fill undersubscribed roles first
        for role in candidate_roles:
            if self.current_role_counts[role] < self.required_roles.get(role, 0):
                self._finalize_assignment(agent, role)
                return role

        # Otherwise assign randomly from compatible roles
        fallback_role = random.choice(candidate_roles)
        self._finalize_assignment(agent, fallback_role)
        return fallback_role

    def _schema_to_roles(self, schema):
        """
        Maps schema identity label to a plausible symbolic function set.
        Avoids hard-coded archetypes in favor of dynamic symbolic translation.
        """
        mappings = {
            "schema_0": ["Observer", "Forager"],
            "schema_1": ["Seer", "Synthesist"],
            "schema_2": ["Tuner", "Observer"],
            "schema_3": ["Forager", "Tuner"],
            "schema_4": ["Synthesist", "Seer"],
        }
        return mappings.get(schema, ["Drifter"])

    def _finalize_assignment(self, agent, role):
        self.role_assignments[agent.id] = role
        self.current_role_counts[role] += 1
        agent.memory.record_event("role_assignment", metadata={"role": role})
        agent.assigned_role = role
