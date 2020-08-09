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
from redbot.core import commands as Commands
from redbot.core import checks as Checks
from redbot.core import Config


class PrivateChannelCog(Commands.Cog):
    """Private Channel Cog"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=6667973120496550387)
        default_guild = {"channel": 0}
        self.config.register_guild(**default_guild)
        self.config.init_custom

    @Commands.group()
    @Commands.guild_only()
    async def personalchannel(self, ctx):
        """Root command for Private Channel Commands"""
        pass

    @personalchannel.command(name="create")
    async def pc_create(self, ctx, target_member: discord.Member):
        """Creates a personal channel that sets it so only the Member can read messages.
        Intended to be used with people who have the 'Administrator' permission node."""
        afterCategory = ctx.guild.get_channel((await self.config.guild(ctx.guild).channel()))
        if afterCategory is None:
            raise TypeError("Channel is null.")
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            target_member: discord.PermissionOverwrite(view_channel=True),
        }
        newCategory = await ctx.guild.create_category_channel(
            target_member.name, overwrites=overwrites, reason=f"Requested by {ctx.author.name}",
        )
        await newCategory.edit(position=afterCategory.position + 1)
        await ctx.guild.create_text_channel("general", category=newCategory, reason=f"Requested by {ctx.author.name}")
        await ctx.tick()
        return

    @personalchannel.command(name="channel")
    @Checks.admin_or_permissions(manage_channels=True)
    async def pc_channel(self, ctx, target_channel: discord.CategoryChannel):
        """Sets the channel to create new channels below."""
        id = target_channel.id
        await self.config.guild(ctx.guild).channel.set(id)
        await ctx.tick()
        return
