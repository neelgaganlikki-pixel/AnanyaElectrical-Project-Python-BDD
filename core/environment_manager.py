import os
import yaml
from typing import Dict, Any

class EnvironmentManager:
    """Manages active environment configuration and safeguards execution."""
    _instance = None
    _config = None

    def __new__(cls, config_path: str = None):
        if cls._instance is None:
            cls._instance = super(EnvironmentManager, cls).__new__(cls)
            cls._instance._initialize(config_path)
        return cls._instance

    def _initialize(self, config_path: str = None):
        if not config_path:
            config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "config.yaml")
        
        with open(config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

        self._active_env = self._config.get("active_environment", "dev").lower()

    def set_environment(self, env_name: str):
        env_name = env_name.lower().strip()
        if env_name not in self._config["environments"]:
            raise ValueError(f"Invalid environment: '{env_name}'. Available: {list(self._config['environments'].keys())}")
        self._active_env = env_name

    @property
    def active_env(self) -> str:
        return self._active_env

    @property
    def base_url(self) -> str:
        return self._config["environments"][self._active_env]["base_url"]

    @property
    def env_name(self) -> str:
        return self._config["environments"][self._active_env].get("name", self._active_env)

    @property
    def allow_write_operations(self) -> bool:
        return self._config["environments"][self._active_env].get("allow_write_operations", False)

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    def validate_safety_guard(self, operation_name: str = "destructive"):
        """Prevents destructive or write operations in production."""
        if self._active_env == "production" and not self.allow_write_operations:
            raise PermissionError(
                f"SAFETY GUARD: Operation '{operation_name}' is blocked in PRODUCTION environment ({self.base_url})."
            )

