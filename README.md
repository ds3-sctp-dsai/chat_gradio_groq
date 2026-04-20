# Flask Telegram OpenAI Bot (Webhook)

This project provides a Flask app that receives Telegram updates via webhook and replies using an OpenAI model.

## Local Development

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

Run locally:

```bash
python app.py
```

The webhook endpoint is:

- `POST /webhook/telegram`

Health check:

- `GET /health`

## Deploy on Render (Gunicorn)

Render Web Service settings:

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
- Python version: use your preferred 3.x version

Environment variables in Render:

- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- `OPENAI_MODEL` (optional, default `gpt-4.1-mini`)
- `TELEGRAM_WEBHOOK_SECRET` (optional but recommended)
- Do not set `PORT` manually in Render. Render injects this automatically.

The included `Procfile` also defines:

- `web: gunicorn app:app --bind 0.0.0.0:$PORT`

After deploy, your Render app URL is usually:

- `https://<your-service-name>.onrender.com`

Webhook URL:

- `https://<your-service-name>.onrender.com/webhook/telegram`

## Register Telegram webhook

```bash
export TELEGRAM_BOT_TOKEN="<your_bot_token>"
export TELEGRAM_WEBHOOK_SECRET="<same_secret_as_env_optional>"
export WEBHOOK_URL="https://<your-service-name>.onrender.com/webhook/telegram"
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
