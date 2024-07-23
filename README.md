
# Aiogram 3 Bot Template

This is a template for telegram bots written in python using the aiogram framework

## About the template

### Used technology
* Python 3.12;
* aiogram 3.x (Asynchronous Telegram Bot framework);
* aiogram_dialog (GUI framework for telegram bot);
* fluentogram (Internationalization tool in the fluent paradigm);
* Docker and Docker Compose (containerization);
* PostgreSQL (database);
* NATS (queue and FSM storage);
* Redis (cache);
* Alembic (database migrations with row SQL);

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

### Installation