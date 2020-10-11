# Modified MIT License (MIT)
#
# Copyright (c) 2020 shroomdog27
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, and sublicense
# the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import discord
from redbot.core import commands, Config, checks


class nvite(commands.Cog):
    """default_message"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=163490961253466112)
        default_guild = {"channel": None, "max_age": 0, "max_uses": 1, "temporary": False}
        self.config.register_guild(**default_guild)

    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(create_instant_invite=True)
    async def nvite(self, ctx):
        """Creates an invite"""
        guild = ctx.guild
        channel_txt_id = await self.config.guild(guild).channel()
        if channel_txt_id is None:
            ctx.send("This guild's settings haven't been configured!")
            return
        channel = guild.get_channel(channel_txt_id)
        if channel is None:
            ctx.send("I couldn't find this guild's configured channel!")
            return
        invite = await channel.create_invite(
            max_age=await self.config.guild(guild).max_age(),
            max_uses=await self.config.guild(guild).max_uses(),
            temporary=await self.config.guild(guild).temporary(),
            unique=True,
            reason=f"Requested invite by {ctx.author.display_name} ({ctx.author.id})",
        )
        await ctx.send(f"Here is your invite {invite}")
        return

    @commands.group()
    @commands.guild_only()
    @checks.mod_or_permissions(manage_channels=True)
    async def nviteset(self, ctx):
        """Change settings for all created invites"""
        pass

    @nviteset.command(name="channel")
    @commands.guild_only()
    async def nviteset_channel(self, ctx, channel: discord.TextChannel):
        """Sets the channel to attach the invite to."""
        await self.config.guild(ctx.guild).channel.set(channel.id)
        await ctx.tick()
        return

    @nviteset.command(name="age")
    @commands.guild_only()
    async def nviteset_age(self, ctx, age: int):
        """
        Sets the max age of all created invites.
        This value is in seconds.
        """
        await self.config.guild(ctx.guild).max_age.set(age)
        await ctx.tick()
        return

    @nviteset.command(name="uses")
    @commands.guild_only()
    async def nviteset_uses(self, ctx, uses: int):
        """Sets the max uses of all created invites"""
        await self.config.guild(ctx.guild).max_uses.set(uses)
        await ctx.tick()
        return

    @nviteset.command(name="temporary")
    @commands.guild_only()
    async def nviteset_temporary(self, ctx, is_temporary: bool):
        """Sets the if the created invite should be a temporary invite"""
        await self.config.guild(ctx.guild).temporary.set(is_temporary)
        await ctx.tick()
        return
