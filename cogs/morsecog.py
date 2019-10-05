"""
Morse Code cog for qrm
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

import json

class MorseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gs = bot.get_cog("GlobalSettings")
        with open('resources/morse.json') as morse_file:
            self.ascii2morse = json.load(morse_file)
            self.morse2ascii = {v: k for k, v in self.ascii2morse.items()}

    @commands.command(name="morse", aliases=['cw'])
    async def _morse(self, ctx, *, msg : str):
        """Converts ASCII to international morse code."""
        with ctx.typing():
            result = ''
            for char in msg.upper():
                try:
                    result += self.ascii2morse[char]
                except:
                    result += '<?>'
                result += ' '
            embed = discord.Embed(title=f'Morse Code for {msg}', description=result,
                                  colour=self.gs.colours.good)
        await ctx.send(embed=embed)

    @commands.command(name="unmorse", aliases=['demorse', 'uncw', 'decw'])
    async def _unmorse(self, ctx, *, msg : str):
        '''Converts international morse code to ASCII.'''
        with ctx.typing():
            result = ''
            msg0 = msg
            msg = msg.split('/')
            msg = [m.split() for m in msg]
            for word in msg:
                for char in word:
                    try:
                        result += self.morse2ascii[char]
                    except:
                        result += '<?>'
                result += ' '
            embed = discord.Embed(title=f'ASCII for {msg0}', description=result,
                                  colour=self.gs.colours.good)
        await ctx.send(embed=embed)

    @commands.command(name="weight", aliases=["cwweight", 'cww'])
    async def _weight(self, ctx, msg : str):
        '''Calculates the CW Weight of a callsign.'''
        with ctx.typing():
            msg = msg.upper()
            weight = 0
            for char in msg:
                try:
                    cwChar = self.ascii2morse[char].replace('-', '==')
                    weight += len(cwChar) * 2 + 2
                except:
                    res = f'Unknown character {char} in callsign'
                    await ctx.send(res)
                    return
            res = f'The CW weight is **{weight}**'
            embed = discord.Embed(title=f'CW Weight of {msg}', description=res,
                                  colour=self.gs.colours.good)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MorseCog(bot))