# agents/agent_factory.py

from agents.agent import Agent

class AgentFactory:
    """
    🏭 AgentFactory creates new agents, verifying conditions with the
    BirthControlEngine and assigning symbolic starting attributes or echoes.
    """

    def __init__(self, birth_control_engine):
        self.birth_control = birth_control_engine
        self.agent_id_counter = 0
        self.log = []

    ### 🔹 Main birth function
    def try_birth_agent(self, extra_params=None):
        """Attempt to create a new agent if birth is permitted."""
        if not self.birth_control.can_birth():
            return None

        agent = Agent(agent_id=self.agent_id_counter)
        self.agent_id_counter += 1

        # Optional: inject symbolic echo, karma, imprint, etc.
        if extra_params:
            for key, value in extra_params.items():
                setattr(agent, key, value)

        self.birth_control.register_birth()
        self.log.append({"event": "birth", "agent_id": agent.agent_id})
        return agent

    ### 🔹 Optional rebirth from death
    def rebirth_from_agent(self, dead_agent):
        """Optional karma-aware rebirth with echo inheritance."""
        if not self.birth_control.can_birth():
            return None

        new_agent = Agent(agent_id=self.agent_id_counter)
        self.agent_id_counter += 1

        # Pass on karma or fragments
        new_agent.karma.karma_score = dead_agent.karma.karma_score * 0.5
        new_agent.imprint = {"symbol": dead_agent.imprint.get("symbol", "Wanderer")}

        self.birth_control.register_birth()
        self.log.append({"event": "rebirth", "agent_id": new_agent.agent_id})
        return new_agent

    ### 🔹 Tracking
    def summarize(self):
        return {
            "created": self.agent_id_counter,
            "log": self.log
        }
