from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""

    app_title: str = (
        'Приложение для Благотворительного фонда поддержки котиков QRKot'
    )
    app_description: str = (
        'Фонд собирает пожертвования на различные целевые проекты: '
        'на медицинское обслуживание нуждающихся хвостатых, '
        'на обустройство кошачьей колонии в подвале, '
        'на корм оставшимся без попечения кошкам — на любые цели, '
        'связанные с поддержкой кошачьей популяции.'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'you-will-never-guess'

    class Config:
        env_prefix = 'CCF_'
        env_file = '.env'


settings = Settings()
