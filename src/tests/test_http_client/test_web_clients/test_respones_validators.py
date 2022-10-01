import pytest

from exceptions.client_exceptions import ValidationException
from http_client.web_clients.response_validators import status_code_validation, accept_ranges_validation, \
    content_length_validation


@pytest.mark.http_client
class TestResponseValidators:

    @pytest.fixture
    def headers(self):
        return {'Accept-Ranges': 'bytes', 'Content-Length': 200}

    def test_status_code_validator_passes_code_in_range_from_200_to_299(self, headers):
        for status_code in range(200, 300):
            assert not status_code_validation(status_code, headers)

    def test_status_code_validator_not_pass_code_not_in_range_from_200_to_299(self, headers):
        with pytest.raises(ValidationException):
            assert not status_code_validation(199, headers)
        with pytest.raises(ValidationException):
            assert not status_code_validation(300, headers)
        with pytest.raises(ValidationException):
            assert not status_code_validation(301, headers)
        with pytest.raises(ValidationException):
            assert not status_code_validation(0, headers)

    def test_accept_ranges_validation_passes_with_accept_ranges_headers(self, headers):
        assert not accept_ranges_validation(200, headers)

    def test_accept_ranges_validation_not_passes_with_wrong_accept_ranges_headers(self, headers):
        headers.update({'Accept-Ranges': None})
        with pytest.raises(ValidationException):
            assert accept_ranges_validation(200, headers)
        headers.update({'Accept-Ranges': 'byte'})
        with pytest.raises(ValidationException):
            assert accept_ranges_validation(200, headers)
        headers.pop('Accept-Ranges')
        with pytest.raises(ValidationException):
            assert accept_ranges_validation(200, headers)

    def test_content_length_validation_passes_with_content_length_header(self, headers):
        assert not content_length_validation(200, headers)

    def test_content_length_validation_not_passes_with_wrong_content_length_header(self, headers):
        headers.update({'Content-Length': None})
        with pytest.raises(ValidationException):
            assert content_length_validation(200, headers)
        headers.update({'Content-Length': 0})
        with pytest.raises(ValidationException):
            assert content_length_validation(200, headers)
        headers.pop('Content-Length')
        with pytest.raises(ValidationException):
            assert content_length_validation(200, headers)
