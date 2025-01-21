import asyncio
import datetime
import logging
import os
import random
import typing as t
from enum import IntEnum
from io import BytesIO
from pathlib import Path
from textwrap import fill
import pathlib

import hikari
import Levenshtein as lev
import lightbulb
import miru
from miru.ext import nav
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


from etc import constants as const

from models.checks import bot_has_permissions
from utils import helpers
from utils.dictionaryapi import DictionaryClient
from utils.dictionaryapi import DictionaryEntry
from utils.dictionaryapi import DictionaryException
from utils.dictionaryapi import UrbanEntry

base_dir = str(pathlib.Path(os.path.abspath(__file__)).parents[1])


logger = logging.getLogger(__name__)

fun = lightbulb.Plugin("Fun")

if api_key := os.getenv("DICTIONARYAPI_API_KEY"):
    dictionary_client = DictionaryClient(api_key)
else:
    dictionary_client = None



@fun.set_error_handler()
async def handle_errors(event: lightbulb.CommandErrorEvent) -> bool:
    if isinstance(event.exception, lightbulb.CheckFailure) and isinstance(
        event.exception.__cause__, DictionaryException
    ):
        await event.context.respond(
            embed=hikari.Embed(
                title="❌ No Dictionary API key provided",
                description="This command is currently unavailable.\n\n**Information:**\nPlease set the `DICTIONARYAPI_API_KEY` environment variable to use the Dictionary API.",
                color=const.ERROR_COLOR,
            )
        )
        return True

    return False


class WinState(IntEnum):
    PLAYER_X = 0
    PLAYER_O = 1
    TIE = 2


class TicTacToeButton(miru.Button):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(style=hikari.ButtonStyle.SECONDARY, label="\u200b", row=y)
        self.x: int = x
        self.y: int = y

    async def callback(self, ctx: miru.Context) -> None:
        if isinstance(self.view, TicTacToeView) and self.view.current_player.id == ctx.user.id:
            view: TicTacToeView = self.view
            value: int = view.board[self.y][self.x]

            if value in (view.size, -view.size):  # If already clicked
                return

            if view.current_player.id == view.playerx.id:
                self.style = hikari.ButtonStyle.DANGER
                self.label = "X"
                self.disabled = True
                view.board[self.y][self.x] = -1
                view.current_player = view.playero
                embed = hikari.Embed(
                    title="Tic Tac Toe!",
                    description=f"It is **{view.playero.display_name}**'s turn!",
                    color=0x009DFF,
                ).set_thumbnail(view.playero.display_avatar_url)

            else:
                self.style = hikari.ButtonStyle.SUCCESS
                self.label = "O"
                self.disabled = True
                view.board[self.y][self.x] = 1
                view.current_player = view.playerx
                embed = hikari.Embed(
                    title="Tic Tac Toe!",
                    description=f"It is **{view.playerx.display_name}**'s turn!",
                    color=0x009DFF,
                ).set_thumbnail(view.playerx.display_avatar_url)

            winner = view.check_winner()

            if winner is not None:

                if winner == WinState.PLAYER_X:
                    embed = hikari.Embed(
                        title="Tic Tac Toe!",
                        description=f"**{view.playerx.display_name}** won!",
                        color=0x77B255,
                    ).set_thumbnail(view.playerx.display_avatar_url)

                elif winner == WinState.PLAYER_O:
                    embed = hikari.Embed(
                        title="Tic Tac Toe!",
                        description=f"**{view.playero.display_name}** won!",
                        color=0x77B255,
                    ).set_thumbnail(view.playero.display_avatar_url)

                else:
                    embed = hikari.Embed(
                        title="Tic Tac Toe!", description=f"It's a tie!", color=0x77B255
                    ).set_thumbnail(None)

                for button in view.children:
                    assert isinstance(button, miru.Button)
                    button.disabled = True

                view.stop()

            await ctx.edit_response(embed=embed, components=view.build())


