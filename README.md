
# Aiogram 3 Bot Template

This is a template for telegram bots written in python using the aiogram framework

## About the template

### Used technology
* Python 3.12;
* aiogram 3.x (Asynchronous Telegram Bot framework);
* aiogram_dialog (GUI framework for telegram bot);
* fluentogram (Internationalization tool in the Fluent paradigm);
* Docker and Docker Compose (containerization);
* PostgreSQL (database);
* NATS (queue and FSM storage);
* Redis (cache);
* Alembic (database migrations with row SQL).

### Structure

```
📁 aiogram_bot_template/
├── 📁 alembic/
│   ├── 📁 versinos/
│   │   ├── 1541bb8a3f26_.py
│   │   └── b20e5643d3bd_.py
│   ├── env.py
│   └── script.py.mako
├── 📁 app/
│   ├── 📁 infrastructure/
│   │   ├── 📁 cache/
│   │   │   └── 📁 utils/
│   │   │       └── connect_to_redis.py
│   │   ├── 📁 database/
│   │   │   ├── 📁 database/
│   │   │   │   ├── db.py
│   │   │   │   └── users.py
│   │   │   ├── 📁 models/
│   │   │   │   ├── base.py
│   │   │   │   └── users.py
│   │   │   └── 📁 utils/
│   │   │       └── connect_to_pg.py
│   │   └── 📁 storage/
│   │       ├── 📁 storage/
│   │       │   └── nats_storage.py
│   │       └── 📁 utils/
│   │           └── nats_connect.py
│   ├── 📁 services/
│   │   └── 📁 delay_service/
│   │       ├── 📁 models/
│   │       │   └── delayed_messages.py
│   │       ├── 📁 utils/
│   │       │   └── start_consumer.py
│   │       ├── consumer.py
│   │       └── publisher.py
│   └── 📁 tgbot/
│       ├── 📁 config/
│       │   └── config.py
│       ├── 📁 dialogs/
│       │   ├── 📁 set_language/
│       │   │   ├── dialogs.py
│       │   │   ├── getters.py
│       │   │   └── handlers.py
│       │   └── 📁 start/
│       │       ├── dialogs.py
│       │       ├── getters.py
│       │       └── handlers.py
│       ├── 📁 enums/
│       │   ├── actions.py
│       │   └── roles.py
│       ├── 📁 filters/
│       │   └── filters.py
│       ├── 📁 handlers/
│       │   ├── commands.py
│       │   └── errors.py
│       ├── 📁 keyboards/
│       │   └── menu_button.py
│       ├── 📁 middlewares/
│       │   ├── database.py
│       │   ├── i18n.py
│       │   └── setlang.py
│       ├── 📁 states/
│       │   └── start.py
│       ├── 📁 utils/
│       │   └── i18n.py
│       ├── __init__.py
│       └── tgbot.py
├── 📁 locales/
│   ├── 📁 en/
│   │   ├── 📁 LC_MESSAGES/
│   │   │   └── txt.ftl
│   │   └── 📁 static/
│   └── 📁 ru/
│       ├── 📁 LC_MESSAGES/
│       │   └── txt.ftl
│       └── 📁 static/
├── 📁 nats/
│   └── 📁 config/
│   │   └── server.conf
│   └── 📁 migrations/
│       └── create_stream.py
├── __main__.py
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.example
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Installation

1. Clone the repository to your local machine via HTTPS:

```bash
git clone https://github.com/kmsint/aiogram_bot_template.git
```
or via SSH:
```bash
git clone git@github.com:kmsint/aiogram_bot_template.git
```

2. Create a `docker-compose.yml` file in the root of the project and copy the code from the `docker-compose.example` file into it.

3. Run `docker-compose.yml` with `docker compose up` command. You need docker and docker-compose installed on your local machine.

4. Create a virtual environment in the project root and activate it.

5. Install the required libraries in the virtual environment. With `pip`:
```bash
pip install .
```
or if you use `poetry`:
```bash
poetry install
```

6. Create a `.env` file in the root of the project and copy the code from the `.env.example` file into it. 
Replace the required secrets (BOT_TOKEN, ADMINS_CHAT, etc).

7. Perform database migrations by command:
```bash
alembic upgrade head
```

8. Run `create_stream.py` to create NATS stream for delayed messages service:
```bash
python3 nats/migrations/create_stream.py
```

9. Run `__main__.py` to check the functionality of the template.

10. You can fill the template with the functionality you need.
