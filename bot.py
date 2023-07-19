from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bs4 import BeautifulSoup

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Please send me an HTML file or .html file from your storage.', reply_markup=ForceReply(selective=True))

def convert_html_to_txt(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.document.file_id)
    file.download('temp.html')
    with open('temp.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        text = soup.get_text()
        with open('temp.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        links = soup.find_all('a')
        with open('links.txt', 'w', encoding='utf-8') as f:
            for link in links:
                name = link.text
                url = link.get('href')
                f.write(f'{name}:{url}\n')
    with open('temp.txt', 'rb') as f:
        update.message.reply_document(f)
    with open('links.txt', 'rb') as f:
        update.message.reply_document(f)

def main() -> None:
    updater = Updater("YOUR_TOKEN_HERE")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.file_extension("html"), convert_html_to_txt))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()