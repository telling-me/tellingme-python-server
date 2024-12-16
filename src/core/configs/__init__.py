from core.configs.base_settings import Settings


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
