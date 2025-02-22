# Artadas Telegram Bot

Telegram Bot service for Artadas project


## Setup Instructions

### Prerequisites

- Python 3.12+
- pip

### Initialization

1. Clone the repository:
   ```bash
   git clone git@github.com:razmikarm/artadas_tg_bot.git
   cd artadas_tg_bot
   ```

2. Rename `.env.example` to `.env` and fill real data

### Local Installation and Run

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Start messaging to [Artadas bot](https://t.me/artadas_bot) in Telegram

### Set ngrok URL for bot webhook

1. Install and run [ngrok](https://ngrok.com/downloads/linux):
   ```bash
   ngrok http 8000
   ```

2. Copy `Forwarding` domain from ngrok output:
   ```yaml
   Example: https://bfe8-2a00-f3c-f4eb-0-888a-4341-e26c-7d1c.ngrok-free.app
   ```

2. Set it as a value for `WEBHOOK_URL` in `.env` file:
   ```bash
   WEBHOOK_URL=https://bfe8-2a00-f3c-f4eb-0-888a-4341-e26c-7d1c.ngrok-free.app
   ```

### Run with Docker

1. Install Docker in your system

2. Install the [Docker Compose](https://docs.docker.com/compose/install/linux/#install-using-the-repository) plugin

3. **Optional:** Leave `WEBHOOK_URL` empty in `.env` file to set it automatically from `ngrok` service

4. Build your containers:
   > Comment `backend` network for `tg_bot` service in `docker-compose.yml` file
   ```bash
   docker compose build
   ```

5. Run containers:
   ```bash
   docker compose up
   ```

6. **Additional:** Inspect requests through ngrok web interface [http://localhost:4040](http://localhost:4040)

> The project will be mounted in container, so that container will be up-to-date and will reload on new changes


## Development

### Add pre-commits

1. Install Pre-Commit Hooks:
   ```bash
   pre-commit install
   ```

2. Check if it's working:
   ```bash
   pre-commit run --all-files
   ```

### Check code manually

1. Run to check with linter:
   ```bash
   ruff check
   ```

2. Run to resolve fixable errors:
   ```bash
   ruff check --fix
   ```

3. Run to reformat code:
   ```bash
   ruff format
   ```
