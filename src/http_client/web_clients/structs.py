from typing import NamedTuple


class URLResourceData(NamedTuple):
    """Stores all necessary information about an url resource."""
    url: str
    summary_length: int
    encoding_type: str
