import lightbulb
import hikari
import asyncio
from lightbulb.buckets import GuildBucket
import miru

pingstorm_plugin = lightbulb.Plugin("pingstorm", "ping deez nuts", include_datastore = True)

@pingstorm_plugin.command()
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.KICK_MEMBERS))
@lightbulb.add_cooldown(3600, 2, GuildBucket)
@lightbulb.set_max_concurrency(1, GuildBucket)
@lightbulb.option("amount", "The amount of the pings", int, required = False, default=5, min_value=1, max_value=100)
@lightbulb.option("user", "The target user", hikari.Member, required = True)
@lightbulb.command("pingstorm", "Ping specified user number of times", hidden=True, pass_options = True)
@lightbulb.implements(lightbulb.SlashCommand)
async def pingstorm(ctx: lightbulb.Context, amount: int, user: hikari.Member) -> None:
    if amount > 100:
        await ctx.respond("**WARNING:** **Maximum allowed amount is 100.**")
        return
    if user.id == ctx.bot.application.id:
        await ctx.respond("HA! You think it'll work against me?? Nice Try.", delete_after=3)
        user = ctx.author
        await asyncio.sleep(2)
    await ctx.respond("Ping Machine Initializing in 3 seconds!", delete_after=5)                
    await asyncio.sleep(3)
    await ctx.respond("Begin!", delete_after=5)
    ping = 0
    for x in range(amount):
        await ctx.respond(f"{user.mention} - {ping + 1}/{amount}", delete_after=10, user_mentions=True)
        ping += 1
        await asyncio.sleep(1)
    await ctx.respond("Finished!", delete_after=5)
    embed = hikari.Embed(title="Hello Mr.Anderson")
    embed.set_image('https://media.giphy.com/media/f0GIF5Y2vGAve/giphy-downsized-large.gif')
    embed.set_thumbnail('https://media.giphy.com/media/NRvtqX3xE3064/giphy.gif')
    view = miru.View()
    view.add_item(miru.Button(url='https://foot.wiki/image.php?id=40W2QF.jpg', label="Shhh Don't Click This Button.... But You Want To, Don't You"))
    await ctx.respond(embed=embed, components=view.build())
    


def load(bot):
    bot.add_plugin(pingstorm_plugin)

def unload(bot):
    bot.remove_plugin(pingstorm_plugin)