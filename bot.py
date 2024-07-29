import discord
import asyncio
from spotify import get_current_track
import os
import logging

token = 'PASTE_TOKEN' # Paste your token here

CUSTOM_EMOJI_ID = '1267529433015648478'
CUSTOM_EMOJI_NAME = 'Spotify'
SPECIAL_SERVER_ID = '1179009716307886080'
FALLBACK_EMOJI = '🎵'
#FALLBACK_EMOJI = '🎶'

logging.basicConfig(level=logging.CRITICAL)

class SelfBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_track = None
        self.custom_emoji = None

    async def on_ready(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        await self.check_nitro_and_emoji()
        self.loop.create_task(self.update_status())

    async def check_nitro_and_emoji(self):
        try:
            if self.user.premium_type in [discord.PremiumType.nitro, discord.PremiumType.nitro_classic, discord.PremiumType.nitro_basic]:
                guild = discord.utils.get(self.guilds, id=int(SPECIAL_SERVER_ID))
                if guild:
                    emoji = discord.utils.get(guild.emojis, id=int(CUSTOM_EMOJI_ID))
                    if emoji:
                        self.custom_emoji = discord.PartialEmoji(name=emoji.name, id=emoji.id)
                        print(f'{self.user} has Nitro. | Emoji: {self.custom_emoji} | Server: {guild.name}')
                    else:
                        print("Custom emoji not found.")
                else:
                    print("Special server not found. Join to get spotify icon next to status: https://dsc.gg/cs2as")
            else:
                print(f'{self.user} does not have Nitro.')
        except Exception as e:
            print(f"Error checking Nitro status or emoji: {e}")

    async def update_status(self):
        await self.wait_until_ready()

        while not self.is_closed():
            track, artist, is_playing = get_current_track()
            if not is_playing and self.last_track:
                status_message = f"{self.last_track[1]} - {self.last_track[0]} (Paused)"
            elif is_playing and (track, artist) != self.last_track:
                status_message = f"{artist} - {track}"
                self.last_track = (track, artist)
            else:
                status_message = f"{artist} - {track}" if track and artist else "Nothing Playing"

            emoji = self.custom_emoji or discord.PartialEmoji(name=FALLBACK_EMOJI, id=None)
            try:
                await self.change_presence(activity=discord.CustomActivity(name=status_message, emoji=emoji))
                print(f"\rUpdated to: {status_message}", end="")
            except Exception as e:
                print(f"\rFailed to update status: {e}", end="")

            await asyncio.sleep(1)

client = SelfBot()
client.run(token)