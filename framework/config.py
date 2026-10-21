"""Acceso centralizado a la configuración de ejecución.

Orden de resolución de cada clave (gana el primer valor no vacío):
  1. Valor de la línea de comandos de pytest (--browser, --headless), registrado con ``set_override``
  2. Variable de entorno en mayúsculas, con guiones bajos en vez de puntos, p. ej. ``SAUCEDEMO_PASSWORD``
  3. ``config.ini`` en la raíz del proyecto

Así CI puede inyectar secretos y sobrescribir valores sin tocar archivos versionados.
"""

import configparser
import os
from pathlib import Path

from framework.browser import Browser

_CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.ini"
_SECTION = "settings"
_overrides: dict[str, str] = {}


def _load() -> configparser.SectionProxy:
    # interpolation=None para que los valores puedan contener '%' de forma literal
    parser = configparser.ConfigParser(interpolation=None)
    if not parser.read(_CONFIG_FILE, encoding="utf-8"):
        raise FileNotFoundError(f"{_CONFIG_FILE} not found")
    return parser[_SECTION]


_FILE_VALUES = _load()


def set_override(key: str, value: str) -> None:
    _overrides[key] = value


def get(key: str) -> str:
    override = _overrides.get(key)
    if override and override.strip():
        return override.strip()
    env_value = os.environ.get(key.upper().replace(".", "_"))
    if env_value and env_value.strip():
        return env_value.strip()
    file_value = _FILE_VALUES.get(key)
    if not file_value or not file_value.strip():
        raise KeyError(f"Missing configuration value for key '{key}'")
    return file_value.strip()


def get_int(key: str) -> int:
    return int(get(key))


def get_bool(key: str) -> bool:
    return get(key).lower() in ("true", "1", "yes")


def browser() -> Browser:
    return Browser.from_name(get("browser"))


def headless() -> bool:
    return get_bool("headless")


def timeout() -> int:
    return get_int("timeout.seconds")
