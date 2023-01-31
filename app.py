import openai
import requests
from flask import Flask, request

app = Flask(__name__)

# Initialize OpenAI API key
openai.api_key = "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"

# Your Telegram Bot API key
TELEGRAM_BOT_TOKEN = "5970232087:AAHpnfPXJtQIA1k2ZFcntRi5_kLdvlWMahE"

# URL for sending messages to Telegram bot
TELEGRAM_SEND_MESSAGE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

@app.route("/telegram_webhook", methods=["GET"])
def telegram_webhook():
    # Extract the message from the Telegram request
    message = requests.get_json()["message"]["text"]

    # Use GPT-3 to generate a response to the message
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Reply to: {message}\n\n",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).get("choices")[0].text

    # Send the response back to Telegram
    requests.get(TELEGRAM_SEND_MESSAGE_URL, json={
        "chat_id": request.get_json()["message"]["chat"]["id"],
        "text": response,
    })

    return "OK"

if __name__ == "__main__":
    app.run()
