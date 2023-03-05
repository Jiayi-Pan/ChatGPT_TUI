from enum import Enum
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.message import Message, MessageTarget
from textual.widgets import Button, Header, Footer, Static, Input, Markdown
from textual.widget import Widget
from textual.binding import Binding
from chatgpt_tui.structures import Agent


class UserInput(Static):
    """
    A widget where the user can type a message.
    """
    BINDINGS = [
        Binding('ctrl+s', 'send', 'Send', show=True, priority=False),
    ]

    class Utterance(Message):
        """Utterance a user typed."""
        def __init__(self, sender: MessageTarget, text: str) -> None:
            self.text = text
            super().__init__(sender)
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Input(name="input", placeholder="Type here...", classes="user_input_field")
        yield Button("Send", classes="user_send_button")
    
    async def action_send(self) -> None:
        """Called when the user presses enter."""
        await self.send()
    
    async def on_button_pressed(self) -> None:
        """Called when the user presses button."""
        await self.send()
    
    async def send(self) -> None:
        input_widget = self.query_one(Input)
        text = input_widget.value
        await self.post_message(self.Utterance(self, text))
        input_widget.value = ""
    


class AgentMessage(Static):
    """
    A widget that renders a message from an agent.
    """
    def __init__(self, agent: Agent, message: str = "") -> None:
        super().__init__()
        self.agent = agent
        self.message = message

    def compose(self) -> ComposeResult:
        if self.agent == Agent.User:
            yield Static("You:")
        elif self.agent == Agent.Bot:
            yield Static("Assistant:")
        elif self.agent == Agent.System:
            yield Static("System:")
        elif self.agent == Agent.ERROR:
            yield Static("Error:")
        else:
            raise ValueError("Agent must be either User or Bot")
        yield Markdown(self.message)