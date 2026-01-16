from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

# Health check (must always exist)
@app.route("/", methods=["GET"])
def health():
    return "OK", 200


# WhatsApp webhook (static reply for stability)
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    resp = MessagingResponse()
    resp.message("Webhook alive. Baseline restored.")
    return Response(str(resp), mimetype="application/xml"), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
