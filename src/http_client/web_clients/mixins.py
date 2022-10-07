from multidict import CIMultiDictProxy
from requests.structures import CaseInsensitiveDict


LikeDict = dict | CIMultiDictProxy | CaseInsensitiveDict


class ResponseValidator:
    """Performs a validation action."""

    response_validators = []

    @classmethod
    def validate_response(cls, response_headers: LikeDict, response_status_code: int):
        """
        Validates a received response via already defined validators
        in the class.
        """
        for validator in cls.response_validators:
            validator(response_status_code, response_headers)
