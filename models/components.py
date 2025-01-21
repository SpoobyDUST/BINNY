import typing as t

import hikari
import miru


class BooleanButton(miru.Button):
    """A boolean toggle button."""

    def __init__(
        self,
        *,
        state: bool,
        label: t.Optional[str] = None,
        disabled: bool = False,
        row: t.Optional[int] = None,
        custom_id: t.Optional[str] = None,
    ) -> None:
        style = hikari.ButtonStyle.SUCCESS if state else hikari.ButtonStyle.DANGER
        emoji = "✔️" if state else "✖️"

        self.state = state

        super().__init__(style=style, label=label, emoji=emoji, disabled=disabled, row=row, custom_id=custom_id)

    async def callback(self, context: miru.View) -> None:
        self.state = not self.state

        self.style = hikari.ButtonStyle.SUCCESS if self.state else hikari.ButtonStyle.DANGER
        self.emoji = "✔️" if self.state else "✖️"
        self.view.value = (self.label, self.state)
        self.view.last_item = self
        self.view.last_ctx = context
        self.view.input_event.set()


class OptionButton(miru.Button):
    """Button that sets view value to label."""

    async def callback(self, context: miru.View) -> None:
        self.view.value = self.label
        self.view.last_item = self
        self.view.last_ctx = context
        self.view.input_event.set()



class OptionsSelect(miru.TextSelect):
    """Select that sets view value to first selected option's value."""

    async def callback(self, context: miru.View) -> None:
        self.view.value = self.values[0]
        self.view.last_item = self
        self.view.last_ctx = context
        self.view.input_event.set()


class BackButton(OptionButton):
    """Go back to page that ctx.parent is set to."""

    def __init__(self, parent: str, **kwargs) -> None:
        super().__init__(style=hikari.ButtonStyle.PRIMARY, custom_id=parent, label="Back", emoji="⬅️")
        self.kwargs = kwargs

    async def callback(self, context: miru.View) -> None:
        self.view.last_ctx = context
        self.view.last_item = self
        self.view.value = None
        self.view.input_event.set()
        await self.view.menu_actions[self.custom_id](**self.kwargs)


class QuitButton(OptionButton):
    """Quit settings, delete message."""

    def __init__(self) -> None:
        super().__init__(style=hikari.ButtonStyle.DANGER, label="Quit", emoji="⬅️")

    async def callback(self, context: miru.View) -> None:
        self.view.last_ctx = context
        self.view.last_item = self
        self.view.value = None
        await self.view.menu_actions["Quit"]()
        self.view.input_event.set()
