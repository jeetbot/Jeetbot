import os
import re
import yt_dlp
from hydrogran import Client, filters
from flask import Flask
from threading import Thread

# Flask web server taaki Render ka port timeout error na aaye
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "🤖 Bot is alive and running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

t = Thread(target=run_flask)
t.start()

API_ID = 32044345
API_HASH = "6bd5f117a5b0966be6c51255fac3023e"
BOT_TOKEN = "8842010032:AAEMAxTHSCdwhL2sX5lRZEAo0mmkcs-eqVQ"

app = Client("video_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "👋 **Namaste!** Main ek Video Downloader Bot hoon.\n\n"
        "🔗 Mujhe **YouTube, Instagram, ya Facebook** ka video link bhejein, main aapko fast speed mein video download karke dunga."
    )

@app.on_message(filters.text & ~filters.command("start"))
async def download_video(client, message):
    text = message.text.strip()
    
    url_match = re.search(r'(https?://[^\s]+)', text)
    if not url_match:
        return  

    raw_url = url_match.group(1)
    
    if "instagram.com" in raw_url:
        clean_url = raw_url.split("?")[0]
    else:
        clean_url = raw_url

    status_message = await message.reply_text("⏳ **Video fast download ho rahi hai, kripya intezaar karein...**")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }

    try:
        os.makedirs("downloads", exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(clean_url, download=True)
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
        await status_message.edit_text(f"❌ **Error aaya hai:**\n\n{str(e)}")

print("🚀 Fast Bot chalu ho raha hai...")
app.run()
