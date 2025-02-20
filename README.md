
# Aiogram 3 Bot Template

This is a template for telegram bots written in python using the `aiogram` framework


You can learn how to develop telegram bots using the `aiogram` framework in the following courses (in Russian):
1. <a href="https://stepik.org/course/120924/">Телеграм-боты на Python и AIOgram</a>
2. <a href="https://stepik.org/a/153850?utm_source=kmsint_github">Телеграм-боты на Python: продвинутый уровень</a>

## About the template

### Used technology
* Python 3.12;
* aiogram 3.x (Asynchronous Telegram Bot framework);
* aiogram_dialog (GUI framework for telegram bot);
* dynaconf (Configuration Management for Python);
* taskiq (Async Distributed Task Manager);
* fluentogram (Internationalization tool in the Fluent paradigm);
* Docker and Docker Compose (containerization);
* PostgreSQL (database);
* NATS (queue and FSM storage);
* Redis (cache, taskiq result backend);
* Alembic (database migrations with raw SQL).

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
│   ├── 📁 bot/
│   │   ├── 📁 dialogs/
│   │   │   ├── 📁 settings/
│   │   │   │   ├── dialogs.py
│   │   │   │   ├── getters.py
│   │   │   │   ├── handlers.py
│   │   │   │   └── keyboards.py
│   │   │   └── 📁 start/
│   │   │       ├── dialogs.py
│   │   │       ├── getters.py
│   │   │       └── handlers.py
│   │   ├── 📁 enums/
│   │   │   ├── actions.py
│   │   │   └── roles.py
│   │   ├── 📁 filters/
│   │   │   └── dialog_filters.py
│   │   ├── 📁 handlers/
│   │   │   ├── commands.py
│   │   │   └── errors.py
│   │   ├── 📁 i18n/
│   │   │   └── translator_hub.py
│   │   ├── 📁 keyboards/
│   │   │   ├── links_kb.py
│   │   │   └── menu_button.py
│   │   ├── 📁 middlewares/
│   │   │   ├── database.py
│   │   │   └── i18n.py
│   │   ├── 📁 states/
│   │   │   ├── settings.py
│   │   │   └── start.py
│   │   ├── __init__.py
│   │   └── bot.py
│   ├── 📁 infrastructure/
│   │   ├── 📁 cache/
│   │   │   └── connect_to_redis.py
│   │   ├── 📁 database/
│   │   │   ├── 📁 database/
│   │   │   │   ├── db.py
│   │   │   │   └── users.py
│   │   │   ├── 📁 models/
│   │   │   │   ├── base.py
│   │   │   │   └── users.py
│   │   │   └── connect_to_pg.py
│   │   └── 📁 storage/
│   │       ├── 📁 storage/
│   │       │   └── nats_storage.py
│   │       └── nats_connect.py
│   └── 📁 services/
│       ├── 📁 delay_service/
│       │   ├── 📁 models/
│       │   │   └── delayed_messages.py
│       │   ├── consumer.py
│       │   ├── publisher.py
│       │   └── start_consumer.py
│       └── 📁 scheduler/
│           ├── taskiq_broker.py
│           └── tasks.py
├── 📁 config/
│   ├── config.py
│   └── settings.toml
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
│   ├── 📁 config/
│   │   └── server.conf
│   └── 📁 migrations/
│       └── create_stream.py
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.example
├── docker-compose.yml
├── main.py
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

3. Create a `.env` file in the root of the project and copy the code from the `.env.example` file into it. Replace the required secrets (BOT_TOKEN, ADMINS_CHAT, etc).

4. Run `docker-compose.yml` with `docker compose up` command. You need docker and docker-compose installed on your local machine.

5. Create a virtual environment in the project root and activate it.

6. Install the required libraries in the virtual environment. With `pip`:
```bash
pip install .
```
or if you use `poetry`:
```bash
poetry install --no-root
```
7. Write SQL code in the `upgrade` and `downgrade` functions to create a database schema. See example in file `alembic/versions/1541bb8a3f26_.py`.

8. If required, create additional empty migrations with the command:
```bash
alembic revision
```
and fill them with SQL code.

9. Apply database migrations using the command:
```bash
alembic upgrade head
```

10. Run `create_stream.py` to create NATS stream for delayed messages service:
```bash
python3 nats/migrations/create_stream.py
```

11. If you want to use the Taskiq broker for background tasks as well as the Taskiq scheduler, add your tasks to the `tasks.py` module and start the worker first:
```bash
taskiq worker app.services.scheduler.taskiq_broker:broker -fsd
```
and then the scheduler:
```bash
taskiq scheduler app.services.scheduler.taskiq_broker:scheduler
```

12. Run `main.py` to check the functionality of the template.

13. You can fill the template with the functionality you need.

## Developer tools

For convenient interaction with nats-server you need to install nats cli tool. For macOS you can do this through the homebrew package manager. Run the commands:
```bash
brew tap nats-io/nats-tools
brew install nats-io/nats-tools/nats
```
For linux:
```bash
curl -sf https://binaries.nats.dev/nats-io/natscli/nats@latest | sh
sudo mv nats /usr/local/bin/
```
After this you can check the NATS version with the command:
```bash
nats --version
```

## TODO

1. Add mailing service
2. Set up a CICD pipeline using Docker and GitHub Actions