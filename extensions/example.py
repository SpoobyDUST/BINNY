from asyncio import events
from enum import auto
from logging import exception, raiseExceptions
from multiprocessing import Event
from tkinter import EventType
import hikari
from datetime import datetime, timedelta, timezone
from hikari.permissions import Permissions
import lightbulb
from fileinput import filename
import os 
import miru
from miru.ext import nav 

plugin = lightbulb.Plugin('Example')

timeout_plugin = lightbulb.Plugin("timeout", "timeout for a moment.")
timeout_plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS),
    lightbulb.checks.bot_has_guild_permissions(hikari.Permissions.MODERATE_MEMBERS)
)
TIMEOUT_PERMISSIONS = (
    Permissions.MODERATE_MEMBERS
)


def load(bot):
    bot.add_plugin(plugin)

@plugin.listener(hikari.GuildMessageCreateEvent)
async def print_messages(event):
    print(event.content)

@plugin.command
@lightbulb.command('howdy', 'Make You Feel Morning!')
@lightbulb.implements(lightbulb.SlashCommand)
async def howdy(ctx):
    await ctx.respond('Top Of The Morning Partner!!')

@plugin.command()
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MUTE_MEMBERS))
@lightbulb.option('reason','reason for muting the user',required=False)
@lightbulb.option('member','mention the user for muting them',type=hikari.Member,required=True)
@lightbulb.command('mute','Mute That Guy',auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def mute(ctx:lightbulb.Context):
    muteRole = ""
    Role =  await ctx.app.rest.fetch_roles(ctx.guild_id)
    for i in Role:
        if i.name.lower() == 'mute':
            muteRole = i
    if not muteRole:
        muteRole = await ctx.app.rest.create_role(ctx.guild_id,name="Mute",permissions=hikari.Permissions.VIEW_CHANNEL,color=(255,0,0))
    channels = ctx.get_guild().get_channels()
    for channel in dict(channels):
        await ctx.app.rest.edit_permission_overwrite(channel=channel,target=muteRole,allow=hikari.Permissions.VIEW_CHANNEL,deny=hikari.Permissions.SEND_MESSAGES)
    await ctx.app.rest.add_role_to_member(ctx.guild_id,ctx.options.member,muteRole,reason=str(ctx.options.reason))
    await ctx.options.member.send(f"You Were Muted In {ctx.get_guild().name} For {ctx.options.reason}")
    await ctx.respond(f"Muted {ctx.options.member.mention} for {ctx.options.reason}")    

@plugin.command()
@lightbulb.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MUTE_MEMBERS))
@lightbulb.option('member','mention the user for unmuting them',type=hikari.Member,required=True)
@lightbulb.command('unmute','UnMute That Guy, BLESSINGS',auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def unmute(ctx:lightbulb.Context):
    muteRole = ""
    Role =  await ctx.app.rest.fetch_roles(ctx.guild_id)
    for i in Role:
        if i.name.lower() == 'mute':
            muteRole = i
    channels = ctx.get_guild().get_channels()
    for channel in dict(channels):
        await ctx.app.rest.edit_permission_overwrite(channel=channel,target=muteRole,allow=hikari.Permissions.VIEW_CHANNEL,deny=hikari.Permissions.SEND_MESSAGES)
    await ctx.app.rest.remove_role_from_member(ctx.guild_id,ctx.options.member,muteRole,reason=str(ctx.options.reason))        
    await ctx.options.member.send(f"You Were UnMuted In {ctx.get_guild().name} For Time Served")
    await ctx.respond(f"UnMuted {ctx.options.member.mention} for Time Served")
       



def load(bot):
    bot.add_plugin(plugin)
