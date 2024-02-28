import asyncio
from VIPMUSIC.misc import SUDOERS
from VIPMUSIC.core.userbot import Userbot
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from VIPMUSIC import app
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from VIPMUSIC import app
from VIPMUSIC.utils.vip_ban import admin_filter
from VIPMUSIC.utils.decorators.userbotjoin import UserbotWrapper
from VIPMUSIC.utils.database import get_assistant, is_active_chat
links = {}


@app.on_message(filters.group & filters.command(["userbotjoin", f"userbotjoin@{app.username}"]) & ~filters.private)
async def join_group(client, message):
    chat_id = message.chat.id
    userbot = await get_assistant(message.chat.id)
    
    # Get chat member object
    chat_member = await app.get_chat_member(chat_id, app.id)
    
    # Condition 1:- Group username is present, bot is not admin
    if message.chat.username and not chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        await userbot.join_chat(message.chat.username)
        return
    
    # Condition 2: Group username is present, bot is admin and Userbot is banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await message.reply("Assistant is unbanned")
                invite_link = await app.create_chat_invite_link(chat_id)
                await userbot.join_chat(invite_link.invite_link)
                await message.reply("Assistant was banned, now unbanned, and joined!")
            except Exception as e:
                await message.reply(str(e))
        return
    
    # Condition 3: Group username is not present/group is private, bot is not admin
    if not message.chat.username and not chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        await message.reply_text("I need Admin power to invite my Assistant")
        return
    
    # Condition 4: Group username is not present/group is private, bot is admin and Userbot is banned
    if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await message.reply("Assistant is unbanned")
                invite_link = await app.create_chat_invite_link(chat_id)
                await userbot.join_chat(invite_link.invite_link)
                await message.reply("Assistant was banned, now unbanned, and joined!")
            except Exception as e:
                await message.reply(str(e))
        return
    
    # Condition 5: Group username is not present/group is private, bot is admin
    if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            invite_link = await app.create_chat_invite_link(chat_id)
            await userbot.join_chat(invite_link.invite_link)
            await message.reply("Assistant joined via invite link")
        except Exception as e:
            await message.reply(str(e))
    
    # Condition 6: Group username is present, bot is admin, and Userbot is not banned
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status not in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
            await userbot.join_chat(message.chat.username)
            return

    # Condition 7: Group username is not present/private group, bot is admin
    if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        try:
            invite_link = await app.create_chat_invite_link(chat_id)
            await userbot.join_chat(invite_link.invite_link)
            await message.reply("Assistant joined via invite link")
        except Exception as e:
            await message.reply(str(e))
    
    # Condition 8: Group username is present, bot is not admin, and Userbot is banned
    if message.chat.username and not chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in [ChatMemberStatus.BANNED, ChatMemberStatus.RESTRICTED]:
            await message.reply_text("I need Admin power to unban invite my Assistant")
            return


    # Condition 1: Group username is not present/group is private, bot is admin and Userbot is banned but bot has no ban power
    if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in ["banned", "restricted"]:
            # Check if bot has ban power
            if not chat_member.can_restrict_members:
                await message.reply_text("I don't have ban power, please provide me")
                return
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await message.reply("Assistant is unbanned")
                invite_link = await app.create_chat_invite_link(chat_id)
                await userbot.join_chat(invite_link.invite_link)
                await message.reply("Assistant was banned, now unbanned, and joined!")
            except Exception as e:
                await message.reply(str(e))
        return
    
    # Condition 2: Group username is not present/group is private, bot is admin and Userbot is banned but bot has no invite user power
    if not message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in ["banned", "restricted"]:
            # Check if bot has invite user power
            if not chat_member.can_invite_users:
                await message.reply_text("I don't have invite user power, please provide me")
                return
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await message.reply("Assistant is unbanned")
                invite_link = await app.create_chat_invite_link(chat_id)
                await userbot.join_chat(invite_link.invite_link)
                await message.reply("Assistant was banned, now unbanned, and joined!")
            except Exception as e:
                await message.reply(str(e))
        return
    
    # Condition 3: Group username is present, bot is admin and Userbot is banned but bot has no invite user power
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in ["banned", "restricted"]:
            # Check if bot has invite user power
            if not chat_member.can_invite_users:
                await message.reply_text("I have no invite user power to invite assistant, please provide me")
                return
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await message.reply("Assistant is unbanned")
                invite_link = await app.create_chat_invite_link(chat_id)
                await userbot.join_chat(invite_link.invite_link)
                await message.reply("Assistant was banned, now unbanned, and joined!")
            except Exception as e:
                await message.reply(str(e))
        return
    
    # Condition 4: Group username is present, bot is admin and Userbot is banned but bot has no ban power
    if message.chat.username and chat_member.status == ChatMemberStatus.ADMINISTRATOR:
        userbot_member = await app.get_chat_member(chat_id, userbot.id)
        if userbot_member.status in ["banned", "restricted"]:
            # Check if bot has ban power
            if not chat_member.can_restrict_members:
                await message.reply_text("I have no ban power to unban assistant, please provide me")
                return
            try:
                await app.unban_chat_member(chat_id, userbot.id)
                await message.reply("Assistant is unbanned")
                invite_link = await app.create_chat_invite_link(chat_id)
                await userbot.join_chat(invite_link.invite_link)
                await message.reply("Assistant was banned, now unbanned, and joined!")
            except Exception as e:
                await message.reply(str(e))
        return
            



        
@app.on_message(filters.command("userbotleave") & filters.group & admin_filter)
async def leave_one(client, message):
    try:
        userbot = await get_assistant(message.chat.id)
        await userbot.leave_chat(message.chat.id)
        await app.send_message(message.chat.id, "✅ Userbot Successfully Left Chat")
    except Exception as e:
        print(e)


@app.on_message(filters.command(["leaveall", f"leaveall@{app.username}"]) & SUDOERS)
async def leave_all(client, message):
    if message.from_user.id not in SUDOERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **Userbot** Leaving All Chats !")
    try:
        userbot = await get_assistant(message.chat.id)
        async for dialog in userbot.one.get_dialogs():
            if dialog.chat.id == -1001733534088:
                continue
            try:
                await userbot.leave_chat(dialog.chat.id)
                left += 1
                await lol.edit(
                    f"Userbot leaving all group...\n\nLeft: {left} chats.\nFailed: {failed} chats."
                )
            except BaseException:
                failed += 1
                await lol.edit(
                    f"Userbot leaving...\n\nLeft: {left} chats.\nFailed: {failed} chats."
                )
            await asyncio.sleep(3)
    finally:
        await app.send_message(
            message.chat.id, f"✅ Left from: {left} chats.\n❌ Failed in: {failed} chats."
        )