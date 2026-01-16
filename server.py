from flask import Response
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import datetime
import os

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    resp = MessagingResponse()

    try:
        incoming = request.form.get("Body", "").strip()
        now = datetime.datetime.now().strftime("%A, %d %B, %I:%M %p")

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY missing")

        client = OpenAI(api_key=api_key)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a calm, direct accountability partner for Soham."},
                {"role": "user", "content": f"It is {now}. Soham said: {incoming}"}
            ],
            timeout=10
        )

        reply = completion.choices[0].message.content

    except Exception as e:
        print("ERROR:", repr(e))
        reply = "I got your message. Small glitch—trying again."

    resp.message(reply)
    return Response(str(resp), mimetype="application/xml"), 200
