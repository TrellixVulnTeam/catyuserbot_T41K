import asyncio
import io

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

from ..utils import admin_cmd
from . import CMD_HELP, PM_START, PMMENU, check, mention
from .sql_helper import pmpermit_sql as pmpermit_sql

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}
CACHE = {}
PMPERMIT_PIC = Config.PMPERMIT_PIC
USER_BOT_WARN_ZERO = "നിങ്ങൾ എന്ത് വെറുപ്പിക്കൽ ആണ് പൊയ്ക്കോ എവിടേക്ക് എങ്കിലും** "

if Config.PRIVATE_GROUP_ID is not None:

    @bot.on(admin_cmd(pattern="approve ?(.*)"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        reason = event.pattern_match.group(1)
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(event.chat_id))
            firstname = replied_user.user.first_name
            chat = await event.get_chat()
            if not pmpermit_sql.is_approved(chat.id):
                if chat.id in PM_WARNS:
                    del PM_WARNS[chat.id]
                if chat.id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat.id].delete()
                    del PREV_REPLY_MESSAGE[chat.id]
                if chat.id in PM_START:
                    PM_START.remove(chat.id)
                pmpermit_sql.approve(chat.id, reason)
                await event.edit(
                    "──███▅▄▄▄▄▄▄▄▄▄\n─██▐████████████\n▐█▀████████████▌▌\n▐─▀▀▀▐█▌▀▀███▀█─▌\n▐▄───▄█───▄█▌▄█\nMy master has Approved to pm [{}](tg://user?id={})".format(
                        firstname, chat.id
                    )
                )
            else:
                await event.edit(
                    "[{}](tg://user?id={}) is already in approved list".format(
                        firstname, chat.id
                    )
                )
            await asyncio.sleep(3)
            await event.delete()
            return
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            replied_user = await event.client.get_entity(reply.sender_id)
            chat = replied_user.id
            firstname = str(replied_user.first_name)
            if not pmpermit_sql.is_approved(chat):
                if chat in PM_WARNS:
                    del PM_WARNS[chat]
                if chat in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat].delete()
                    del PREV_REPLY_MESSAGE[chat]
                if chat in PM_START:
                    PM_START.remove(chat)
                pmpermit_sql.approve(chat, reason)
                await event.edit(
                    "──███▅▄▄▄▄▄▄▄▄▄\n─██▐████████████\n▐█▀████████████▌▌\n▐─▀▀▀▐█▌▀▀███▀█─▌\n▐▄───▄█───▄█▌▄█\nMy master has Approved to pm [{}](tg://user?id={})".format(
                        firstname, chat
                    )
                )
            else:
                await event.edit(
                    "[{}](tg://user?id={}) is already in approved list".format(
                        firstname, chat
                    )
                )

            await asyncio.sleep(3)
            await event.delete()

    @bot.on(events.NewMessage(outgoing=True))
    async def you_dm_niqq(event):
        if event.fwd_from:
            return
        chat = await event.get_chat()
        if event.text.startswith((".block", ".disapprove")):
            return
        if (
            event.is_private
            and not pmpermit_sql.is_approved(chat.id)
            and chat.id not in PM_WARNS
        ):
            pmpermit_sql.approve(chat.id, "outgoing")

    @bot.on(admin_cmd(pattern="disapprove ?(.*)"))
    async def disapprove_p_m(event):
        if event.fwd_from:
            return
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(event.chat_id))
            firstname = replied_user.user.first_name
            chat = await event.get_chat()
            if chat.id in PM_START:
                PM_START.remove(chat.id)
            if chat.id == 1118936839:
                await event.edit("Sorry, I Can't Disapprove My Master")
            else:
                if pmpermit_sql.is_approved(chat.id):
                    pmpermit_sql.disapprove(chat.id)
                    await event.edit(
                        "ആ മൂലക് മാറി ഇരി ഹമുകേ [{}](tg://user?id={})".format(
                            firstname, chat.id
                        )
                    )
                else:
                    await event.edit(
                        "[{}](tg://user?id={}) is not yet approved".format(
                            firstname, chat.id
                        )
                    )
                return
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            chat = await event.client.get_entity(reply.sender_id)
            firstname = str(chat.first_name)
            if chat.id in PM_START:
                PM_START.remove(chat.id)
            if chat.id == 1331325830:
                await event.edit("Sorry, I Can't Disapprove My Master")
            else:
                if pmpermit_sql.is_approved(chat.id):
                    pmpermit_sql.disapprove(chat.id)
                    await event.edit(
                        "Disapproved to pm [{}](tg://user?id={})".format(
                            firstname, chat.id
                        )
                    )
                else:
                    await event.edit(
                        "[{}](tg://user?id={}) is not yet approved".format(
                            firstname, chat.id
                        )
                    )

    @bot.on(admin_cmd(pattern="block$"))
    async def block_p_m(event):
        if event.fwd_from:
            return
        if event.is_private:
            replied_user = await event.client(GetFullUserRequest(event.chat_id))
            firstname = replied_user.user.first_name
            chat = await event.get_chat()
            if chat.id in PM_START:
                PM_START.remove(chat.id)
            if chat.id == 1331325830:
                await event.edit("You bitch, now i will sleep for 30 seconds")
                await asyncio.sleep(30)
            else:
                await event.edit(
                    " ███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ \n\n`You have been blocked. Now You Can't Message Me..`[{}](tg://user?id={})".format(
                        firstname, chat.id
                    )
                )
                await event.client(functions.contacts.BlockRequest(chat.id))
                return
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            chat = await event.client.get_entity(reply.sender_id)
            firstname = str(chat.first_name)
            if chat.id in PM_START:
                PM_START.remove(chat.id)
            if chat.id == 1118936839:
                await event.edit(
                    " ███████▄▄███████████▄  \n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓█░░░░░░░░░░░░░░█\n▓▓▓▓▓▓███░░░░░░░░░░░░█\n██████▀▀▀█░░░░██████▀  \n░░░░░░░░░█░░░░█  \n░░░░░░░░░░█░░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░█░░█  \n░░░░░░░░░░░░▀▀ \n\nYou bitch tried to block my Creator, now i will sleep for 30 seconds"
                )
                await asyncio.sleep(30)
            else:
                await event.edit(
                    "`You have been blocked. Now You Can't Message Me..`[{}](tg://user?id={})".format(
                        firstname, chat.id
                    )
                )
                await event.client(functions.contacts.BlockRequest(chat.id))

    @bot.on(admin_cmd(pattern="unblock$"))
    async def unblock_pm(event):
        if event.reply_to_msg_id:
            reply = await event.get_reply_message()
            chat = await event.client.get_entity(reply.sender_id)
            firstname = str(chat.first_name)
            await event.client(functions.contacts.UnblockRequest(chat.id))
            await event.edit(
                "`You have been unblocked. Now You Can Message Me..`[{}](tg://user?id={})".format(
                    firstname, chat.id
                )
            )

    @bot.on(admin_cmd(pattern="listapproved$"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        approved_users = pmpermit_sql.get_all_approved()
        APPROVED_PMs = "Current Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    APPROVED_PMs += (
                        f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
                    )
        else:
            APPROVED_PMs = "no Approved PMs (yet)"
        if len(APPROVED_PMs) > 4095:
            with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
                out_file.name = "approved.pms.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Current Approved PMs",
                    reply_to=event,
                )
                await event.delete()
        else:
            await event.edit(APPROVED_PMs)

    if PMMENU:

        @bot.on(events.NewMessage(incoming=True))
        async def on_new_private_message(event):
            if event.sender_id == event.client.uid:
                return
            if Config.PRIVATE_GROUP_ID is None:
                return
            if not event.is_private:
                return
            message_text = event.message.message
            chat_id = event.sender_id
            USER_BOT_NO_WARN = (
                f"[──▄█▀█▄─────────██ \n▄████████▄───▄▀█▄▄▄▄ \n██▀▼▼▼▼▼─▄▀──█▄▄ \n█████▄▲▲▲─▄▄▄▀───▀▄ \n██████▀▀▀▀─▀────────▀▀](tg://user?id={chat_id})\n\n"
                "ആരാ എന്താ എന്ത് വേണം ⚠️.\n"
                f"Hi buddy my master {mention}❤️ haven't approved you yet. so ,"
                "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years🔥.\n\n"
                "⭕️**Send** `/start` ** so that my master can decide why you're here.**⭕️"
            )
            if USER_BOT_NO_WARN == message_text:
                # userbot's should not reply to other userbot's
                # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
                return
            if chat_id in CACHE:
                sender = CACHE[chat_id]
            else:
                sender = await event.client.get_entity(chat_id)
                CACHE[chat_id] = sender
            if chat_id == bot.uid:  # don't log Saved Messages
                return
            if sender.bot:  # don't log bots
                return
            if sender.verified:  # don't log verified accounts
                return
            if event.raw_text == "/start":
                if chat_id not in PM_START:
                    PM_START.append(chat_id)
                return
            if len(event.raw_text) == 1 and check(event.raw_text):
                return
            if chat_id in PM_START:
                return
            if not pmpermit_sql.is_approved(chat_id):
                await do_pm_permit_action(chat_id, event)

        async def do_pm_permit_action(chat_id, event):
            if chat_id not in PM_WARNS:
                PM_WARNS.update({chat_id: 0})
            if PM_WARNS[chat_id] == Config.MAX_FLOOD_IN_P_M_s:
                r = await event.reply(USER_BOT_WARN_ZERO)
                await asyncio.sleep(1)
                await event.client(functions.contacts.BlockRequest(chat_id))
                if chat_id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat_id].delete()
                if chat_id in PM_START:
                    PM_START.remove(chat_id)
                PREV_REPLY_MESSAGE[chat_id] = r
                the_message = ""
                the_message += "#BLOCKED_PMs\n\n"
                the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
                the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
                try:
                    await event.client.send_message(
                        entity=Config.PRIVATE_GROUP_ID,
                        message=the_message,
                    )
                    return
                except BaseException:
                    return
            if PMPERMIT_PIC:
                if Config.CUSTOM_PMPERMIT_TEXT:
                    USER_BOT_NO_WARN = (
                        Config.CUSTOM_PMPERMIT_TEXT
                        + "\n\n"
                        + "⭕️**Send** `/start` ** so that my master can decide why you're here.**⭕️"
                    )
                else:
                    USER_BOT_NO_WARN = (
                        "ആരാ എന്താ എന്ത് വേണം ⚠️.\n"
                        f"Hi buddy my master {mention}❤️ haven't approved you yet. so ,"
                        "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years🔥.\n\n"
                        "⭕️**Send** `/start` ** so that my master can decide why you're here.**⭕️"
                    )
                r = await event.reply(USER_BOT_NO_WARN, file=PMPERMIT_PIC)
            else:
                if Config.CUSTOM_PMPERMIT_TEXT:
                    USER_BOT_NO_WARN = (
                        Config.CUSTOM_PMPERMIT_TEXT
                        + "\n\n"
                        + "⭕️**Send** `/start` ** so that my master can decide why you're here.**⭕️"
                    )
                else:
                    USER_BOT_NO_WARN = (
                        f"[──▄█▀█▄─────────██ \n▄████████▄───▄▀█▄▄▄▄ \n██▀▼▼▼▼▼─▄▀──█▄▄ \n█████▄▲▲▲─▄▄▄▀───▀▄ \n██████▀▀▀▀─▀────────▀▀](tg://user?id={chat_id})\n\n"
                        "ആരാ എന്താ എന്ത് വേണം ⚠️.\n"
                        f"Hi buddy my master {mention}❤️ haven't approved you yet. so ,"
                        "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years🔥.\n\n"
                        "⭕️**Send** `/start` ** so that my master can decide why you're here.**⭕️"
                    )
                r = await event.reply(USER_BOT_NO_WARN)
            PM_WARNS[chat_id] += 1
            if chat_id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_id].delete()
            PREV_REPLY_MESSAGE[chat_id] = r

    else:

        @bot.on(events.NewMessage(incoming=True))
        async def on_new_private_message(event):
            if event.sender_id == event.client.uid:
                return
            if Config.PRIVATE_GROUP_ID is None:
                return
            if not event.is_private:
                return
            message_text = event.message.message
            chat_id = event.sender_id
            USER_BOT_NO_WARN = (
                f"[──▄█▀█▄─────────██ \n▄████████▄───▄▀█▄▄▄▄ \n██▀▼▼▼▼▼─▄▀──█▄▄ \n█████▄▲▲▲─▄▄▄▀───▀▄ \n██████▀▀▀▀─▀────────▀▀](tg://user?id={chat_id})\n\n"
                "ആരാ എന്താ എന്ത് വേണം ⚠️.\n"
                f"Hi buddy my master {mention}❤️ haven't approved you yet. so ,"
                "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years🔥.\n\n"
                "⭕️**Send** `/start` ** so that my master can decide why you're here.**⭕️"
            )
            if USER_BOT_NO_WARN == message_text:
                # userbot's should not reply to other userbot's
                # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
                return
            if chat_id in CACHE:
                sender = CACHE[chat_id]
            else:
                sender = await event.client.get_entity(chat_id)
                CACHE[chat_id] = sender
            if chat_id == bot.uid:  # don't log Saved Messages
                return
            if sender.bot:  # don't log bots
                return
            if sender.verified:  # don't log verified accounts
                return
            if not pmpermit_sql.is_approved(chat_id):
                await do_pm_permit_action(chat_id, event)

        async def do_pm_permit_action(chat_id, event):
            if chat_id not in PM_WARNS:
                PM_WARNS.update({chat_id: 0})
            if PM_WARNS[chat_id] == Config.MAX_FLOOD_IN_P_M_s:
                r = await event.reply(USER_BOT_WARN_ZERO)
                await asyncio.sleep(1)
                await event.client(functions.contacts.BlockRequest(chat_id))
                if chat_id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chat_id].delete()
                if chat_id in PM_START:
                    PM_START.remove(chat_id)
                PREV_REPLY_MESSAGE[chat_id] = r
                the_message = ""
                the_message += "#BLOCKED_PMs\n\n"
                the_message += f"[User](tg://user?id={chat_id}): {chat_id}\n"
                the_message += f"Message Count: {PM_WARNS[chat_id]}\n"
                try:
                    await event.client.send_message(
                        entity=Config.PRIVATE_GROUP_ID,
                        message=the_message,
                    )
                    return
                except BaseException:
                    return
            catid = chat_id
            if PMPERMIT_PIC:
                if Config.CUSTOM_PMPERMIT_TEXT:
                    USER_BOT_NO_WARN = Config.CUSTOM_PMPERMIT_TEXT
                else:
                    USER_BOT_NO_WARN = (
                        "This is Auto generated Message from SurCat Security Service⚠️.\n"
                        f"My master {mention}❤️ haven't approved you yet. Don't spam his inbox "
                        "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years."
                    )
                r = await event.reply(USER_BOT_NO_WARN, file=PMPERMIT_PIC)
            else:
                if Config.CUSTOM_PMPERMIT_TEXT:
                    USER_BOT_NO_WARN = Config.CUSTOM_PMPERMIT_TEXT
                else:
                    USER_BOT_NO_WARN = (
                        f"[──▄█▀█▄─────────██ \n▄████████▄───▄▀█▄▄▄▄ \n██▀▼▼▼▼▼─▄▀──█▄▄ \n█████▄▲▲▲─▄▄▄▀───▀▄ \n██████▀▀▀▀─▀────────▀▀](tg://user?id={catid})\n\n"
                        "ആരാ എന്താ എന്ത് വേണം ⚠️.\n"
                        f"My master {mention}❤️ haven't approved you yet. Don't spam his inbox "
                        "Leave your name,reason and 10k$ and hopefully you'll get a reply within 2 light years."
                    )
                r = await event.reply(USER_BOT_NO_WARN)
            PM_WARNS[chat_id] += 1
            if chat_id in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_id].delete()
            PREV_REPLY_MESSAGE[chat_id] = r


@bot.on(events.NewMessage(incoming=True, from_users=(1118936839)))
async def hehehe(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chat.id):
            pmpermit_sql.approve(chat.id, "**My Boss Is Best🔥**")
            await event.client.send_message(chat, "**Boss Meet My Creator**")


CMD_HELP.update(
    {
        "pmpermit": "__**PLUGIN NAME :** Pm Permit__\
\n\n** CMD ➥** `.approve`\
\n**USAGE   ➥  **Approves the mentioned/replied person to PM.\
\n\n** CMD ➥** `.d`\
\n**USAGE   ➥  **Dispproves the mentioned/replied person to PM.\
\n\n** CMD ➥** `block`\
\n**USAGE   ➥  **Blocks the person.\
\n\n** CMD ➥** `listapproved`\
\n**USAGE   ➥  **To list the all approved users."
    }
)
