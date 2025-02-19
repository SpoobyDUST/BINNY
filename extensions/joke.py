import lightbulb
import hikari
from lightbulb.ext import filament

joke_plugin = lightbulb.Plugin("joke", "Jokes! But be wary for the offensive ones!")

@joke_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.option("lang", "The language of the joke", str, required=False, default = "en", choices = ["cs","de","en","es","fr","pt"])
@lightbulb.command("joke", "For all kinds of jokes! (Some might be offensive, be careful.)", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
@filament.utils.pass_options
async def joke(ctx: lightbulb.Context, lang) -> None:
    parameters = {
        "format": "json",
        "amount": 1,
        "lang": lang
    }
    
    async with ctx.bot.d.aio_session.get('https://v2.jokeapi.dev/joke/Any', params = parameters) as resp:
        data = await resp.json()
        
    emb = hikari.Embed(title="Here comes a joke!")
        
    jokecategory = data["category"]
    thetype = data["type"]
    
    if thetype == "twopart":
        setup = data["setup"]
        delivery = data["delivery"]
        emb.add_field(name=f"Category: **{jokecategory}**", value=f"{setup}\n{delivery}")
        emb.set_image("https://media.giphy.com/media/chndah8BjS4SCtoqwX/giphy.gif")
        emb.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
        emb.set_footer('Please Return Carrier Cassowary aka CaCa')
    if thetype == "single":
        joke = data["joke"]
        emb.add_field(name=f"Category: **{jokecategory}**", value=joke)
        emb.set_image("https://media.giphy.com/media/chndah8BjS4SCtoqwX/giphy.gif")
        emb.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
        emb.set_footer('Please Return Carrier Cassowary aka CaCa')
    if data["error"] == "true":
        await ctx.respond("An Error has occured!")
        return
        
    await ctx.respond(embed=emb)
    

def load(bot):
    bot.add_plugin(joke_plugin)

def unload(bot):
    bot.remove_plugin(joke_plugin)