class TicTacToeView(miru.View):
    def __init__(self, size: int, playerx: hikari.Member, playero: hikari.Member, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.current_player: hikari.Member = playerx
        self.size: int = size
        self.playerx: hikari.Member = playerx
        self.playero: hikari.Member = playero

        if size in [3, 4, 5]:
            # Create board
            self.board = [[0 for _ in range(size)] for _ in range(size)]

        else:
            raise TypeError("Invalid size specified. Must be either 3, 4, 5.")

        for x in range(size):
            for y in range(size):
                self.add_item(TicTacToeButton(x, y))

    async def on_timeout(self) -> None:
        for item in self.children:
            assert isinstance(item, miru.Button)
            item.disabled = True

        assert self.message is not None

        await self.message.edit(
            embed=hikari.Embed(
                title="Tic Tac Toe!",
                description="This game timed out! Try starting a new one!",
                color=0xFF0000,
            ),
            components=self.build(),
        )

    def check_blocked(self) -> bool:
        """
        Check if the board is blocked
        """
        blocked_list = [False, False, False, False]

        # TODO: Replace this old garbage

        # Check rows
        blocked = []
        for row in self.board:
            if not (-1 in row and 1 in row):
                blocked.append(False)
            else:
                blocked.append(True)

        if blocked.count(True) == len(blocked):
            blocked_list[0] = True

        # Check columns
        values = []
        for col in range(self.size):
            values.append([])
            for row in self.board:
                values[col].append(row[col])

        blocked = []
        for col in values:
            if not (-1 in col and 1 in col):
                blocked.append(False)
            else:
                blocked.append(True)
        if blocked.count(True) == len(blocked):
            blocked_list[1] = True

        # Check diagonals
        values = []
        diag_offset = self.size - 1
        for i in range(0, self.size):
            values.append(self.board[i][diag_offset])
            diag_offset -= 1
        if -1 in values and 1 in values:
            blocked_list[2] = True

        values = []
        diag_offset = 0
        for i in range(0, self.size):
            values.append(self.board[i][diag_offset])
            diag_offset += 1
        if -1 in values and 1 in values:
            blocked_list[3] = True

        if blocked_list.count(True) == len(blocked_list):
            return True

        return False

    def check_winner(self) -> t.Optional[WinState]:
        """
        Check if there is a winner
        """

        # Check rows
        for row in self.board:
            value = sum(row)
            if value == self.size:
                return WinState.PLAYER_O
            elif value == -self.size:
                return WinState.PLAYER_X

        # Check columns
        for col in range(self.size):
            value = 0
            for row in self.board:
                value += row[col]
            if value == self.size:
                return WinState.PLAYER_O
            elif value == -self.size:
                return WinState.PLAYER_X

        # Check diagonals
        diag_offset_1 = self.size - 1
        diag_offset_2 = 0
        value_1 = 0
        value_2 = 0
        for i in range(0, self.size):
            value_1 += self.board[i][diag_offset_1]
            value_2 += self.board[i][diag_offset_2]
            diag_offset_1 -= 1
            diag_offset_2 += 1
        if value_1 == self.size or value_2 == self.size:
            return WinState.PLAYER_O
        elif value_1 == -self.size or value_2 == -self.size:
            return WinState.PLAYER_X

        # Check if board is blocked
        if self.check_blocked():
            return WinState.TIE




@fun.command
@lightbulb.option("size", "The size of the board. Default is 3.", required=False, choices=["3", "4", "5"])
@lightbulb.option("user", "The user to play tic tac toe with!", type=hikari.Member)
@lightbulb.command("tictactoe", "Play tic tac toe with someone!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def tictactoe(ctx:lightbulb.Context, user: hikari.Member, size: t.Optional[str] = None) -> None:
    size_int = int(size or 3)
    helpers.is_member(user)
    assert ctx.member is not None

    if user.id == ctx.author.id:
        await ctx.respond(
            embed=hikari.Embed(
                title="❌ Invoking self",
                description=f"I'm sorry, but how would that even work?",
                color=const.ERROR_COLOR,
            ),
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if not user.is_bot:
        view = TicTacToeView(size_int, ctx.member, user)
        proxy = await ctx.respond(
            embed=hikari.Embed(
                title="Tic Tac Toe!",
                description=f"**{user.display_name}** was challenged for a round of tic tac toe by **{ctx.member.display_name}**!\nFirst to a row of **{size_int} wins!**\nIt is **{ctx.member.display_name}**'s turn!",
                color=const.EMBED_BLUE,
            ).set_thumbnail(ctx.member.display_avatar_url),
            components=view.build(),
        )
        await view.start(await proxy.message())

    else:
        await ctx.respond(
            embed=hikari.Embed(
                title="❌ Invalid user",
                description=f"Sorry, but you cannot play with a bot.. yet...",
                color=const.ERROR_COLOR,
            ),
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return


@fun.command
@lightbulb.set_max_concurrency(1, lightbulb.ChannelBucket)
@lightbulb.add_checks(bot_has_permissions(hikari.Permissions.ADD_REACTIONS))
@lightbulb.option("length", "The amount of words provided.", required=False, type=int, min_value=1, max_value=15)
@lightbulb.option(
    "difficulty", "The difficulty of the words provided.", choices=["easy", "medium", "hard"], required=False
)
@lightbulb.command("typeracer", "Start a typerace to see who can type the fastest!", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def typeracer(ctx: lightbulb.Context, difficulty: t.Optional[str] = None, length: t.Optional[int] = None) -> None:
    length = length or 5
    difficulty = difficulty or "medium"

    file = open(Path(r'etc\text', f"words_{difficulty}.txt"), "r", encoding='utf-8')
    words = [word.strip() for word in file.readlines()]
    font = Path(r"etc\fonts\roboto-slab.ttf")
    text = " ".join([random.choice(words) for i in range(0, length)])
    file.close()

    await ctx.respond(
        embed=hikari.Embed(
            title=f"🏁 Typeracing begins {helpers.format_dt(helpers.utcnow() + datetime.timedelta(seconds=10), style='R')}",
            description="Prepare your keyboard of choice!",
            color=const.EMBED_BLUE,
        )
    )

    await asyncio.sleep(10.0)

    def create_image() -> BytesIO:
        display_text = fill(text, 60)

        img = Image.new("RGBA", (1, 1), color=0)  # 1x1 transparent image
        draw = ImageDraw.Draw(img)
        outline = ImageFont.truetype(str(font), 42)
        text_font = ImageFont.truetype(str(font), 40)

        # Resize image for text
        textwidth, textheight = draw.textsize(display_text, outline)
        margin = 20
        img = img.resize((textwidth + margin, textheight + margin))
        draw = ImageDraw.Draw(img)
        # draw.text(
        #    (margin/2, margin/2), display_text, font=outline, fill=(54, 57, 63)
        # )
        draw.text((margin / 2, margin / 2), display_text, font=text_font, fill="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer

    buffer: BytesIO = await asyncio.get_running_loop().run_in_executor(None, create_image)
    await ctx.respond(
        embed=hikari.Embed(
            description="🏁 Type in the text from above as fast as you can!",
            color=const.EMBED_BLUE,
        ),
        attachment=hikari.Bytes(buffer.getvalue(), "sned_typerace.png"),
    )

    end_trigger = asyncio.Event()
    start = helpers.utcnow()
    winners = {}

    def predicate(event: hikari.GuildMessageCreateEvent) -> bool:
        message = event.message

        if not message.content:
            return False

        if ctx.channel_id == message.channel_id and text.lower() == message.content.lower():
            winners[message.author] = (helpers.utcnow() - start).total_seconds()
            asyncio.create_task(message.add_reaction("✅"))
            end_trigger.set()

        elif ctx.channel_id == message.channel_id and lev.distance(text.lower(), message.content.lower()) < 5:
            asyncio.create_task(message.add_reaction("❌"))

        return False

    msg_listener = asyncio.create_task(
        ctx.bot.wait_for(hikari.GuildMessageCreateEvent, predicate=predicate, timeout=None)
    )

    try:
        await asyncio.wait_for(end_trigger.wait(), timeout=60)
    except asyncio.TimeoutError:
        await ctx.respond(
            embed=hikari.Embed(
                title="🏁 Typeracing results",
                description="Nobody was able to complete the typerace within **60** seconds. Typerace cancelled.",
                color=const.ERROR_COLOR,
            )
        )

    else:
        await ctx.respond(
            embed=hikari.Embed(
                title="🏁 First Place",
                description=f"**{list(winners.keys())[0]}** finished first, everyone else has **15 seconds** to submit their reply!",
                color=const.EMBED_GREEN,
            )
        )
        await asyncio.sleep(15.0)

        desc = "**Participants:**\n"
        for winner in winners:
            desc = f"{desc}**#{list(winners.keys()).index(winner)+1}** **{winner}** `{round(winners[winner], 1)}` seconds - `{round((len(text) / 5) / (winners[winner] / 60))}`WPM\n"

        await ctx.respond(
            embed=hikari.Embed(
                title="🏁 Typeracing results",
                description=desc,
                color=const.EMBED_GREEN,
            )
        )

    finally:
        msg_listener.cancel()


@fun.command
@lightbulb.app_command_permissions(None, dm_enabled=False)
@lightbulb.command("funfact", "Shows a random fun fact.")
@lightbulb.implements(lightbulb.SlashCommand)
async def funfact(ctx: lightbulb.Context) -> None:
    fun_path = Path(r"etc\text\funfacts.txt")
    fun_facts = open(fun_path, "r", encoding='utf-8').readlines()
    
    embed=hikari.Embed(
            title="🤓 Did you know?",
            description=f"{random.choice(fun_facts)}",
            color=const.EMBED_BLUE,
        )
    embed.set_image('https://media.giphy.com/media/JgfJrINqmg6dNw3qJ3/giphy.gif')
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    await ctx.respond(embed)

@fun.command
@lightbulb.app_command_permissions(None, dm_enabled=False)
@lightbulb.option("question", "The question you want to ask of the mighty 8ball.")
@lightbulb.command("8ball", "Ask a question, and the answers shall reveal themselves.", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def eightball(ctx: lightbulb.Context, question: str) -> None:
    ball_path = Path(r"C:\Users\scott\Desktop\DayWalkR\etc\text\8ball.txt")
    answers = open(ball_path, "r").readlines()
    color = hikari.Color(0x26D934)
    eightball = hikari.Embed(color=color)
    eightball.add_field(name="Question:", value=question.capitalize(), inline=False)
    eightball.add_field(name="Answer:", value= random.choice(answers))
    eightball.set_author(name = "The Mighty 8-Ball")
    eightball.set_footer(f"Requested by: {ctx.author.username}", icon=ctx.author.avatar_url)
    eightball.set_thumbnail("https://i.imgur.com/Q9dxpTz.png")
    await ctx.respond(eightball)



@fun.command
@lightbulb.option("query", "The query you want to search for on Wikipedia.")
@lightbulb.command("wiki", "Search Wikipedia for articles!", auto_defer=True, pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def wiki(ctx: lightbulb.Context, query: str) -> None:
    link = "https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=5"

    async with ctx.bot.d.aio_session.get(link.format(query=query)) as response:
        results = await response.json()
        results_text = results[1]
        results_link = results[3]

        if results_text:
            desc = "\n".join([f"[{result}]({results_link[i]})" for i, result in enumerate(results_text)])
            embed = hikari.Embed(
                title=f"Wikipedia: {query}",
                description=desc,
                color=const.MISC_COLOR,
            )
            embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
            embed.set_footer('Please Return Carrier Cassowary aka CaCa')
        else:
            embed = hikari.Embed(
                title="❌ No results",
                description="Could not find anything related to your query.",
                color=const.ERROR_COLOR,
            )
            embed.set_image('https://media.giphy.com/media/IHOOMIiw5v9VS/giphy.gif')
            embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
            embed.set_footer('Please Return Carrier Cassowary aka CaCa')
        await ctx.respond(embed=embed)


def load(bot) -> None:
    bot.add_plugin(fun)


def unload(bot) -> None:
    bot.remove_plugin(fun)