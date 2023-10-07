import asyncio, re, ast, math, logging, pyrogram
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
from utils import get_shortlink 
from info import AUTH_USERS, PM_IMDB, SINGLE_BUTTON, PROTECT_CONTENT, SPELL_CHECK_REPLY, IMDB_TEMPLATE, IMDB_DELET_TIME, PMFILTER, G_FILTER, SHORT_URL, SHORT_API
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums 
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from plugins.group_filter import global_filters
from fuzzywuzzy import fuzz

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Client.on_message(filters.private & filters.text & filters.chat(AUTH_USERS) if AUTH_USERS else filters.text & filters.private)
async def auto_pm_fill(b, m):
    if PMFILTER:       
        if G_FILTER:
            kd = await global_filters(b, m)
            if kd == False: await pm_AutoFilter(b, m)
        else: await pm_AutoFilter(b, m)
    else: return 


async def pm_AutoFilter(client, msg, pmspoll=False):    
    if not pmspoll:
        message = msg 
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text): return
        if 0 < len(message.text) < 100:
            search = message.text
            return await pm_spoll_choker(msg)              
        else: return 

async def pm_spoll_choker(msg):
    vid = msg.chat.id
    await msg.reply("ദയവായി ഗ്രൂപ്പ് വഴി സെർച്ച് ചെയ്യുക.\n\n@pschelpergroup\n\n{vid}")
