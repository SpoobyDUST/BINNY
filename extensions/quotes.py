import lightbulb
import hikari

quote_plugin = lightbulb.Plugin("quote", "Some quotes that you might find useful :)")

@quote_plugin.command()
@lightbulb.add_cooldown(3, 3, lightbulb.UserBucket)
@lightbulb.command("quote", "Send quotes!.", auto_defer = True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def dad(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get('https://quote-garden.herokuapp.com/api/v3/quotes/random') as resp:
        data = await resp.json()
    quote = data["data"][0]["quoteText"]
    author = data["data"][0]["quoteAuthor"]
    emb = hikari.Embed(description="Someone Has Already Said It Best")
    emb.add_field(name= f"**{quote}**", value= f"Quote by: {author}")
    emb.set_image("https://media.giphy.com/media/9D7egcpo4IUCJRwwzp/giphy.gif")
    emb.set_thumbnail('http://naturalbridgezoo.com/wp-content/uploads/2017/03/Cassawary3.jpg')
    emb.set_footer('Please Return Carrier Cassowary aka CaCa')
    
    await ctx.respond(embed=emb)

def load(bot):
    bot.add_plugin(quote_plugin)

def unload(bot):
    bot.remove_plugin(quote_plugin)