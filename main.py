from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # Tanpa @
STREAM_LINK = os.getenv("STREAM_LINK")  # Link website series

app = Client("bangsabacolbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    try:
        member = await client.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        if member.status in ["member", "administrator", "creator"]:
            button = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Tonton Sekarang", url=STREAM_LINK)]
            ])
            await message.reply("Klik tombol di bawah untuk mulai nonton:", reply_markup=button)
        else:
            raise Exception("Not a member")
    except:
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
            [InlineKeyboardButton("✅ Sudah Join", callback_data="check_sub")]
        ])
        await message.reply("Gabung dulu ke channel untuk mendapatkan akses nonton:", reply_markup=join_button)

@app.on_message(filters.text & ~filters.command("start"))
async def text_handler(client, message):
    await start(client, message)

@app.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client, callback_query):
    user_id = callback_query.from_user.id
    try:
        member = await client.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        if member.status in ["member", "administrator", "creator"]:
            button = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 Tonton Sekarang", url=STREAM_LINK)]
            ])
            await callback_query.message.edit("Klik tombol di bawah untuk mulai nonton:", reply_markup=button)
            await callback_query.answer()
        else:
            await callback_query.answer("Kamu belum join channel.", show_alert=True)
    except:
        await callback_query.answer("Kamu belum join channel.", show_alert=True)

app.run()