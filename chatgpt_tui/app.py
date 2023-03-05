from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Input, Static
from chatgpt_tui.widgets import UserInput, AgentMessage
from chatgpt_tui.structures import Agent, History
from chatgpt_tui.chat_api import get_openai_response
from textual.binding import Binding
import pyperclip

class ChatApp(App):
    CSS_PATH = "style.css"
    history: History = History()
    BINDINGS = [
        Binding('ctrl+d', 'toggle_dark', 'Toggle dark mode', show=True, priority=True),
        Binding('ctrl+y', 'yank', 'Yank latest message', show=True, priority=True),
        ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Container(*self.compose_history(), id="chat_container")
        yield UserInput()
        yield Static("Ctrl+s: Send | Ctrl+y: Yank latest message | Ctrl+d: Toggle dark mode") # temporal solution
        # yield Footer() 
    
    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_yank(self) -> None:
        if self.history.data:
            pyperclip.copy(self.history.data[-1][1])

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # this allows the user to type immediately
        self.query_one(Input).focus()
    
    def compose_history(self) -> ComposeResult:
        history_widgets = []
        for agent, utterance in self.history.data:
            history_widgets.append(AgentMessage(agent, utterance))
        return history_widgets
    
    async def on_user_input_utterance(self, message: UserInput.Utterance) -> None:
        self.history.add_utterance(Agent.User, message.text)
        self.query_one("#chat_container").mount(AgentMessage(Agent.User, message.text))
        await self.add_bot_response()

    async def add_bot_response(self):
        succeed, bot_response = await get_openai_response(self.history.export())
        if succeed:
            self.history.add_utterance(Agent.Bot, bot_response)
            self.query_one("#chat_container").mount(AgentMessage(Agent.Bot, bot_response))
        else:
            self.history.add_utterance(Agent.ERROR, bot_response)
            self.query_one("#chat_container").mount(AgentMessage(Agent.ERROR, bot_response))

def run():
    app = ChatApp()
    app.run()


if __name__ == "__main__":
    run()