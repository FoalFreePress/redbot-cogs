# Personal Roles - Adds automated personal roles to discord
# Copyright (C) 2023 brandons209
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#######################################
# This file is forked from brandons209's PersonalRoles cog.
# Original Source can be found at:
# https://github.com/brandons209/Red-bot-Cogs/tree/66bf686eec363a729c3dc21e979903b56bd05312/personalroles
#######################################
from .personalroles import PersonalRoles

__red_end_user_data_statement__ = "This will store what a user's custom role is if they have one."


async def setup(bot):
    await bot.add_cog(PersonalRoles(bot))
