from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os, datetime

app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
You are an AI accountability partner for Soham.
Be calm, direct, disciplined.
One clear response at a time.
"""

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.form.get("Body", "")
    now = datetime.datetime.now().strftime("%A, %d %B, %I:%M %p")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"It is {now}. Soham said: {incoming}"}
        ]
    )

    reply = response.choices[0].message.content

    resp = MessagingResponse()
    resp.message(reply)
    return str(resp), 200


@app.route("/")
def health():
    return "OK", 200
