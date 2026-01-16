from flask import Response
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os, datetime

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    resp = MessagingResponse()
    incoming = request.form.get("Body", "").strip()

    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY missing")

        client = OpenAI(api_key=api_key)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a calm, direct accountability partner for Soham."},
                {"role": "user", "content": incoming}
            ],
            timeout=8
        )

        reply = completion.choices[0].message.content

    except Exception as e:
        print("OPENAI ERROR:", repr(e))
        reply = "I’m here. AI had a hiccup, but I got your message."

    resp.message(reply)
    return Response(str(resp), mimetype="application/xml"), 200
