from flask import Flask, request, render_template
from telegram import Bot
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import asyncio
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
ID = os.getenv('ID')
executor = ThreadPoolExecutor(2)
loop = asyncio.get_event_loop()

app = Flask(__name__)
bot = Bot(token=TOKEN)

# get index.htm
@app.route('/')
def index():
    return open('index.html').read()

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']  # Use the name of your file input field
    chat_id = ID
    file.save(f"{file.filename}")  # Save the file locally
    with open(file.filename, 'rb') as f:
        future = loop.run_in_executor(executor, lambda: asyncio.run(bot.send_document(chat_id=chat_id, document=f)))
    future.add_done_callback(lambda future: print(f"API response: {future.result()}"))  # Print the API response when the future completes
    os.remove(file.filename)
    return render_template('success.html')

if __name__ == '__main__':
    app.run(port=5000)