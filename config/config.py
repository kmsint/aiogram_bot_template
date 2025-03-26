from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=False,  # "DYNACONF",
    environments=True,  # Автоматически использовать секцию текущей среды
    env_switcher="ENV_FOR_DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
)
