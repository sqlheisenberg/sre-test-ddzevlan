from simple_env_config import env_config


@env_config
class AppConfig:
    port: int = 9090
    why_response: str = "42"
    hostname = "localhost"
    max_buffer_size_client = 1024
