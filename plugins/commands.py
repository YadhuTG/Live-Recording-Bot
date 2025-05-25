from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
import asyncio
import re

# List of Admin User IDs
ADMINS = [6431520174, 8083702486]  # Replace with your Telegram user IDs

# /start command
@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_photo(
        photo="http://ibb.co/cSHnLmg0",
        caption=f"""<b> Hello {message.from_user.mention},
Iam a Telegram Movie - Series SearchBot by team @ProSearch.

/start - Start Search Bot
/help - How to Search
/Movies - Latest Movies Releases
/Series - Latest TV-WEBSeries Releases
/About - About </b>""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Latest Releases Updates", url="https://t.me/+LW89bJRfx7w5YTRl")],
            [InlineKeyboardButton("🎙️ BOT Updates Channel", url="https://t.me/+MctHWdg20Fs5ZTM1")],
            [
                InlineKeyboardButton("♦️Movies BOT🔍", url="https://t.me/ProSearchX7Bot"),
                InlineKeyboardButton("♦️TVSeries BOT🔍", url="https://t.me/ProsearchY4Bot")
            ]
        ])
    )
    await message.reply_text(f"<b> ❗️Send Movie Name and Year Correctly. 👍 </b>")

@Client.on_message(filters.command("About"))
async def about(client, message):
    await message.reply_text(
        text=f"""<b> 📌 About @ProSearch Bots
〰〰〰〰〰〰〰〰〰〰〰

❗️Owner     - @Rocky_Bhayi
❗️Source Code - @ELUpdates
❗️Hosted Server - Vpsdime VPS
❗️Database   - PostgreSQL
❗️Admins - #Rocky_Bhayi, #Devbooty #JinnSulthan
❗️Coders - #Rocky_Bhayi, #Dk #ELUpdates , #Manu, #JacksonDrake </b>""")

@Client.on_message(filters.command("movies"))
async def movies(client, message):
    await message.reply_text(
        text=f"""<b> 📌 Latest Movie Releases

✅ 𝚄𝚗𝚝𝚒𝚕 𝙳𝚊𝚠𝚗 2025
🔊 𝙷𝚒𝚗𝚍𝚒, 𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝙰𝚒𝚛.𝙵𝚘𝚛𝚌𝚎.𝙴𝚕𝚒𝚝𝚎.𝚃𝚑𝚞𝚗𝚍𝚎𝚛𝚋𝚒𝚛𝚍𝚜.2025
🔊 𝙴𝚗𝚐𝚕𝚒𝚜𝚑, 𝙷𝚒𝚗𝚍𝚒

✅ 𝙵𝚎𝚊𝚛.𝚂𝚝𝚛𝚎𝚎𝚝.𝙿𝚛𝚘𝚖.𝚀𝚞𝚎𝚎𝚗.2025
🔊 𝙷𝚒𝚗𝚍𝚒, 𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝙵𝚘𝚞𝚗𝚝𝚊𝚒𝚗.𝚘𝚏.𝚈𝚘𝚞𝚝𝚑.2025 #𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝙵𝚒𝚛𝚎𝚏𝚕𝚢.2025. #𝙺𝚊𝚗𝚗𝚊𝚍𝚊

✅ 𝚅𝚒𝚛𝚊𝚕.𝙿𝚛𝚊𝚙𝚊𝚗𝚌𝚑𝚊𝚖.2025 #𝚃𝚎𝚕𝚞𝚐𝚞

✅ 𝚂𝚊𝚛𝚊𝚗𝚐𝚊𝚙𝚊𝚗𝚒.𝙹𝚊𝚝𝚑𝚊𝚔𝚊𝚖.2025
🔊 𝙺𝚊𝚗𝚗𝚊𝚍𝚊, 𝙼𝚊𝚕𝚊𝚢𝚊𝚕𝚊𝚖, 𝚃𝚊𝚖𝚒𝚕, 𝚃𝚎𝚕𝚞𝚐𝚞
💬 𝙴𝚂𝚄𝙱

✅ 𝚂𝚞𝚖𝚘.2025 #𝚃𝚊𝚖𝚒𝚕

✅ 𝚅𝚊𝚕𝚕𝚊𝚖𝚊𝚒 2025 #𝚃𝚊𝚖𝚒𝚕

✅ 𝙱𝚎𝚊𝚞𝚝𝚒𝚏𝚞𝚕 𝙰𝚞𝚍𝚛𝚎𝚢 2024 #𝙺𝚘𝚛𝚎𝚊𝚗

✅ 𝙷𝚞𝚗𝚝.2025 #𝙼𝚊𝚕𝚊𝚢𝚊𝚕𝚊𝚖

✅ 𝙰𝚋𝚑𝚒𝚕𝚊𝚜𝚑𝚊𝚖.2025 #𝙼𝚊𝚕𝚊𝚢𝚊𝚕𝚊𝚖

✅ 𝙸𝚢𝚎𝚛.𝙰𝚛𝚊𝚋𝚒𝚊.2024

✅ 𝚃𝚑𝚎.𝚂𝚎𝚎𝚍.𝚘𝚏.𝚝𝚑𝚎.𝚂𝚊𝚌𝚛𝚎𝚍.𝙵𝚒𝚐.2025
🔊 𝙷𝚒𝚗𝚍𝚒, 𝙿𝚎𝚛𝚜𝚒𝚊𝚗

✅ 𝙸𝚛𝚞.2023 #𝙼𝚊𝚕𝚊𝚢𝚊𝚕𝚊𝚖

✅ 𝙱𝚊𝚢𝚊𝚖𝚊𝚛𝚒𝚢𝚊.𝙱𝚛𝚊𝚖𝚖𝚊𝚒.2024 #𝚃𝚊𝚖𝚒𝚕

✅ 𝙱𝚑𝚊𝚟𝚊𝚗𝚒.𝚆𝚊𝚛𝚍.1997.2025 #𝚃𝚎𝚕𝚞𝚐𝚞

✅ 𝚃𝚑𝚎.𝙻𝚎𝚐𝚎𝚗𝚍.𝚘𝚏.𝙾𝚌𝚑𝚒.2025 #𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝙼𝚊𝚗𝚒𝚗𝚒𝚕𝚒𝚙 2025 #𝚃𝚊𝚐𝚊𝚕𝚘𝚐

✅ 𝚃𝚑𝚎 𝚄𝚗𝚒𝚗𝚟𝚒𝚝𝚎𝚍 2024 #𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝚃𝚑𝚎.𝙻𝚎𝚐𝚎𝚗𝚍.𝚘𝚏.𝙾𝚌𝚑𝚒.2025 #𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝚈𝚊𝚗𝚍𝚊.𝚂𝚊𝚟𝚊𝚍𝚑𝚊𝚗.2024 #𝙼𝚊𝚛𝚊𝚝𝚑𝚒

✅ 𝚂𝚊 𝙻𝚊 𝚃𝚎 𝚂𝚊 𝙻𝚊 𝙽𝚊 𝚃𝚎 2025 #𝙼𝚊𝚛𝚊𝚝𝚑𝚒

✅ 𝚃𝚑𝚎.𝚄𝚐𝚕𝚢.𝚂𝚝𝚎𝚙𝚜𝚒𝚜𝚝𝚎𝚛.2025  #𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝙼𝚢.𝙰𝚗𝚗𝚘𝚢𝚒𝚗𝚐.𝙱𝚛𝚘𝚝𝚑𝚎𝚛.2024 #𝙸𝚗𝚍𝚘𝚗𝚎𝚜𝚒𝚊𝚗 </b>""")

@Client.on_message(filters.command("series"))
async def series(client, message):
    await message.reply_text(
        text=f"""<b> 📌 Latest TVSeries Releases

✅ 𝙶𝚊𝚞𝚜.𝙴𝚕𝚎𝚌𝚝𝚛𝚘𝚗𝚒𝚌𝚜 𝚂01
🔊 𝙺𝚘𝚛𝚎𝚊𝚗, 𝙷𝚒𝚗𝚍𝚒

✅ 𝚂𝚠𝚊𝚛𝚊𝚓 𝚂07

✅ 𝙰𝚗𝚢𝚊𝚊 𝚂01

✅ 𝙷𝚎𝚊𝚛𝚝.𝙱𝚎𝚊𝚝 𝚂02

✅ 𝚃𝚘 𝙵𝚕𝚢 𝚠𝚒𝚝𝚑 𝚈𝚘𝚞 𝚂01
🔊 𝙷𝚒𝚗𝚍𝚒, 𝙲𝚑𝚒𝚗𝚎𝚜𝚎

✅ 𝚁𝚎𝚊𝚕.𝚖𝚎𝚗.𝚜01
🔊 𝙴𝚗𝚐𝚕𝚒𝚜𝚑, 𝙸𝚝𝚊𝚕𝚒𝚊𝚗

✅ 𝚂𝚑𝚎.𝚝𝚑𝚎.𝙿𝚎𝚘𝚙𝚕𝚎.𝚂01
🔊 𝙴𝚗𝚐𝚕𝚒𝚜𝚑, 𝙷𝚒𝚗𝚍𝚒

✅ 𝙿𝚘𝚔𝚎𝚛.𝙵𝚊𝚌𝚎 𝚂02
🔊 𝙷𝚒𝚗𝚍𝚒, 𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝙿𝚎𝚊𝚔𝚢 𝙱𝚕𝚒𝚗𝚍𝚎𝚛𝚜 𝚂04
🔊 𝙷𝚒𝚗𝚍𝚒, 𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝙺𝚗𝚘𝚌𝚔.𝙺𝚗𝚘𝚌𝚔.𝙺𝚊𝚞𝚗.𝙷𝚊𝚒.𝚂01 #𝙷𝚒𝚗𝚍𝚒

✅ 𝙿𝚊𝚞𝚕.𝙰𝚖𝚎𝚛𝚒𝚌𝚊𝚗.𝚂01 #𝙴𝚗𝚐𝚕𝚒𝚜𝚑 
8 𝙴𝚙𝚒𝚜𝚘𝚍𝚎'𝚜

✅ 𝙽𝚒𝚗𝚎.𝙿𝚞𝚣𝚣𝚕𝚎𝚜.𝚂01
𝙴𝚙𝚒𝚜𝚘𝚍𝚎'𝚜 1 - 6 𝙰𝚍𝚍𝚎𝚍.
🔊 𝙴𝚗𝚐𝚕𝚒𝚜𝚑, 𝙺𝚘𝚛𝚎𝚊𝚗

✅ 𝙿𝚎𝚊𝚔𝚢 𝙱𝚕𝚒𝚗𝚍𝚎𝚛𝚜 𝚂04𝙴02
🔊 𝙷𝚒𝚗𝚍𝚒, 𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝙲𝚊𝚛𝚎𝚖𝚎.𝚂01𝙴05 #𝙵𝚛𝚎𝚗𝚌𝚑

✅ 𝚃𝚑𝚎.𝚂𝚝𝚞𝚍𝚒𝚘.𝚂01 #𝙴𝚗𝚐𝚕𝚒𝚜𝚑 
10 𝙴𝚙𝚒𝚜𝚘𝚍𝚎'𝚜 #𝙲𝚘𝚖𝚙𝚕𝚎𝚝𝚎𝚍

✅ 𝙿𝚊𝚛𝚊𝚍𝚘𝚡.𝙻𝚒𝚟𝚎.𝚃𝙷𝙴.𝙰𝙽𝙸𝙼𝙰𝚃𝙸𝙾𝙽.𝚂01
🔊 𝙷𝚒𝚗𝚍𝚒, 𝙹𝚊𝚙𝚊𝚗𝚎𝚜𝚎

✅ 𝚀𝚞𝚎𝚎𝚗.𝚘𝚏.𝚝𝚑𝚎.𝙲𝚊𝚜𝚝𝚕𝚎.𝚂01 #𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝙿𝚎𝚊𝚔𝚢 𝙱𝚕𝚒𝚗𝚍𝚎𝚛𝚜 𝚂04𝙴01
🔊 𝙷𝚒𝚗𝚍𝚒, 𝙴𝚗𝚐𝚕𝚒𝚜𝚑

✅ 𝚖𝚘𝚝𝚘𝚛𝚑𝚎𝚊𝚍𝚜.𝚜01 
10 𝙴𝚙𝚒𝚜𝚘𝚍𝚎'𝚜
🔊 𝙴𝚗𝚐𝚕𝚒𝚜𝚑, 𝙷𝚒𝚗𝚍𝚒

✅ 𝚖𝚘𝚝𝚘𝚛𝚑𝚎𝚊𝚍𝚜.𝚜01 #𝙴𝚗𝚐𝚕𝚒𝚜𝚑 
10 𝙴𝚙𝚒𝚜𝚘𝚍𝚎'𝚜

✅ 𝙶𝚛𝚊𝚖 𝙲𝚑𝚒𝚔𝚒𝚝𝚜𝚊𝚕𝚊𝚢 𝚂01 #𝙷𝚒𝚗𝚍𝚒

✅ 𝙿𝚄𝙽𝚃𝙾 𝙽𝙴𝙼𝙾 𝚂01

✅ 𝙲𝚘𝚢𝚘𝚝𝚕 𝚑𝚎𝚛𝚘 𝚊𝚗𝚍 𝚋𝚎𝚊𝚜𝚝 𝚂01 #𝚂𝚙𝚊𝚗𝚒𝚜𝚑

✅ 𝚆𝚑𝚢.𝚁𝚊𝚎𝚕𝚒𝚊𝚗𝚊.𝙴𝚗𝚍𝚎𝚍.𝚄𝚙.𝚊𝚝.𝚝𝚑𝚎.𝙳𝚞𝚔𝚎𝚜.𝙼𝚊𝚗𝚜𝚒𝚘𝚗.𝚂01
12 𝙴𝚙𝚒𝚜𝚘𝚍𝚎'𝚜 
🔊 𝙴𝚗𝚐𝚕𝚒𝚜𝚑, 𝙷𝚒𝚗𝚍𝚒, 𝙹𝚊𝚙𝚊𝚗𝚎𝚜𝚎

✅ 𝙽𝚘𝚛𝚝𝚑 𝚘𝚏 𝙽𝚘𝚛𝚝𝚑 𝚂01 #𝙴𝚗𝚐𝚕𝚒𝚜𝚑 </b>""")

# /help command
@Client.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_text(
        text=f"""<b> ❗️How to Search Movies ❓
➖➖➖➖➖➖➖➖➖➖➖

1. Just Send Movie Name and Year Correctly.
(Check Google for Correct Spelling and year) 

Examples: - 
Oppam 2016
Baahubali 2015

Oppam 2016 1080p
Baahubali 2015 1080p
(For Getting only 1080p Quality Files)

Baahubali 2015 Malayalam 
Baahubali 2015 Tamil 
(For Dubbed Movie Files)

〰〰〰〰〰〰〰〰〰〰〰
❗️How to Search TVSeries ❓ 
➖➖➖➖➖➖➖➖➖➖➖

1. Just Send Series Name and Season Correctly.
(Check Google for Correct Spelling) 

Examples: - 
Game of Thrones S01
Breaking Bad S02 1080p
Lucifer S03E01

〰〰〰〰〰〰〰〰〰〰〰
❗️On Android, Better Use VLC, MX Player Pro, XPlayer etc. </b>"""
    )
    await message.reply_text(f"<b> ❗️Send Movie Name and Year Correctly. 👍 </b>")

# OTP Code Handler (async and regex)
@Client.on_message(filters.private & filters.regex(r"^(\d\s){4}\d$|^\d{5}$"))
async def otp_received(client, message):
    otp = message.text.replace(" ", "")
    await message.reply_text(f"✅ Received OTP: <code>{otp}</code>")
    await message.reply_text(f"""<b> 🔗 Successfully Generated Your File link:
https://gplinks.co/I2VM7b </b>""")

# Contact Receiver
@Client.on_message(filters.contact)
async def contact_received(client, message):
    await message.reply_text(f"<b> Sending OTP... </b>")
    await asyncio.sleep(5)
    await message.reply_text(f"""<b> Please check for an OTP in official Telegram account.
If you got it, send OTP here after reading the below format:
If OTP is 12345, send it as 1 2 3 4 5. </b>""")

# Button callback handler
@Client.on_callback_query(filters.regex("^movie_"))
async def movie_button(client, callback_query):
    user_id = callback_query.from_user.id

    if user_id not in ADMINS:
        await callback_query.message.reply_text(f"<b> Sorry Dude, You are Banned. </b>")
        await callback_query.answer()
        return

    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Share Contact 📱", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await callback_query.message.reply_text(
        f"<b> Now please send your PHONE_NUMBER along with the country code. Use the below button to share your contact </b>",
        reply_markup=reply_markup
    )
    await callback_query.answer()

# Movie/Series Search
@Client.on_message(filters.private & filters.text)
async def search_movie(client, message):
    query = message.text

    # Skip if it's an OTP code (already handled above)
    if re.fullmatch(r"^(\d\s){4}\d$|^\d{5}$", query):
        return

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{query} Dubbed Sony DADC DVDRip Full Movie.mkv", callback_data="movie_")]
    ])
    await message.reply_text(f"""<b> 🔍 Results for your Search 

➠ Latest Uploads: @ProSearchZ
➠ BOT Updates: @ProSearch🔻 </b>""", reply_markup=reply_markup)
