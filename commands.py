import asyncio
import logging
import os
import re
import time
from datetime import datetime, timedelta
from io import BytesIO
import ffmpeg
import aiohttp

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked

import pymongo

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
OWNER_ID = 8083702486
MAX_FREE_DOWNLOADS = 3
MAX_UPLOAD_SIZE = 4 * 1024 * 1024 * 1024  # 4GB
ADMINS = [8083702486]

# --- DATABASE CONFIGURATION ---
MONGODB_URI = "mongodb+srv://astrobotzofficial:astrobotzofficial@cluster0.lchxt82.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # e.g., "mongodb://user:password@host:port/database"
DATABASE_NAME = "stream_recorder_db"
USER_COLLECTION_NAME = "users"

# --- MongoDB Client ---
mongo_client = pymongo.MongoClient(MONGODB_URI)
db = mongo_client[DATABASE_NAME]
user_collection = db[USER_COLLECTION_NAME]


# --- Helper Functions ---

def get_user_data(user_id):
    """Retrieves user data from MongoDB."""
    user_doc = user_collection.find_one({"user_id": user_id})
    if user_doc:
        return user_doc
    else:
        # Create a default user document if it doesn't exist
        default_data = {
            "user_id": user_id,
            "is_premium": False,
            "downloads_today": 0,
            "last_download": datetime.now().date()
        }
        user_collection.insert_one(default_data)
        return default_data

def update_user_data(user_id, update_data):
    """Updates user data in MongoDB."""
    user_collection.update_one({"user_id": user_id}, {"$set": update_data}, upsert=True)

def is_premium(user_id):
    user_data = get_user_data(user_id)
    return user_data.get('is_premium', False)

def can_download(user_id):
    user_data = get_user_data(user_id)
    if is_premium(user_id):
        return True

    now = datetime.now()
    last_download = user_data.get('last_download')

    if not isinstance(last_download, datetime):
        try:
            last_download = datetime.strptime(str(last_download), '%Y-%m-%d').date()
        except:
             last_download = now.date()
    else:
        last_download = last_download.date()

    if last_download != now.date():
        update_user_data(user_id, {"downloads_today": 0, "last_download": now})
        return True

    if user_data.get('downloads_today', 0) < MAX_FREE_DOWNLOADS:
        return True
    else:
        return False

def increment_download_count(user_id):
    if not is_premium(user_id):
        user_data = get_user_data(user_id)
        downloads_today = user_data.get('downloads_today', 0) + 1
        update_user_data(user_id, {"downloads_today": downloads_today, "last_download": datetime.now()})

def generate_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{caption}-{timestamp}-WEB-DL-x264-AstroBotz.mp4"

async def download_thumbnail(client, message):
    """Downloads the image sent as a thumbnail and returns the file path."""
    if message.photo:
        file_id = message.photo.file_id
        # Download the image. Use the file_id to get the image data.
        return file_id  # Store the file_id
    elif message.document and message.document.mime_type.startswith('image'):
        file_id = message.document.file_id
        return file_id
    else:
        return None  # Not a valid image

async def send_video_with_retries(client, chat_id, video_path, caption, thumbnail_path=None, retries=3):
    """Sends the video to the user with retries on FloodWait."""
    for attempt in range(retries):
        try:
            if thumbnail_path:
                await client.send_video(
                    chat_id=chat_id,
                    video=video_path,
                    caption=caption,
                    thumb=thumbnail_path,
                    supports_streaming=True,
                    progress=progress_callback,
                    progress_args=(client, chat_id, 'Uploading...')
                )
            else:
                 await client.send_video(
                    chat_id=chat_id,
                    video=video_path,
                    caption=caption,
                    supports_streaming=True,
                    progress=progress_callback,
                    progress_args=(client, chat_id, 'Uploading...')
                )

            return True  # Success
        except FloodWait as e:
            wait_time = e.value + 5
            logger.warning(f"FloodWait encountered. Waiting for {wait_time} seconds. Attempt {attempt + 1}/{retries}")
            await asyncio.sleep(wait_time)
        except UserIsBlocked:
            logger.error(f"User {chat_id} has blocked the bot.")
            return False
        except Exception as e:
            logger.error(f"Error sending video: {e}")
            return False

    logger.error(f"Failed to send video after {retries} attempts.")
    return False # All retries failed

async def progress_callback(current, total, client, chat_id, message_text):
    """Custom progress callback function."""
    percentage = current * 100 / total
    progress_message = f"{message_text}: {percentage:.1f}%"
    try:
        await client.edit_message_text(chat_id=chat_id, message_id=progress_callback.message.id, text=progress_message)
    except Exception as e:
        logger.warning(f"Error updating progress message: {e}")

    await asyncio.sleep(2)  # Throttle updates to avoid FloodWait

# --- Command Handlers ---

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text="Help", callback_data="help")]
        ]
    )
    await message.reply_text("Welcome to the Stream Recorder Bot!\n\nUse /record to start recording a stream.", reply_markup=reply_markup)

@Client.on_callback_query()
async def help_callback(client: Client, callback_query: CallbackQuery):
    if callback_query.data == "help":
        await callback_query.answer()
        await callback_query.edit_message_text(
            "**Help:**\n"
            "/record <m3u8/mpd URL> <start_time> <end_time>\n"
            "  - Records a stream from start_time to end_time.\n"
            "  - Times are in HH:MM:SS format.\n"
            "/setcaption <custom caption>\n"
            "  - Sets a custom caption for your recordings.\n"
            "/setthumbnail (reply to image)\n"
            "  - Sets a thumbnail for your recordings. Reply to an image message.\n"
            "/myinfo - Shows your premium status and download count.\n"
        )

