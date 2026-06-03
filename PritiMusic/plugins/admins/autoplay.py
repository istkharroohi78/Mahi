from pyrogram import filters
from pyrogram.types import Message

# PritiMusic ke zaroori modules import karein
from PritiMusic import app
from PritiMusic.utils.database.autoplay import is_autoplay_group, add_autoplay_group, remove_autoplay_group
from PritiMusic.utils.decorators import AdminRightsCheck
from config import BANNED_USERS  

@app.on_message(
    filters.command(["autoplay"]) 
    & filters.group 
    & ~BANNED_USERS
)
@AdminRightsCheck
async def autoplay_mode(client, message: Message, _, chat_id):
    # Database se check karein ki group me autoplay ON hai ya OFF
    state = await is_autoplay_group(chat_id)
    
    if state:
        # Agar ON hai, toh OFF kar dein
        await remove_autoplay_group(chat_id)
        return await message.reply_text(
            "**Autoplay Disabled 🔴**\n\nAb queue khatam hone ke baad naye gaane automatically play nahi honge."
        )
    else:
        # Agar OFF hai, toh ON kar dein
        await add_autoplay_group(chat_id)
        return await message.reply_text(
            "**Autoplay Enabled 🟢**\n\nAb queue khali hone par YouTube se related gaane automatically chalenge."
        )
