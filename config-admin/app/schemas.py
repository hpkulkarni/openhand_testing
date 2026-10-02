"""Request models and value validation."""
import json
from typing import Literal

from pydantic import BaseModel, Field


class LoginIn(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class ConfigIn(BaseModel):
    key: str = Field(min_length=1, max_length=100, pattern=r"^[a-z0-9_.-]+$")
    value: str
    value_type: Literal["string", "int", "bool", "json"]
    environment: Literal["dev", "staging", "prod"]
    description: str = Field(default="", max_length=500)


def validate_value(value: str, value_type: str) -> str | None:
    """Return an error message if `value` does not fit `value_type`, else None."""
    if value_type == "int":
        try:
            int(value)
        except ValueError:
            return "value must be an integer"
    elif value_type == "bool":
        if value not in ("true", "false"):
            return "value must be 'true' or 'false'"
    elif value_type == "json":
        try:
            json.loads(value)
        except ValueError:
            return "value must be valid JSON"
    return None
