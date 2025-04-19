import random
import asyncio
import os
import re
import subprocess
import time
import requests
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import UserNotParticipant

force_channel = "IndianRobots"

# Replace with your Telegram Bot API Token
BOT_TOKEN = "7398500602:AAFZJPiJa-igPnJthlxslZWDBnkwiLkZmlU"

# Replace with your Telegram App API ID and Hash
API_ID = "22136772"
API_HASH = "7541e5b6d298eb1f60dac89aae92868c"

# Initialize the Pyrogram client
bot = Client(
    "live-recording-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@bot.on_message(filters.command("start"))
async def start(bot, update):
    if force_channel:
        try:
            user = await bot.get_chat_member(force_channel, update.from_user.id)
            if user.status == "kicked out":
                await update.reply_text("You Are Banned")
                return
        except UserNotParticipant :
            await update.reply_text(
                text="Sᴏʀʀy Dᴜᴅᴇ Yᴏᴜ'ʀᴇ Nᴏᴛ Jᴏɪɴᴇᴅ My Cʜᴀɴɴᴇʟ 😐. Sᴏ Pʟᴇᴀꜱᴇ Jᴏɪɴ Oᴜʀ Uᴩᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴏɴᴛɪɴᴜᴇ",
                reply_markup=InlineKeyboardMarkup( [[
                 InlineKeyboardButton("🔊 𝗝𝗼𝗶𝗻 𝗢𝘂𝗿 𝗠𝗮𝗶𝗻 𝗰𝗵𝗮𝗻𝗻𝗲𝗹", url=f"t.me/{force_channel}")
                 ]]
                 )
            )
            return
    await update.reply_photo(
        photo="http://postimg.cc/3ddb8qWD",
        caption=f"""<b> Hey There {update.from_user.mention} 👋,

I am a Live Recorder Bot, Just Send Me Any Supported URL In Appropriate Format and I'll upload file remotely to Telegram.

💡 Use /help to learn how to use the bot.
🔒 Subscription required for usage.

⚜ Maintained By : @IndianRobots </b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("📣 Updates", url="t.me/IndianRobots"),
            InlineKeyboardButton("👥 Support", url="t.me/IndianRobots")
            ]]
            )
        )

@bot.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_photo(
        photo="http://postimg.cc/3ddb8qWD",
        caption=f"""<b> Hey There {message.from_user.mention} 👋,

📝 How to Record Live Streams
------------------------------

Format :
-------
[URL] [Filename] [Custom Time]

Time Format: HH:MM:SS

Note : 
-----
- Duration accuracy may vary depending on stream source
- Custom filename is optional
- If no filename is provided, "Recorded_by_@IndianRobots.mp4" will be used

⚜ Maintained By : @IndianRobots </b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("📣 Updates", url="t.me/IndianRobots"),
            InlineKeyboardButton("👥 Support", url="t.me/IndianRobots")
            ]]
            )
        )

@bot.on_message(filters.command("about"))
async def about(client, message):
    await message.reply_photo(
        photo="http://postimg.cc/3ddb8qWD",
        caption=f"""<b> Hey There {message.from_user.mention} 👋,

⍟ My Name : Live Recorder Bot
⍟ Owner : @YadhuTG
⍟ Updates Channel : @IndianRobots
⍟ Language : Python3
⍟ Library : Pyrogram
⍟ Server : VPS 

⚜ Maintained By : @IndianRobots </b>""",
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton("📣 Updates", url="t.me/IndianRobots"),
            InlineKeyboardButton("👥 Support", url="t.me/IndianRobots")
            ]]
            )
        )
        

async def is_url(url):
    """Checks if the given string is a valid URL."""
    regex = re.compile(
        r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
        re.IGNORECASE,
    )
    return regex.match(url) is not None


