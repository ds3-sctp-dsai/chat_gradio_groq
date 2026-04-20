import os
from typing import Any

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from openai import OpenAI


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in environment")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in environment")

app = Flask(__name__)
openai_client = OpenAI(api_key=OPENAI_API_KEY)


TELEGRAM_API_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def _send_telegram_message(chat_id: int, text: str) -> None:
    url = f"{TELEGRAM_API_BASE}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()


def _extract_user_text(update: dict[str, Any]) -> tuple[int | None, str | None]:
    message = update.get("message") or update.get("edited_message")
    if not message:
        return None, None

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text")
    if not isinstance(chat_id, int) or not isinstance(text, str):
        return None, None

    return chat_id, text.strip()


def _generate_llm_reply(user_text: str) -> str:
    response = openai_client.responses.create(
        model=OPENAI_MODEL,
        input=user_text,
    )
    return response.output_text.strip() or "I could not generate a response."


@app.get("/health")
def health() -> Any:
    return jsonify({"status": "ok"})


@app.post("/webhook/telegram")
def telegram_webhook() -> Any:
    if TELEGRAM_WEBHOOK_SECRET:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if secret != TELEGRAM_WEBHOOK_SECRET:
            return jsonify({"ok": False, "error": "unauthorized"}), 401

    update = request.get_json(silent=True) or {}
    chat_id, user_text = _extract_user_text(update)

    if chat_id is None or not user_text:
        return jsonify({"ok": True, "ignored": True})

    try:
        assistant_reply = _generate_llm_reply(user_text)
    except Exception:
        assistant_reply = "I hit an error talking to the model. Please try again."

    try:
        _send_telegram_message(chat_id, assistant_reply)
    except Exception:
        # Swallow Telegram send errors so webhook still returns success quickly.
        pass

    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
