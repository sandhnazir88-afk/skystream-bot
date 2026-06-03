import os
import base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 AAPKA BOT TOKEN AUR WEBSITE URL
BOT_TOKEN = 8798315268:AAHOnMRMw21mnua_1bYD-ucY0HvTI6ZoHLI
YOUR_BLOG_URL = https://skystreamm.blogspot.com/
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Welcome to SkyStream Core Bot!\n\n"
        "Mujhe koi bhi Video, File ya Direct Link bhejo/forward karo. "
        "Main turant use SkyStream ke high-earning link mein badal dunga!"
    )

async def generate_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Status message dikhane ke liye
    status_msg = await update.message.reply_text("⏳ Processing file & generating secure cloud link...")
    
    file_url = ""
    
    # 1. Agar user ne direct link bheja hai
    if update.message.text:
        file_url = update.message.text.strip()
        
    # 2. Agar user ne Video bheji hai (Telegram local link simulation)
    elif update.message.video:
        # Note: Direct video stream ke liye professional bots ise file-sharing server par upload karte hain.
        # Abhi ke liye hum telegram file link ya dummy path ko base64 kar rahe hain.
        file_id = update.message.video.file_id
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"
        
    # 3. Agar user ne koi Document/File bheji hai
    elif update.message.document:
        file_id = update.message.document.file_id
        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_id}"

    if file_url:
        try:
            # 🔐 Link ko Base64 mein encrypt karna
            string_bytes = file_url.encode("ascii")
            base64_bytes = base64.b64encode(string_bytes)
            encoded_link = base64_bytes.decode("ascii")
            
            # 🚀 Final SkyStream URL banana
            final_earning_url = f"{YOUR_BLOG_URL}?download={encoded_link}"
            
            # Response message template (Ekdam professional formatting)
            response_text = (
                "🎯 **SkyStream Link Generated Successfully!**\n\n"
                f"🔗 **Your Earning Link:**\n`{final_earning_url}`\n\n"
                "💡 *Is link ko copy karo aur apne Telegram Channel par post kar do. Monetag Ads live hain!*"
            )
            
            await status_msg.edit_text(response_text, parse_mode="Markdown")
            
        except Exception as e:
            await status_msg.edit_text(f"❌ Error: Link generate nahi ho paya. Details: {str(e)}")
    else:
        await status_msg.edit_text("❌ Mujhe samajh nahi aaya! Kripya koi valid video, file ya link bhejein.")

def main():
    # Application build karna
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers add karna
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_link))
    application.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, generate_link))

    # Bot shuru karna
    print("SkyStream Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
