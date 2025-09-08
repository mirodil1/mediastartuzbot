# mediastartuzbot

A Telegram bot for accepting media submissions, with an admin panel built using Django.

## Features

- Accept media submissions via Telegram
- Admin dashboard for managing submissions (Django)
- Media upload and download
- User-friendly commands
- Logging and error handling

## Installation

Clone the repository and set up using Docker:

```bash
git clone https://github.com/yourusername/mediastartuzbot.git
cd mediastartuzbot
docker-compose -f local.yml up
```

## Usage

1. Configure your bot token and Django settings in `.env` or `config.py`.
2. Start the services with Docker Compose:

    ```bash
    docker-compose -f local.yml up
    ```
