from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        text=f"""<b> Hey there {message.from_user.mention} 👋,

I'm Screenshot Generator Bot. I can provide screenshots or sample clips from your video files </b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("Source ♥️", url="https://github.com/odysseusmax/animated-lamp"),
            InlineKeyboardButton("Updates Channel ✨", url="https://t.me/od_bots"),
            ],[
            InlineKeyboardButton("Developer 🧑🏼‍💻", url="https://t.me/odysseusmax")
            ]]
            )
        )

@Client.on_message(filters.media)
async def media(client, message):
    await message.reply_text(
        text=f"""<b> Hey there {message.from_user.mention}

Choose one of the options to continue... </b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("2", callback_data="mission"),
            InlineKeyboardButton("3", callback_data="mission"),
            ],[
            InlineKeyboardButton("4", callback_data="mission"),
            InlineKeyboardButton("5", callback_data="mission"),
            ],[
            InlineKeyboardButton("6", callback_data="mission"),
            InlineKeyboardButton("7", callback_data="mission"),
            ],[
            InlineKeyboardButton("8", callback_data="mission"),
            InlineKeyboardButton("9", callback_data="mission"),
            ],[
            InlineKeyboardButton("10", callback_data="mission"),
            InlineKeyboardButton("➡️", callback_data="mission"),
            ],[
            InlineKeyboardButton("Manual Screenshots", callback_data="mission"),
            ],[
            InlineKeyboardButton("Trim Video", callback_data="mission"),
            ],[
            InlineKeyboardButton("Generate Sample Video", callback_data="mission"),
            ],[
            InlineKeyboardButton("Get Media Information", callback_data="mission")
            ]]
            )
        )

@Client.on_callback_query(filters.regex("^mission_")) # Only handle data that starts with button_
async def handle_button_callbacks(client, callback_query):
    await callback_query.answer("Error while Generating Sample Video, Try with another file..☺️")
    await callback_query.message.edit_text("Error while Generating Sample Video, Try with another file.")
