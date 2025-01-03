from pydantic_settings import BaseSettings
from typing import List
from typing import Optional


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Shopping Cart API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # OpenTelemetry settings
    OTEL_SERVICE_NAME: str = "shopping-cart-api"
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://otel-collector:4317"
    OTEL_PYTHON_LOG_CORRELATION: bool = True
    OTEL_TRACES_SAMPLER: str = "parentbased_always_on"
    OTEL_TRACES_EXPORTER: str = "otlp"
    OTEL_METRICS_EXPORTER: str = "otlp"
    OTEL_LOGS_EXPORTER: str = "otlp"

    # Service settings
    SERVICE_NAME: str = "shopping-cart-api"
    INSTANCE_ID: str = "instance-12"
    ENVIRONMENT: str = "production"

    # Authentication settings
    NEWRELIC_API_KEY: Optional[str] = None
    OPENOBSERVE_API_KEY: Optional[str] = None

    # Redis settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PREFIX: str = "cart:"

    # Business logic settings
    MAX_CART_ITEMS: int = 50
    MAX_ITEM_QUANTITY: int = 100
    CART_EXPIRY_HOURS: int = 24
    CACHE_TTL_SECONDS: int = 3600
    RATE_LIMIT_PER_SECOND: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
