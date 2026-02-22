from dynaconf import Dynaconf

# Dynaconf initialization
settings = Dynaconf(
    envvar_prefix=False,  # "DYNACONF",
    environments=True,
    env_switcher="ENV_FOR_DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
)
