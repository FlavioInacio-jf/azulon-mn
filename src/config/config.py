from __future__ import annotations

import os
from dotenv import load_dotenv

class ConfigLoader:
    """
    Loads configuration from environment variables (and optionally from a .env file).

    Usage:
        cfg = ConfigLoader().load_config()
    """

    def __init__(self, load_dotenv_file: bool = True) -> None:
        self._load_dotenv_file = load_dotenv_file

    def load_env_file(self) -> None:
        """Load environment variables from a .env file if configured to do so."""
        if self._load_dotenv_file:
            load_dotenv()

    def get_env_var(self, var_name: str, default: str = "") -> str:
        """Get an environment variable with an optional default."""
        return os.getenv(var_name, default)

    @staticmethod
    def _get_float_0_1(var_name: str, default: float) -> float:
        """Helper to read a float from env vars, ensuring it's between 0.0 and 1.0."""
        raw = os.getenv(var_name, str(default))
        try:
            value = float(raw)
        except ValueError as exc:
            raise ValueError(
                f"{var_name} must be a float between 0.0 and 1.0, got {raw!r}"
            ) from exc

        if not (0.0 <= value <= 1.0):
            raise ValueError(f"{var_name} must be between 0.0 and 1.0, got {value}")

        return value