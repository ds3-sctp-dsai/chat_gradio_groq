# Flask Telegram OpenAI Bot (Webhook)

This project provides a Flask app that receives Telegram updates via webhook and replies using an OpenAI model.

## 1. Install dependencies

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 2. Configure environment

```bash
cp .env.example .env
```

Set values in `.env`:

- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional)
- `TELEGRAM_WEBHOOK_SECRET` (optional but recommended)

## 3. Run the Flask app

```bash
python app.py
```

The webhook endpoint is:

- `POST /webhook/telegram`

Health check:

- `GET /health`

## 4. Expose your local server publicly

Telegram must reach your app on a public HTTPS URL (for example via ngrok, Cloudflare Tunnel, Render, Fly.io, etc.).

Example with ngrok (separate terminal):

```bash
ngrok http 8080
```

Assume ngrok gives `https://abc123.ngrok.io`.

## 5. Register Telegram webhook

```bash
export TELEGRAM_BOT_TOKEN="<your_bot_token>"
export TELEGRAM_WEBHOOK_SECRET="<same_secret_as_env_optional>"
export WEBHOOK_URL="https://abc123.ngrok.io/webhook/telegram"
./scripts/set_telegram_webhook.sh
```

You can verify webhook status with:

```bash
curl "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo"
```

## Notes

- Telegram sends updates as JSON to your webhook endpoint.
- The app currently handles text messages from `message` and `edited_message`.
- If Telegram secret validation is enabled, requests without the matching header are rejected.
