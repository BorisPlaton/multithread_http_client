from exceptions.client_exceptions import ValidationException


def status_code_validation(status_code: int, headers: dict):
    """Validates that a status code is in the range from 200 to 299."""
    if status_code not in range(200, 300):
        raise ValidationException(
            f"The response's status code is {status_code}. Expected from 200 to 299."
        )


def accept_ranges_validation(status_code: int, headers: dict):
    """Validates a response has a `Accept-Ranges` header."""
    if headers.get("Accept-Ranges") != 'bytes':
        raise ValidationException(
            "The remote server doesn't support an `Accept-Ranges` header."
        )


def content_length_validation(status_code: int, headers: dict):
    """Validates a response has a `Content-Length` header."""
    if headers.get("Content-Length") is None:
        raise ValidationException(
            "The remote server didn't send a `Content-Length` header."
        )
    elif headers.get("Content-Length") == 0:
        raise ValidationException(
            "The remote server doesn't have a content of the requested page."
        )


def content_encoding_validation(status_code: int, headers: dict):
    """Validates a response has a valid `Content-Encoding` header."""
    available_accept_encodings = ['gzip', 'deflate']
    if headers.get("Content-Encoding") is None:
        raise ValidationException(
            "The remote server didn't send the `Content-Encoding` header."
        )
    elif content_encoding := headers.get("Content-Encoding") not in available_accept_encodings:
        raise ValidationException(
            f"The remote server sends an unacceptable encoding `{content_encoding}` when only"
            f" `{'`, `'.join(available_accept_encodings)}` are available."
        )
