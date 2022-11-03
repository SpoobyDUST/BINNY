import random
from enum import Enum
from PIL import Image
import hikari
import lightbulb
import miru

rpsls_plugin = lightbulb.Plugin("rpsls", "Rock Paper Scissor Lizard Spock!")

class RPSView(miru.View):
    RPS = ("Rock", "Paper", "Scissors", "Lizard", "Spock")

    win = hikari.Embed(
        title="RPSLS",
        description="You won! You chose `{}` and BINNY chose `{}`",
    )   

    lose = hikari.Embed(
        title="RPSLS",
        description="You lost! You chose `{}` and BINNY chose `{}`",
        
    )

    tie = hikari.Embed(
        title="RPSLS",
        description="You tied! You chose `{}` and BINNY chose `{}`",
        
    )

    def __init__(self):
        super().__init__(timeout=30.0)
        self._rps = random.choice(self.RPS)

    @miru.button(label="Rock", style=hikari.ButtonStyle.PRIMARY, emoji="🪨")
    async def rock(self, button: miru.Button, ctx: miru.Context) -> None:
        RESPONSES = {
            "Rock": self.tie,
            "Paper": self.lose,
            "Scissors": self.win,
            "Lizard":self.win,
            "Spock":self.lose,
        }

        RESPONSES[self._rps].description = RESPONSES[self._rps].description.format(
            self.rock.label, self._rps
        )

        await ctx.edit_response(RESPONSES[self._rps], components=None)
        self.stop()

    @miru.button(label="Paper", style=hikari.ButtonStyle.DANGER, emoji="🧻")
    async def paper(self, button: miru.Button, ctx: miru.Context) -> None:
        RESPONSES = {
            "Rock": self.win,
            "Paper": self.tie,
            "Scissors": self.lose,
            "Lizard":self.lose,
            "Spock":self.win,
        }

        RESPONSES[self._rps].description = RESPONSES[self._rps].description.format(
            self.paper.label, self._rps
        )

        await ctx.edit_response(RESPONSES[self._rps], components=None)
        self.stop()

    @miru.button(label="Scissors", style=hikari.ButtonStyle.SUCCESS, emoji="✂️")
    async def scissors(self, button: miru.Button, ctx: miru.Context) -> None:
        RESPONSES = {
            "Rock": self.lose,
            "Paper": self.win,
            "Scissors": self.tie,
            "Lizard":self.win,
            "Spock":self.lose,
        }

        RESPONSES[self._rps].description = RESPONSES[self._rps].description.format(
            self.scissors.label, self._rps
        )
        await ctx.edit_response(RESPONSES[self._rps], components=None)
        self.stop()

    @miru.button(label="Lizard", style=hikari.ButtonStyle.DANGER, emoji= "🦎")
    async def lizard(self, button:miru.Button, ctx: miru.Context) -> None:
        RESPONSES = {
            "Rock":self.lose,
            "Paper":self.win,
            "Scissors":self.lose,
            "Lizard":self.tie,
            "Spock":self.win,
            
        }

        RESPONSES[self._rps].description = RESPONSES[self._rps].description.format(
            self.lizard.label, self._rps
        )

        await ctx.edit_response(RESPONSES[self._rps], components=None)
        self.stop()

        

    @miru.button(label="Spock", style=hikari.ButtonStyle.SUCCESS, emoji= "🖖")
    async def spock(self, button:miru.Button, ctx: miru.Context) -> None:
        RESPONSES = {
            "Rock":self.win,
            "Paper":self.lose,
            "Scissors":self.win,
            "Lizard":self.lose,
            "Spock":self.tie,
        }

        RESPONSES[self._rps].description = RESPONSES[self._rps].description.format(
            self.spock.label, self._rps
        )

        await ctx.edit_response(RESPONSES[self._rps], components=None)
        self.stop()

    async def view_check(self, ctx: miru.Context) -> bool:
        if ctx.user != self.message.interaction.user:
            embed = hikari.Embed(
                title="Error",
                description="This command was not invoked by you!",
                
            )
            await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        self.rock.disabled = True
        self.paper.disabled = True
        self.scissors.disabled = True
        self.add_item(
            miru.Button(
                style=hikari.ButtonStyle.SECONDARY, label="Timed out", disabled=True
            )
        )

        await self.message.edit(components=self.build())


@rpsls_plugin.command()
@lightbulb.command("rpsls", "Play Rock,Paper,Scissors,Lizard,Spock with BINNY!", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rps(ctx: lightbulb.Context) -> None:
    view = RPSView()

    embed = hikari.Embed(
        title="RPSLS",
        description="Click on the button options to continue the game!",
        
    )

    await ctx.respond(embed=embed, components=view.build())

    message = await ctx.interaction.fetch_initial_response()
    view.start(message)
    await view.wait()

@rpsls_plugin.command
@lightbulb.add_cooldown(5, 5, lightbulb.UserBucket)
@lightbulb.command("rpslsrules", "Tells You Rule For Rock, Paper, Scissors, Lizard, Spock", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rules(ctx: lightbulb.Context):
    embed=hikari.Embed(title="Here are the rules for Rock, Paper, Scissors, Lizard, Spock") 
    embed.add_field(name="Rule 1", value="Scissors cuts paper")
    embed.add_field(name="Rule 2", value="Paper covers rock.")
    embed.add_field(name="Rule 3", value="Rock crushes lizard.")
    embed.add_field(name="Rule 4", value="Lizard poisons Spock.")
    embed.add_field(name="Rule 5", value="Spock smashes scissors.")
    embed.add_field(name="Rule 6", value="Scissors decapitates lizard.")
    embed.add_field(name="Rule 7", value="Lizard eats paper.")
    embed.add_field(name="Rule 8", value="Paper disproves Spock.")
    embed.add_field(name="Rule 9", value="Spock vaporizes rock.")
    embed.add_field(name="Rule 10", value="Rock crushes scissors.")
    embed.set_image('https://media.giphy.com/media/3ohc1bNYPZR8gQ5ybS/giphy.gif')
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/X6DonaldDamus", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(rpsls_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(rpsls_plugin)