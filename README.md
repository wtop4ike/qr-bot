# QR Bot

A Telegram bot written in Python that generates QR codes from text and links, with multilingual support.

## Features

- **QR Code Generation** — generate QR codes from text and links.
- **Multilingual Support** — 
The bot selects the language based on the language used in the user's messenger.
- **Configurable Language** — set the default language through environment variables.

## Project Structure

```text
qr-bot/
├── bot/
│   ├── config.py
│   ├── handlers.py
│   └── main.py
├── translations/
│   ├── __init__.py
│   ├── en.yml
│   └── ru.yml
├── utils/
│   ├── __init__.py
│   ├── generator.py
│   └── reader.py
├── requirements.txt
└── start.sh
```

## Requirements

- Python 3.11 or newer
- A Telegram bot token
- Dependencies listed in `requirements.txt`

## Installation

Clone the repository:

```bash
git clone https://github.com/wtop4ike/qr-bot.git
cd qr-bot
```

Create and activate a virtual environment.

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The bot reads its configuration from environment variables.

| Variable | Description | Default |
|---|---|---|
| `BOT_TOKEN` | Telegram bot API token | Empty |
| `DEFAULT_LANGUAGE` | Default interface language | `en` |

Set the variables before starting the bot.

**Linux / macOS:**

```bash
export BOT_TOKEN="your_telegram_bot_token"
export DEFAULT_LANGUAGE="en"
```

Replace the placeholder with your actual token. Never commit secrets or expose your bot token publicly.

## Running the Bot

From the project root, run:

```bash
python -m bot.main
```

Alternatively, on Linux or macOS, you can use the provided startup script if it is configured for your environment:

```bash
chmod +x start.sh
./start.sh
```

## Translations

Translation resources are stored in YAML files inside the `translations/` directory:

- `en.yml` — English translations
- `ru.yml` — Russian translations

The `DEFAULT_LANGUAGE` environment variable determines the default language. If you add another language, provide a corresponding YAML file and ensure the translation reader supports it.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.