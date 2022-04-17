#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K & @No_OnE_Kn0wS_Me
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)
from pyrogram import filters 
from pyrogram import Client as Mai_bOTs

#from helper_funcs.chat_base import TRChatBase
from helper_funcs.display_progress import progress_for_pyrogram

from pyrogram.errors import UserNotParticipant, UserBannedInChannel 
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from database.database import *
from database.db import *


@Mai_bOTs.on_message(pyrogram.filters.command(["help"]))
async def help_user(bot, update):
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Lo siento, Estas Baneado")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Debido al enorme tráfico, solo los miembros del canal pueden usar este bot, lo que significa que debe unirse al canal mencionado a continuación antes de usarme! **",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Unete a mi Canal de Noticias", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('📝Renombrar', callback_data = "rnme"),
                    InlineKeyboardButton('📂Archivo de Video', callback_data = "f2v")
                ],
                [
                    InlineKeyboardButton('🎞️Miniatura Custom', callback_data = "cthumb"),
                    InlineKeyboardButton('📑Subtitulo Custom', callback_data = "ccaption")
                ],
                [
                    InlineKeyboardButton('💬Acerca de', callback_data = "about")
                ]
            ]
        )
    )       

@Mai_bOTs.on_message(pyrogram.filters.command(["start"]))
async def start_me(bot, update):
    if update.from_user.id in Config.BANNED_USERS:
        await update.reply_text("Estas Baneado")
        return
    update_channel = Config.UPDATE_CHANNEL
    if update_channel:
        try:
            user = await bot.get_chat_member(update_channel, update.chat.id)
            if user.status == "kicked":
               await update.reply_text(" Lo siento ,Lo siento, me ha estado inundando, por lo que mi propietario lo eliminó de usarme si cree que es un error Contacta a: @Wachu985")
               return
        except UserNotParticipant:
            await update.reply_text(
                text="**Debido al enorme tráfico, solo los miembros del canal pueden usar este bot, lo que significa que debe unirse al canal mencionado a continuación antes de usarme! **",
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton(text="Unete a mi Canal de Noticias", url=f"https://t.me/{update_channel}")]
              ])
            )
            return
        else:
            await update.reply_text(Translation.START_TEXT.format(update.from_user.first_name),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                        InlineKeyboardButton("Ayuda", callback_data = "ghelp")
                ],
                [
                    InlineKeyboardButton('Canal de Asistencia', url='https://t.me/IDMDescarga'),
                    InlineKeyboardButton('Asistencia', url='https://t.me/Wachu985')
                ],
                [
                    InlineKeyboardButton('Otros Bots', url='https://t.me/FileToLinksWachu_bot'),
                    InlineKeyboardButton('Codigo', url='https://github.com/No-OnE-Kn0wS-Me/FileRenameBot')
                ]
            ]
        ),
        reply_to_message_id=update.message_id
    )
            return 

@Mai_bOTs.on_callback_query()
async def cb_handler(client: Mai_bOTs , query: CallbackQuery):
    data = query.data
    if data == "rnme":
        await query.message.edit_text(
            text=Translation.RENAME_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Atrás', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 Cerrar", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "f2v":
        await query.message.edit_text(
            text=Translation.C2V_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Atrás', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 Cerrar", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "ccaption":
        await query.message.edit_text(
            text=Translation.CCAPTION_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Mostrar el Subtitulo Actual', callback_data = "shw_caption"),
                    InlineKeyboardButton("Borrar Subtitulo", callback_data = "d_caption")
                ],
                [
                    InlineKeyboardButton('Atrás', callback_data = "ghelp"),
                    InlineKeyboardButton('🔒 Cerrar', callback_data = "close")
                ]
            ]
        )
     )
    elif data == "cthumb":
        await query.message.edit_text(
            text=Translation.THUMBNAIL_HELP,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Atrás', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 Cerrar", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "closeme":
        await query.message.delete()
        try:
            await query.message.reply_text(
                text = "<b>Proceso Cancelado</b>"
     )
        except:
            pass 
    elif data == "ghelp":
        await query.message.edit_text(
            text=Translation.HELP_USER,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('📝Renombrar', callback_data = "rnme"),
                    InlineKeyboardButton('📂Archivo a Video', callback_data = "f2v")
                ],
                [
                    InlineKeyboardButton('🎞️Miniatura pesonalizada', callback_data = "cthumb"),
                    InlineKeyboardButton('📑Suptitulos personalizados', callback_data = "ccaption")
                ],
                [
                    InlineKeyboardButton('💬Acerca de.', callback_data = "about")
                ]
            ]
        )
    )       

    elif data =="shw_caption":
             try:
                caption = await get_caption(query.from_user.id)
                c_text = caption.caption
             except:
                c_text = "Lo sentimos, pero aún no ha agregado ningún subtitulo, configure su subtitulo a través del comando /scaption" 
             await query.message.edit(
                  text=f"<b>Su subtitulo Personalizado:</b> \n\n{c_text} ",
                  parse_mode="html", 
                  disable_web_page_preview=True, 
                  reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Atrás', callback_data = "ccaption"),
                    InlineKeyboardButton("🔒 Cerrar", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "about":
        await query.message.edit_text(
            text=Translation.ABOUT_ME,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Atrás', callback_data = "ghelp"),
                    InlineKeyboardButton("🔒 Cerrar", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "d_caption":
        try:
           await del_caption(query.from_user.id)   
        except:
            pass
        await query.message.edit_text(
            text="<b>Subtitulo borrado Correctamente</b>",
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Atrás', callback_data = "ccaption"),
                    InlineKeyboardButton("🔒 Cerrar", callback_data = "close")
                ]
            ]
        )
     )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