@Client.on_message(filters.command("record"))
async def record_command(client: Client, message: Message):
    user_id = message.from_user.id
    if not can_download(user_id):
        await message.reply_text("You have reached your daily download limit. Become a premium user to download unlimited videos.")
        return

    try:
        args = message.text.split(" ", 3) #splits into 4 parts.
        if len(args) != 4:
            await message.reply_text("Usage: /record <m3u8/mpd URL> <start_time> <end_time>")
            return

        stream_url = args[1]
        start_time_str = args[2]
        end_time_str = args[3]

        # Validate URL
        if not stream_url.startswith("http"):
            await message.reply_text("Invalid stream URL. Must start with http.")
            return

        # Validate Time Format
        try:
            start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
            end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
            now = datetime.now()
            start_datetime = datetime.combine(now.date(), start_time)
            end_datetime = datetime.combine(now.date(), end_time)

            if end_datetime <= start_datetime:
                await message.reply_text("End time must be after start time.")
                return

            duration = (end_datetime - start_datetime).total_seconds()
            if duration <= 0:
                await message.reply_text("Invalid start and end times.")
                return

        except ValueError:
            await message.reply_text("Invalid time format. Use HH:MM:SS.")
            return


        filename = generate_filename()
        output_path = os.path.join(".", filename) # Current directory

        user_data = get_user_data(user_id)
        custom_caption = user_data.get('caption', "Recorded Stream")
        thumbnail_file_id = user_data.get('thumbnail')

        await message.reply_text("Starting recording...", quote=True)
        progress_callback.message = await message.reply_text("Initializing...", quote=True) #Store the message object to edit it later.


        try:
            logger.info(f"Starting recording for user {user_id} from {stream_url} for {duration} seconds.")
            process = await asyncio.create_subprocess_exec(
                'ffmpeg',
                '-y',
                '-i', stream_url,
                '-ss', start_time_str,
                '-to', end_time_str,
                '-c', 'copy',
                output_path,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                 error_message = stderr.decode()
                 logger.error(f"FFmpeg error: {error_message}")
                 await message.reply_text(f"FFmpeg error: {error_message}")
                 return

            file_size = os.path.getsize(output_path)

            if file_size > MAX_UPLOAD_SIZE:
                await message.reply_text("Video size exceeds the maximum allowed size (4GB).")
                os.remove(output_path)  # Clean up
                return

            # Prepare thumbnail
            thumb_path = None
            if thumbnail_file_id:
                try:
                    thumb_path = await client.download_media(thumbnail_file_id, file_name="thumbnail.jpg")
                except Exception as e:
                    logger.error(f"Error downloading thumbnail: {e}")
                    await message.reply_text("Error downloading your thumbnail, continuing without it.")

            # Send the video
            increment_download_count(user_id)
            upload_success = await send_video_with_retries(client, user_id, output_path, custom_caption, thumb_path)

            if upload_success:
                await message.reply_text("Recording complete and uploaded!")
            else:
                await message.reply_text("Failed to upload the video.")

            # Clean up
            if os.path.exists(output_path):
                os.remove(output_path)
            if thumb_path and os.path.exists(thumb_path):
                os.remove(thumb_path)

        except Exception as e:
            logger.exception(f"An error occurred during recording: {e}")
            await message.reply_text(f"An error occurred: {e}")
            if os.path.exists(output_path):
                os.remove(output_path) #Clean up if error occured.

    except Exception as e:
        logger.exception(f"Error processing record command: {e}")
        await message.reply_text(f"An error occurred: {e}")



@Client.on_message(filters.command("setcaption"))
async def set_caption_command(client: Client, message: Message):
    user_id = message.from_user.id
    try:
        new_caption = message.text.split(" ", 1)[1]
        update_user_data(user_id, {"caption": new_caption})
        await message.reply_text("Caption updated!")
    except IndexError:
        await message.reply_text("Usage: /setcaption <new caption>")

@Client.on_message(filters.command("setthumbnail") & filters.reply)
async def set_thumbnail_command(client: Client, message: Message):
    user_id = message.from_user.id
    replied_message = message.reply_to_message

    thumbnail_file_id = await download_thumbnail(client, replied_message) #Store the file_id

    if thumbnail_file_id:
        update_user_data(user_id, {"thumbnail": thumbnail_file_id})
        await message.reply_text("Thumbnail updated!")
    else:
        await message.reply_text("Reply to an image to set as thumbnail.")

@Client.on_message(filters.command("promote") & filters.user(ADMINS))
async def promote_command(client: Client, message: Message):
    try:
        user_id_to_promote = int(message.text.split(" ")[1])
        update_user_data(user_id_to_promote, {"is_premium": True})
        await message.reply_text(f"User {user_id_to_promote} promoted to premium.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: /promote <user_id>")

@Client.on_message(filters.command("demote") & filters.user(ADMINS))
async def demote_command(client: Client, message: Message):
    try:
        user_id_to_demote = int(message.text.split(" ")[1])
        update_user_data(user_id_to_demote, {"is_premium": False})
        await message.reply_text(f"User {user_id_to_demote} demoted to free.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: /demote <user_id>")

@Client.on_message(filters.command("myinfo"))
async def myinfo_command(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    is_user_premium = user_data.get('is_premium', False)
    downloads_today = user_data.get('downloads_today', 0)

    info_text = f"Your User ID: {user_id}\n"
    info_text += f"Premium Status: {is_user_premium}\n"
    if not is_user_premium:
        info_text += f"Downloads Today: {downloads_today} / {MAX_FREE_DOWNLOADS}"

    await message.reply_text(info_text)

# --- Start the Bot ---
app.run()
