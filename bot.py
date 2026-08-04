import os
import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    try:
        loop = asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

from hydrogram import Client, filters
import yt_dlp

API_ID = 32844345       
API_HASH = "6bd5f117a5b0966be6c51255fac3023e"   
BOT_TOKEN = "8842010002:AAEMAzTHSCdwhL2sX5iRZEAoOmmkcs-oqVQ" 

app = Client("video_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "👋 **Namaste!** Main ek Video Downloader Bot hoon.\n\n"
        "🔗 Mujhe **YouTube, Instagram, ya Facebook** ka video link bhejein, main aapko fast speed mein video download karke dunga."
    )

@app.on_message(filters.text & ~filters.command("start"))
async def download_video(client, message):
    url = message.text.strip()
    
    if not (url.startswith("http://") or url.startswith("https://")):
        await message.reply_text("❌ Kripya ek valid URL bhejein.")
        return

    status_message = await message.reply_text("⏳ **Video fast download ho rahi hai, kripya intezaar karein...**")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }

    try:
        os.makedirs("downloads", exist_ok=True)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)

        await status_message.edit_text("📤 **Video upload ho rahi hai...**")
        
        await message.reply_video(
            video=file_path,
            caption="✅ **Yeh lijiye aapki video!**"
        )
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        await status_message.delete()

    except Exception as e:
        await status_message.edit_text(f"❌ **Error aaya hai:**\n`{str(e)}`")

print("🤖 Fast Bot chalu ho raha hai...")
app.run()