async def get_file_name(url):
    """Gets a filename from a URL or uses a default one."""
    try:
        response = requests.head(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            file_name = re.findall("filename=(.+)", content_disposition)
            if file_name:
                return file_name[0]
    except requests.exceptions.RequestException as e:
        print(f"Error getting filename from URL: {e}")

    return None


async def download_stream_requests(url, file_name, message, custom_time):
    """Downloads the stream using requests."""
    try:
        output_template = file_name or "Recorded_by_@IndianRobots.mp4"
        if not output_template.endswith(".mp4"):
            output_template += ".mp4"

        start_time = time.time()
        print(f"Connecting to {url}")  # Log the connection attempt
        response = requests.get(url, stream=True)
        print(f"Response status code: {response.status_code}")  # Log the status code
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        total_length = response.headers.get("content-length")
        if total_length is None:  # no content length header
            await message.edit_text("Downloading...")
        else:
            total_length = int(total_length)

        chunk_size = 65536  # 64KB chunks (increased buffer size) - Adjust this as needed
        bytes_downloaded = 0

        with open(output_template, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    bytes_downloaded += len(chunk)

                    if total_length:
                        percent = (bytes_downloaded / total_length) * 100
                        await message.edit_text(
                            f"Downloading: {percent:.2f}% ({bytes_downloaded / (1024 * 1024):.2f} MB / {total_length / (1024 * 1024):.2f} MB)"
                        )  # Progress update
                    print(f"Downloaded chunk of size: {len(chunk)}") #Log each chunk
        end_time = time.time()
        download_time = end_time - start_time
        await message.edit_text(
            f"Download complete! Saved as {output_template}\nDownload Time: {download_time:.2f} seconds"
        )
        return output_template  # return filepath

    except requests.exceptions.RequestException as e:
        print(f"RequestException during download: {e}")
        await message.edit_text(f"Download failed: {e}")
        return None
    except Exception as e:
        print(f"Exception during download: {e}")
        await message.edit_text(f"An unexpected error occurred:\n{e}")
        return None


async def upload_video(file_path, message, file_name):
    """Uploads the recorded video to Telegram."""
    if not os.path.exists(file_path):
        await message.edit_text(f"Error: File not found at {file_path}")
        return

    try:
        duration = await get_video_duration(file_path)  # Get video duration
        await message.edit_text("Uploading...")
        await bot.send_video(
            chat_id=message.chat.id,
            video=file_path,
            caption=f"{file_name}/n/nRecorded By @IndianRobots",
            duration=duration,  # Set video duration
            supports_streaming=True,  # Enable streaming if supported
        )
        await message.delete()
        os.remove(file_path)  # Delete the local file after upload
    except Exception as e:
        print(f"Upload failed: {e}")
        await message.edit_text(f"Upload failed: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)  # Delete file on failure as well to avoid disk clogging


async def get_video_duration(file_path):
    """Gets the duration of a video file using hachoir."""
    try:
        parser = createParser(file_path)
        if not parser:
            return 0  # Unable to parse video

        metadata = extractMetadata(parser)
        if not metadata:
            return 0  # Unable to extract metadata

        for line in metadata.exportPlaintext():
            if line.startswith("Duration: "):
                duration_str = line[len("Duration: ") :]
                parts = duration_str.split(":")
                if len(parts) == 3:
                    hours, minutes, seconds = map(int, parts)
                    return hours * 3600 + minutes * 60 + seconds
                elif len(parts) == 2:
                    minutes, seconds = map(int, parts)
                    return minutes * 60 + seconds
        return 0  # Duration not found

    except Exception as e:
        print(f"Error getting video duration: {e}")
        return 0  # Error during processing


@bot.on_message(filters.command("download"))
async def download_command(client, message):
    """Handles the /download command."""
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("Usage: /download <URL> [filename] [custom_time]")
        return

    url = args[1].split()[0]
    if not await is_url(url):
        await message.reply_text("Invalid URL provided.")
        return

    file_name = None
    custom_time = None

    # Extract optional filename and custom_time. Splitting by spaces allows for
    # more structured command usage: /download <url> <filename> <custom_time>
    parts = args[1].split()
    if len(parts) > 1:
        file_name = parts[1]  #Filename becomes second word
    if len(parts) > 2:
        custom_time = parts[2] #Custom time becomes third word


    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Cancel", callback_data="cancel_download")
            ]
        ]
    )

    download_message = await message.reply_text(
        "Starting download...", reply_markup=reply_markup
    )

    file_path = await download_stream_requests(url, file_name, download_message, custom_time)

    if file_path:
        await upload_video(file_path, download_message, file_name)


@bot.on_callback_query(filters.regex("cancel_download"))
async def cancel_download_callback(client, callback_query):
    """Handles the cancel button."""
    await callback_query.answer("Download cancelled.")
    await callback_query.message.edit_text("Download cancelled by user.")
    # Termination of yt-dlp process is handled in download_stream function.


print("Bot started.")
bot.run()
