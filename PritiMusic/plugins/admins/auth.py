from pyrogram import filters, Client
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus # 🟢 Zaroori Import

import config
from PritiMusic import app
from PritiMusic.utils import extract_user, int_to_alpha
from PritiMusic.utils.database import (
    delete_authuser,
    get_authuser,
    get_authuser_names,
    save_authuser,
)
from PritiMusic.utils.decorators import AdminActual, language
from PritiMusic.utils.inline import close_markup
from config import BANNED_USERS, adminlist


# 🟢 THE FIX 1: @app ko @Client se replace kiya + Prefixes lagaye
@Client.on_message(filters.command(["auth", "cauth"], prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def auth(client: Client, message: Message, _):
    
    # 🟢 THE FIX 2: BULLETPROOF ADMIN CHECK
    if message.from_user.id not in config.SUDOERS:
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await message.reply_text("❌ **Sirf Admins he is command ko use kar sakte hain!**")
        except Exception:
            return await message.reply_text("❌ **Error: Admin rights verify nahi ho paye.**")

    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
            
    user = await extract_user(message)
    
    # Int to alpha is usually synchronous, added a safe fallback just in case
    try:
        token = await int_to_alpha(user.id)
    except:
        token = int_to_alpha(user.id)
        
    _check = await get_authuser_names(message.chat.id)
    count = len(_check)
    
    if int(count) == 25:
        return await message.reply_text(_["auth_1"])
        
    if token not in _check:
        assis = {
            "auth_user_id": user.id,
            "auth_name": user.first_name,
            "admin_id": message.from_user.id,
            "admin_name": message.from_user.first_name,
        }
        
        get = adminlist.get(message.chat.id)
        if get is not None:
            if user.id not in get:
                get.append(user.id)
        else:
            adminlist[message.chat.id] = [user.id]
            
        await save_authuser(message.chat.id, token, assis)
        return await message.reply_text(_["auth_2"].format(user.mention))
    else:
        return await message.reply_text(_["auth_3"].format(user.mention))


@Client.on_message(filters.command(["unauth", "cunauth"], prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def unauthusers(client: Client, message: Message, _):
    
    # 🟢 THE FIX 2: BULLETPROOF ADMIN CHECK
    if message.from_user.id not in config.SUDOERS:
        try:
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await message.reply_text("❌ **Sirf Admins he is command ko use kar sakte hain!**")
        except Exception:
            return await message.reply_text("❌ **Error: Admin rights verify nahi ho paye.**")

    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
            
    user = await extract_user(message)
    try:
        token = await int_to_alpha(user.id)
    except:
        token = int_to_alpha(user.id)
        
    deleted = await delete_authuser(message.chat.id, token)
    
    get = adminlist.get(message.chat.id)
    if get:
        if user.id in get:
            get.remove(user.id)
            
    if deleted:
        return await message.reply_text(_["auth_4"].format(user.mention))
    else:
        return await message.reply_text(_["auth_5"].format(user.mention))

# Ze0
@Client.on_message(
    filters.command(["authlist", "authusers", "cauthlist"], prefixes=["/", "!", "%", ",", ".", "@", "#"]) & filters.group & ~BANNED_USERS
)
@language
async def authusers(client: Client, message: Message, _):
    _wtf = await get_authuser_names(message.chat.id)
    if not _wtf:
        return await message.reply_text(_["setting_4"])
    else:
        j = 0
        mystic = await message.reply_text(_["auth_6"])
        text = _["auth_7"].format(message.chat.title)
        for umm in _wtf:
            _umm = await get_authuser(message.chat.id, umm)
            user_id = _umm["auth_user_id"]
            admin_id = _umm["admin_id"]
            admin_name = _umm["admin_name"]
            try:
                # 🟢 THE FIX 3: app.get_users ko client.get_users banaya taaki Clones error na dein!
                user = (await client.get_users(user_id)).first_name
                j += 1
            except:
                continue
            text += f"{j}➤ {user}[<code>{user_id}</code>]\n"
            text += f"   {_['auth_8']} {admin_name}[<code>{admin_id}</code>]\n\n"
        await mystic.edit_text(text, reply_markup=close_markup(_))
