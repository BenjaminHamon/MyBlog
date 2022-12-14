from typing import Optional

import dateutil.parser


def render_date(value: Optional[str], format_spec: str) -> str:
    if value is None:
        return ""

    value_parsed = dateutil.parser.parse(value)
    return value_parsed.strftime(format_spec)


def render_text(value: Optional[str]) -> str:
    return value if value is not None else ""