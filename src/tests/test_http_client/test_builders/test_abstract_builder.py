import pytest

from http_client.builders.abstract_builder import AbstractBuilder


@pytest.mark.http_client
class TestAbstractBuilder:

    @pytest.fixture
    def abs_builder(self):
        yield AbstractBuilder
        AbstractBuilder.instance_class = None

    def test_building_class_without_args(self, abs_builder):
        class A:

            def __init__(self):
                pass

        abs_builder.instance_class = A
        assert isinstance(abs_builder().build(), A)
