import asyncio
import time
import os
import subprocess
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pymongo import MongoClient
from yt_dlp import YoutubeDL
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

ADMIN_IDS = [8083702486]  # Your Telegram user IDs here


mongo = MongoClient("mongodb://localhost:27017/")
db = mongo["Cluster0"]
jobs = db["downloads"]
users = db["users"]
logs = db["logs"]

def log_event(user_id, event_type, message):
    logs.insert_one({
        "user_id": user_id,
        "event_type": event_type,
        "message": message,
        "timestamp": datetime.utcnow()
    })

def make_progress_bar(percent):
    filled = int(percent / 5)
    bar = "█" * filled + "░" * (20 - filled)
    return f"🎬 **Recording Progress:**\n`[{bar}]` {percent:.1f}%"

def get_duration(filepath):
    parser = createParser(filepath)
    if not parser:
        return "Unknown"
    with parser:
        metadata = extractMetadata(parser)
        if metadata and metadata.has("duration"):
            return str(metadata.get("duration"))
    return "Unknown"

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T"]:
        if abs(num) < 1024.0:
            return f"{num:.2f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.2f}P{suffix}"

def create_thumbnail(video_path, thumb_path, time=5):
    cmd = [
        "ffmpeg",
        "-ss", str(time),
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        thumb_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

async def record_stream(user_id, chat_id, link, duration, filename):
    log_event(user_id, "start", f"Started recording {link} for {duration}s as {filename}")
    msg = await client.send_message(
        chat_id,
        f"🔴 **Recording Started** 🔴\n\n"
        f"▶️ Link: `{link}`\n⏳ Duration: `{duration}` seconds\n"
        f"📁 Filename: `{filename}`\n\n"
        f"Please wait..."
    )

    # Extract stream url via yt-dlp
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "format": "best",
        "skip_download": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            url = info.get("url", link)
    except Exception as e:
        await msg.edit_text(f"❌ Failed to extract stream URL:\n`{e}`")
        log_event(user_id, "error", f"Extract URL failed: {e}")
        return

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", url,
        "-t", str(duration),
        "-c", "copy",
        filename
    ]

    process = await asyncio.create_subprocess_exec(
        *ffmpeg_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    start_time = time.time()
    while True:
        if process.returncode is not None:
            break
        elapsed = time.time() - start_time
        percent = min(elapsed / duration * 100, 100)
        try:
            await msg.edit_text(make_progress_bar(percent))
        except Exception:
            pass
        if elapsed >= duration:
            break
        await asyncio.sleep(1)

    await process.wait()

    if process.returncode != 0:
        err = (await process.stderr.read()).decode()
        await msg.edit_text(f"❌ **Recording failed!** ❌\n\n`{err}`")
        log_event(user_id, "error", f"FFmpeg error: {err}")
        return

    jobs.insert_one({
        "user_id": user_id,
        "link": link,
        "filename": filename,
        "status": "completed",
        "timestamp": datetime.utcnow()
    })

    await msg.edit_text(
        "✅ **Recording Complete!** ✅\n\n"
        "Select how you want to upload your file:",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📄 Upload as Document", callback_data=f"upload_doc|{filename}|{user_id}")],
                [InlineKeyboardButton("🎥 Upload as Video", callback_data=f"upload_vid|{filename}|{user_id}")]
            ]
        )
    )

    log_event(user_id, "complete", f"Recording complete for {filename}")

@client.on_message(filters.command("start"))
async def start_handler(_, message):
    await message.reply_text(
        "👋 **Welcome to Stream Recorder Bot!**\n\n"
        "Use the command:\n"
        "`/record <link> <duration_in_seconds> [filename]`\n\n"
        "Example:\n"
        "`/record https://example.com/stream.m3u8 60 myvideo.mp4`\n\n"
        "Additional commands:\n"
        "• `/setcaption Your caption with {filename}, {duration}, {size}`\n"
        "• Reply to an image with `/setthumbnail` to set a custom thumbnail\n"
        "• Admins can use `/logs` to view recent activity\n\n"
        "🎉 Enjoy recording your streams!"
    )

@client.on_message(filters.command("setcaption"))
async def set_caption(client, message: Message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.reply_text("⚠️ Usage: `/setcaption Your caption with {filename}, {duration}, {size}`", quote=True)
        return
    caption = parts[1].strip()
    users.update_one({"user_id": message.from_user.id}, {"$set": {"caption": caption}}, upsert=True)
    await message.reply_text("✅ Custom caption saved! You can use `{filename}`, `{duration}`, `{size}` placeholders.")

@client.on_message(filters.command("setthumbnail") & filters.reply)
async def set_thumbnail(client, message: Message):
    reply = message.reply_to_message
    if not reply.photo:
        await message.reply_text("⚠️ Please reply to an image to set as custom thumbnail.", quote=True)
        return
    path = f"thumb_{message.from_user.id}.jpg"
    await reply.download(file_name=path)
    users.update_one({"user_id": message.from_user.id}, {"$set": {"thumbnail": path}}, upsert=True)
    await message.reply_text("✅ Custom thumbnail saved!")

@client.on_message(filters.command("record"))
async def record_handler(client, message: Message):
    args = message.text.split(" ")
    if len(args) < 3:
        await message.reply_text("⚠️ Usage:\n`/record <link> <duration_in_seconds> [filename]`", quote=True)
        return
    link = args[1]
    try:
        duration = int(args[2])
    except ValueError:
        await message.reply_text("⚠️ Duration must be an integer number of seconds.", quote=True)
        return
    filename = args[3] if len(args) > 3 else f"record_{int(time.time())}.mp4"
    await record_stream(message.from_user.id, message.chat.id, link, duration, filename)

@client.on_message(filters.command("logs"))
async def logs_handler(client, message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply_text("❌ You are not authorized to view logs.")
        return

    recent_logs = logs.find().sort("timestamp", -1).limit(10)
    text = "📜 **Recent Logs:**\n\n"
    for log in recent_logs:
        ts = log.get("timestamp").strftime("%Y-%m-%d %H:%M:%S")
        uid = log.get("user_id")
        etype = log.get("event_type")
        msg = log.get("message")
        text += f"• [{ts}] User: `{uid}` | *{etype}* | `{msg}`\n"
    await message.reply_text(text or "No logs found.")

@client.on_callback_query()
async def callback_handler(client, query):
    data = query.data
    if data.startswith("upload_"):
        action, filename, user_id_str = data.split("|", 2)
        user_id = int(user_id_str)
        await query.answer()
        await query.message.edit_text(f"⏳ **Uploading `{filename}`...**")

        user_data = users.find_one({"user_id": user_id}) or {}
        caption_template = user_data.get("caption")
        thumb_path = user_data.get("thumbnail")

        # Compose caption
        if caption_template:
            duration_str = get_duration(filename)
            size_str = sizeof_fmt(os.path.getsize(filename))
            caption = caption_template.format(filename=filename, duration=duration_str, size=size_str)
        else:
            caption = f"📁 File: `{filename}`"

        try:
            if action == "upload_doc":
                await client.send_document(query.message.chat.id, filename, caption=caption, thumb=thumb_path)
            elif action == "upload_vid":
                await client.send_video(query.message.chat.id, filename, caption=caption, thumb=thumb_path)
            await query.message.delete()
            os.remove(filename)
            if thumb_path and os.path.exists(thumb_path):
                os.remove(thumb_path)
            log_event(user_id, "upload", f"Uploaded {filename} as {action}")
        except Exception as e:
            await query.message.edit_text(f"❌ Upload failed:\n`{e}`")
            log_event(user_id, "error", f"Upload failed: {e}")

client.run()
