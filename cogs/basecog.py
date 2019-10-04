"""
Info cog for qrm
---

Copyright (C) 2019  Abigail Gold, 0x5c

This file is part of discord-qrmbot.

discord-qrmbot is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import discord
import discord.ext.commands as commands

import os

class BaseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")

    @commands.command(name="info", aliases=["about"])
    async def _info(self, ctx):
        """Shows info about qrm."""
        embed = discord.Embed(title="About qrm", description=self.gs.info.description, colour=self.gs.colours.neutral)
        embed = embed.add_field(name="Authors", value=", ".join(self.gs.info.authors))
        embed = embed.add_field(name="Contributing", value=self.gs.info.contributing)
        embed = embed.add_field(name="License", value=self.gs.info.license)
        await ctx.send(embed=embed)

    @commands.command(name="restart")
    async def _restart_bot(self, ctx):
        """Restarts the bot."""
        if ctx.author.id in self.gs.opt.owners_uids:
            await ctx.message.add_reaction("✅")
            await self.bot.logout()
        else:
            try:
                await ctx.message.add_reaction("❌")
            except:
                return

    @commands.command(name="shutdown")
    async def _shutdown_bot(self, ctx):
        """Shuts down the bot."""
        if ctx.author.id in self.gs.opt.owners_uids:
            await ctx.message.add_reaction("✅")
            os._exit(42)
        else:
            try:
                await ctx.message.add_reaction("❌")
            except:
                return

def setup(bot):
    bot.add_cog(BaseCog(bot))
