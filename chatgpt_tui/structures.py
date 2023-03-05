from enum import Enum

class Agent(Enum):
    System = 0
    Bot = 1
    User = 2
    ERROR = 3

class History:
    def __init__(self, history: list[(Agent, str)] = []) -> None:
        super().__init__()
        self.data = history

    def add_utterance(self, agent: Agent, utterance: str) -> None:
        self.data.append((agent, utterance))
    
    def export(self) -> list[dict]:
        exported_history = []
        for agent, utterance in self.data:
            if agent == Agent.System:
                exported_history.append({"role": "system", "content": utterance})
            elif agent == Agent.Bot:
                exported_history.append({"role": "assistant", "content": utterance})
            elif agent == Agent.User:
                exported_history.append({"role": "user", "content": utterance})
            else:
                raise ValueError("Agent must be either User or Bot")
        return exported_history