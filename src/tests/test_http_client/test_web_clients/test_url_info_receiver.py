from unittest import mock

import pytest
from multidict import CIMultiDictProxy

from exceptions.base import ApplicationException
from http_client.web_clients.url_info import URLInfoReceiver, HeaderData


@pytest.mark.http_client
class TestURLInfoReceiver:

    @pytest.fixture
    def info_receiver(self):
        return URLInfoReceiver()

    @mock.patch('http_client.web_clients.url_info.URLInfoReceiver.headers_to_return')
    def test_all_necessary_resource_headers_values_returned(self, headers_mock, info_receiver):
        headers_to_return = {
            'content_length': HeaderData('Content-Length', int),
            'accept_ranges': HeaderData('Accept-Ranges', str),
        }
        resource_headers = {
            'Content-Length': '200',
            'Accept-Ranges': 'bytes',
        }
        headers_mock.__getitem__.side_effect = headers_to_return.__getitem__
        headers_mock.items.side_effect = headers_to_return.items

        returned_headers_values = info_receiver._get_resource_necessary_headers_values(resource_headers)
        assert returned_headers_values['content_length'] == 200
        assert returned_headers_values['accept_ranges'] == 'bytes'

    @mock.patch('http_client.web_clients.url_info.URLInfoReceiver.headers_to_return')
    def test_exception_raised_if_cannot_construct_headers_values(self, headers_mock, info_receiver):
        headers_to_return = {
            'content_length': HeaderData('Content-Length', int),
            'accept_ranges': HeaderData('Accept-Ranges', str),
        }
        resource_headers = {
            'Content-Length': 'not integer',
            'Accept-Ranges': 'bytes',
        }
        headers_mock.__getitem__.side_effect = headers_to_return.__getitem__
        headers_mock.items.side_effect = headers_to_return.items
        with pytest.raises(ApplicationException):
            info_receiver._get_resource_necessary_headers_values(resource_headers)
        resource_headers.pop('Content-Length')
        with pytest.raises(ApplicationException):
            info_receiver._get_resource_necessary_headers_values(resource_headers)

    @mock.patch('http_client.web_clients.url_info.URLInfoReceiver.response_validators')
    def test_all_validators_executed(self, validators_list, info_receiver):
        results_list = []

        def fake_validator(status_code, headers):
            results_list.append('fake_validator is executed')

        validators_list.__iter__.side_effect = [fake_validator, fake_validator].__iter__
        info_receiver._validate_response({}, 200)
        assert len(results_list) == 2

    @pytest.mark.web
    @pytest.mark.asyncio
    async def test_url_headers_and_status_are_returned_values(self, info_receiver):
        headers, status_code = await info_receiver._get_url_info('https://google.com')
        assert isinstance(headers, CIMultiDictProxy)
        assert isinstance(status_code, int)
