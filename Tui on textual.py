from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import ListView, ListItem, Label, Button

periods = ["custom", "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd"]


class PeriodListApp(App):
	list_view = ListView()
	CSS_PATH = 'style.css'

	def compose(self):
		with Vertical():
			yield self.list_view
			yield Button("Exit", id="exit", classes="exit")

	async def on_mount(self):
		for period in periods:
			await self.list_view.append(ListItem(Label(period)))

	def on_button_pressed(self, event: Button.Pressed):
		if event.button.id == "exit":
			self.exit()


if __name__ == "__main__":
	PeriodListApp().run()