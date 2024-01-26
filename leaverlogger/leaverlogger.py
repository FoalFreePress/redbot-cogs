# The MIT License (MIT)
#
# Copyright (c) 2023 shroomdog27
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
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
import time
from redbot.core import commands as Commands
from redbot.core import Config
from redbot.core.utils.chat_formatting import inline


class LeaverLoggerCog(Commands.Cog):
    """My custom cog"""

    def __init__(self):
        self.config = Config.get_conf(self, identifier=458459923910065184)

    async def get_channel(self, guild: discord.Guild) -> discord.TextChannel:
        txt_id = await self.config.guild(guild).channel()
        text_channel = guild.get_channel(txt_id)
        return text_channel

    async def set_channel(self, guild: discord.Guild, text_channel_id: int):
        await self.config.guild(guild).channel.set(text_channel_id)

    @Commands.group()
    @Commands.guild_only()
    async def leaverset(self, ctx):
        """Root command for Voice Chat Logger Commands"""
        pass

    @leaverset.command(name="channel")
    async def leaverset_channel(self, ctx, txt_channel: discord.TextChannel):
        """Sets the text channel to send messages to"""
        vc_id = txt_channel.id
        await self.set_channel(ctx.guild, vc_id)
        await ctx.tick()
        return

    @Commands.Cog.listener("on_raw_member_remove")
    async def on_raw_member_remove(self, payload: discord.RawMemberRemoveEvent) -> None:
        member = payload.user  # discord.member.Member
        guild = member.guild

        if guild.id != payload.guild_id:
            return

        if member.bot:
            return

        await self.send_message(
            (await self.get_channel(guild)),
            "⬅️",
            "<t:" + str(int(time.time())) + ":f>",
            "**" + str(member) + "**",
            "has left the server.",
        )
        return

    @Commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: discord.Member) -> None:
        guild = member.guild

        if member.bot:
            return

        await self.send_message(
            (await self.get_channel(guild)),
            "➡️",
            "<t:" + str(int(time.time())) + ":f>",
            "**" + str(member) + "**",
            "has joined the server.",
        )
        return

    async def send_message(self, s_channel, v_emoji, v_time, v_user, v_action) -> None:
        msg = "{emoji} {t_time} {user} {action}".format(emoji=v_emoji, t_time=v_time, user=v_user, action=v_action)
        await s_channel.send(msg, allowed_mentions=discord.AllowedMentions.none())
        return
