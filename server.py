from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os
import datetime

app = Flask(__name__)

# Health check (never remove this)
@app.route("/", methods=["GET"])
def health():
    return "OK", 200


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    resp = MessagingResponse()
    incoming = request.form.get("Body", "").strip()

    try:
        # Hard safety: always verify key at runtime
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY missing")

        client = OpenAI(api_key=api_key)

        now = datetime.datetime.now().strftime("%A, %d %B, %I:%M %p")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI accountability partner for Soham. "
                        "You are calm, direct, motivating, and grounded. "
                        "Give practical advice. No fluff."
                    ),
                },
                {
                    "role": "user",
                    "content": f"It is {now}. Soham said: {incoming}"
                }
            ],
            timeout=8
        )

        reply = completion.choices[0].message.content

    except Exception as e:
        # Fail-open: WhatsApp ALWAYS replies
        print("AI ERROR:", repr(e))
        reply = "I got your message. Small glitch on my end, but I’m here."

    resp.message(reply)
    return Response(str(resp), mimetype="application/xml"), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
