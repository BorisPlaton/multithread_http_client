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
