import random
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from PritiMusic import app
from PritiMusic.core.call import Lucky
from PritiMusic.utils.database import music_off
from config import BANNED_USERS

# ✅ Kurigram Button Style Import
from button import ButtonStyle

# ✅ IMPORT NEW ADMIN CHECKER
from PritiMusic.cplugin.utils.decorators.admins import AdminRightsCheck

# ==========================================
# 🔥 PREMIUM EMOJIS & SMART BUTTON HELPER
# ==========================================
PREMIUM_EMOJIS = [
    "5422831825178206894", 
    "5368324170673489600",
    "5206607081334906820",
    "5206380668048496464"
]

def action_btn(text, callback_data=None, url=None, style=ButtonStyle.PRIMARY, use_emoji=False):
    kwargs = {"text": text, "style": style}
    if callback_data: 
        kwargs["callback_data"] = callback_data
    if url: 
        kwargs["url"] = url
    if use_emoji: 
        kwargs["icon_custom_emoji_id"] = random.choice(PREMIUM_EMOJIS)
    return InlineKeyboardButton(**kwargs)

# ==========================================
# 🛑 PAUSE COMMAND EXECUTION
# ==========================================

@Client.on_message(filters.command(["pause", "cpause"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck 
async def pause_admin(cli, message: Message, _, chat_id):
    
    # 1. Database mein music off mark karein
    await music_off(chat_id)
    
    # 2. Call module ka use karke stream pause karein
    await Lucky.pause_stream(chat_id)

    # 3. Inline Buttons setup with Kurigram Styles
    buttons = [
        [
            action_btn("ʀᴇsᴜᴍᴇ ▷", callback_data=f"ADMIN Resume|{chat_id}", style=ButtonStyle.SUCCESS),
            action_btn("ʀᴇᴘʟᴀʏ ↺", callback_data=f"ADMIN Replay|{chat_id}", style=ButtonStyle.PRIMARY),
        ],
        [ 
            action_btn("✯ CLONE NOW ✯", url="https://t.me/clone_MUSICrobot", style=ButtonStyle.PRIMARY, use_emoji=True)
        ],
    ]

    # 4. Reply message
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
