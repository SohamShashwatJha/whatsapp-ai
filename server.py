from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# Health check (Railway uses this)
@app.route("/")
def health():
    return "OK", 200


# WhatsApp webhook (TEST VERSION)
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    resp = MessagingResponse()
    resp.message("Webhook reached. This is a test reply.")
    return str(resp), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
