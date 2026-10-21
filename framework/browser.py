from enum import Enum


class Browser(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    EDGE = "edge"

    @classmethod
    def from_name(cls, name: str) -> "Browser":
        try:
            return cls(name.strip().lower())
        except ValueError:
            supported = ", ".join(b.value for b in cls)
            raise ValueError(f"Unsupported browser '{name}'. Use one of: {supported}") from None
