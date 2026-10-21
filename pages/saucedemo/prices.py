import re
from decimal import Decimal

_AMOUNT = re.compile(r"\$(\d+(?:\.\d{2})?)")


def parse_price(label: str) -> Decimal:
    """Interpreta etiquetas de importe como "$29.99" o "Item total: $39.98"."""
    match = _AMOUNT.search(label)
    if not match:
        raise ValueError(f"No price found in '{label}'")
    return Decimal(match.group(1))
