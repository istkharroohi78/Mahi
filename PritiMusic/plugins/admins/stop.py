from pyrogram import filters
from pyrogram.types import Message

from PritiMusic import app
from PritiMusic.core.call import Lucky
from PritiMusic.misc import db
from PritiMusic.utils.database import set_loop
from PritiMusic.utils.decorators import AdminRightsCheck
from PritiMusic.utils.inline import close_markup
from config import BANNED_USERS

@app.on_message(
    filters.command(
        ["end", "stop", "cend", "cstop"], 
        # 🟢 THE FIX: Removed the empty string "" to prevent random triggers
        prefixes=["/", "!", "#"]
    ) 
    & filters.group 
    & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if len(message.command) != 1:
        return
        
    # Stream Stop Karega
    await Lucky.stop_stream(chat_id)
    
    # Loop Reset Karega
    await set_loop(chat_id, 0)
    
    # 🟢 THE FIX: Queue Empty Karega (Safety ke liye)
    try:
        db[chat_id] = []
    except:
        pass
        
    await message.reply_text(
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
    )
