# src/config/env_config.py
import os

ENV = os.environ.get("APP_ENV", "dev")

IS_PROD = ENV == "prod"
