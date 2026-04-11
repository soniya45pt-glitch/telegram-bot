from flask import Flask, request
import hmac, hashlib, json, os, requests
from database import set_paid

app = Flask(__name__)

SECRET = os.getenv("mysecret12")
BOT_TOKEN = "8621358668:AAEzPQCtDTlWauYltL8kzkWBZ1h-oPwr-AM"


def send_message(user_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": user_id, "text": text})

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.data
    signature = request.headers.get("X-Razorpay-Signature")

    expected = hmac.new(
        SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if expected == signature:
        data = json.loads(body)

        if data["event"] == "payment.captured":
            payment = data["payload"]["payment"]["entity"]

            user_id = int(payment["notes"]["user_id"])

            set_paid(user_id)

            send_message(user_id, "✅ Payment done! You got access 😏")

    return "OK"
