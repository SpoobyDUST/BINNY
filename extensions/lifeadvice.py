import lightbulb
import hikari
import json
import miru 

advice_plugin = lightbulb.Plugin("advices", "Some advices that might aid you in your journey of life! :)")

@advice_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("lifeadvice", "Send useful advices!.", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def dad(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(f'https://api.adviceslip.com/advice') as resp:
        data = json.loads(await resp.read())
    adv = data["slip"]["advice"]
    emb = hikari.Embed(title="Here's some advice for you :)", description=adv)
    emb.set_image('https://media.giphy.com/media/hsljPUxpxM5BhR8HAN/giphy.gif') 
    emb.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    emb.set_footer('Please Return Carrier Cassowary aka CaCa')
    view = miru.View()
    view.add_item(miru.Button(url="https://linktr.ee/X6DonaldDamus", label="LinkTree Goodies"))
    await ctx.respond(embed=emb, components=view.build())

def load(bot):
    bot.add_plugin(advice_plugin)

def unload(bot):
    bot.remove_plugin(advice_plugin)