from dataclasses import dataclass


@dataclass
class URLResourceData:
    """Stores all necessary information about an url resource."""
    url: str
    summary_length: int
    encoding_type: str
