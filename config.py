from dataclasses import dataclass

from environs import Env


@dataclass
class DjangoSetting:
    """Django configuration data"""

    secret_key: str
    debug: bool


@dataclass
class Config:
    """Project configration data."""

    django_settings: DjangoSetting


def load_config() -> Config:
    """Load environment variables from .env file."""

    env = Env()
    env.read_env()
    return Config(
        DjangoSetting(
            secret_key=env.str('SECRET_KEY', 'SECRET_KEY'),
            debug=env.bool('DEBUG'),
        ),
    )


config: Config = load_config()
