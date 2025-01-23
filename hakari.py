import asyncio
from fileinput import filename
import hikari
from hikari import Intents
from lavasnek_rs import Lavalink
import lightbulb
from lightbulb.ext import filament
import os
import miru
from miru.ext import nav 
import aiohttp
import concurrent.futures
from enum import auto
from logging import exception, raiseExceptions
from multiprocessing import Event
from tkinter import EventType
import io
from pathlib import Path

from dotenv import load_dotenv 
MEDIA_URL = "http://127.0.0.1:8000/media/" 

load_dotenv()
TOKEN = os.getenv("TOKEN")
hikari.Activity(name='To PsyOPs', type=hikari.ActivityType.LISTENING)
bot = lightbulb.BotApp(
    TOKEN,
    intents=hikari.Intents.ALL,
    
    default_enabled_guilds=(988579939655778324, 764963419920531457, 890010030408093706,1009170512779431998, 686007857644175380, 1002009682338136076, 1286207146530443285)
    )
miru.install(bot)  
 
@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print('DayWalkR Just Walked In')


@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()
    bot.d.process_pool = concurrent.futures.ProcessPoolExecutor()
    

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()
    bot.d.process_pool.shutdown(wait=True)

@bot.command #Decorator
@lightbulb.command('ping', 'Gives Bot Latency!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    embed=hikari.Embed(title=f"**My ping is {bot.heartbeat_latency * 1_000:.0f} ms.**", color=0x6100FF)
    embed.set_image('https://media.giphy.com/media/8TFzy0P5sY1dcNjxI0/giphy.gif')
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('group','This is a group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def my_group(ctx):
    pass

@my_group.child
@lightbulb.command('subcommand', 'This is a subcommand')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title='I am a subcommand, I do as Zaddy Commands!!')
    embed.set_image('https://media.giphy.com/media/26BkNrYYSj9onwJ0s/giphy.gif')
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())


@bot.command
@lightbulb.command('ape', 'What Ape Ready For?!?')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title='Ape Ready For SNu SNu')
    embed.set_image('https://media.giphy.com/media/SnioCkL9cd3B6/giphy.gif')
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())



@bot.command
@lightbulb.command('ye', 'All Praise')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title='All Praise To Ye')
    embed.set_image('https://geeksoncoffee.com/wp-content/uploads/2019/12/eeekscarykindofcuteoracutephotou1w650q60fmpjpgfitcropcropfaces22.jpg')
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('bet', 'What Your Suppose To Do')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.context) -> None:
    image_url = f"{MEDIA_URL}betmore-gregriba.gif"

    embed = hikari.Embed(title='What Do We Do?!?')
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('cucked', 'It Has No Soul?!?')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}cuckedx6.jpeg"

    embed = hikari.Embed(title="Ape Can't Beat The Box")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('stfu', 'Hey You!!')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Shut The Fuck Up.mp4f"

    embed = hikari.Embed(title="Now It's Time")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('thanks', 'Thank Someone For Their Service')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Thank You For Your Service.jpg"

    embed = hikari.Embed(title="Thank You For Your Service")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())


@bot.command
@lightbulb.command('simp', 'Simp Lyfe')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Simp Lyfe be Like.mp4"

    embed = hikari.Embed(title="A Simp In Natural Habitat")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('pinged', 'Who Did It?!?')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Who pinged me.mp4"

    embed = hikari.Embed(title="Who Pinged Me?!?")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('sad', 'Who The Sad Boi')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Sad Duck.mp4"

    embed = hikari.Embed(title="No One Knows What It's Like, To Be A Sad Duck")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('advice', 'Financial Advice')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}obama advice.jpg.gif"

    embed = hikari.Embed(title="Obama Says")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('dumpit', 'Use In Times Of Dampage')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Cliff but in  discord friendly.jpeg"

    embed = hikari.Embed(title="Prepare Thy Anus")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('brr', 'Oh, You KnoOow')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Becky Go BRR in Da Trap.mp4"

    embed = hikari.Embed(title="When Becky Brings The Printer")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('dampit', 'Use In Times Of Dampage')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title="Prepare Thy Pockets")
    embed.set_image("https://media.giphy.com/media/YRw676NBrmPeM/giphy.gif")
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('dip', 'Dip Financial Advice')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Kanye Buy The Dip.jpg"

    embed = hikari.Embed(title="Kanye Says")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('bye', 'The Final Goodbye')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Execute Order Kurt.jpg"

    embed = hikari.Embed(title="Execute Order Adios")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('bmw', 'Come Howl With Me')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}H O W L with me discord friendly.jpeg"

    embed = hikari.Embed(title="Come H O W L With Me!!")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('laugh', 'For When LOL Aint Enough')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Charlie Murphyyyy.mp4"
    
    embed = hikari.Embed(title="Charlie And The Gang")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('dale', 'Use For Smoke')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}Planet_Fitness_Selfie_X6.jpeg"
    
    embed = hikari.Embed(title="Dale Brings All The Smoke")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    await ctx.respond(embed=embed, components=view.build())

@bot.command
@lightbulb.command('blessings', 'Many Blessings')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    image_url = f"{MEDIA_URL}AAALLLLAAAHHHHHH mp4.mp4"
    
    embed = hikari.Embed(title="Allah Brings Great Glory")
    embed.set_image(image_url)
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    components=view.build()
    await ctx.respond(embed=embed, components=view.build())


@bot.command
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR))
@lightbulb.option('member', 'the target user',type=hikari.User , required = True)
@lightbulb.command('allahuakbar', 'Statistical Procurement')
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(title="Hello Mr.Anderson")
    embed.set_image('https://media.giphy.com/media/LMnpUqCHQ2CTP6KfZs/giphy.gif')
    view = miru.View()
    view.add_item(miru.Button(url='https://foot.wiki/image.php?id=40W2QF.jpg', label="Shhh Don't Click This Button.... But You Want To, Don't You"))
    await ctx.options.member.send(embed=embed, components=view.build())
    await ctx.respond(f"You've Been Contacted")


@bot.listen(lightbulb.events.CommandErrorEvent) 
async def on_error(event: lightbulb.CommandErrorEvent)-> None:
    embed = hikari.Embed(title='BWahaha')
    embed.add_field(name= "So Sad", value= "All The Years Of Your Life, Just To Get Here.")
    embed.set_image('https://dreager1.files.wordpress.com/2012/07/ash_ketchum_vs_hulk_by_leadapprentice.jpg?w=584')
    embed.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    embed.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/SpoobyDaPunk", label="LinkTree Goodies"))
    
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(embed=embed, components=view.build())
        raise event.exception


bot.load_extensions_from('./extensions')
bot.run(
    status=hikari.Status.ONLINE,
    activity=hikari.Activity(
        name="Covert Operations",
        type=hikari.ActivityType.LISTENING ,
    )
)