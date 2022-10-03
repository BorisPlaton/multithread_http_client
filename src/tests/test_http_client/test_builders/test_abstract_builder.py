import pytest

from exceptions.client_exceptions import ValidationException
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

    def test_validation_without_variables_assignment(self, abs_builder):
        class A:
            def __init__(self, one, two):
                pass

        class ABuilder(abs_builder):
            instance_class = A
            one: int
            two: str

        with pytest.raises(ValidationException):
            ABuilder().build()

    def test_instance_building_with_variables_assignment(self, abs_builder):
        class A:
            def __init__(self, one, two):
                self.one = one
                self.two = two

        class ABuilder(abs_builder):
            instance_class = A
            one: int
            two: str

        builder = ABuilder()
        builder.one = 1
        builder.two = '2'
        built_instance = builder.build()
        assert isinstance(built_instance, A)
        assert built_instance.one == 1
        assert built_instance.two == '2'

    def test_instance_building_with_optional_variables(self, abs_builder):
        class A:
            def __init__(self, one, two=None):
                self.one = one
                self.two = two

        class ABuilder(abs_builder):
            instance_class = A
            one: int
            two: None | str

        builder = ABuilder()
        builder.one = 1
        built_instance = builder.build()
        assert isinstance(built_instance, A)
        assert built_instance.one == 1
        assert built_instance.two is None

        second_builder = ABuilder()
        second_builder.one = 2
        second_builder.two = '22'
        second_built_instance = second_builder.build()
        assert isinstance(second_built_instance, A)
        assert second_built_instance.one == 2
        assert second_built_instance.two == '22'

    def test_additional_validation_during_instance_building(self, abs_builder):
        class A:
            def __init__(self, one, two=None):
                self.one = one
                self.two = two

        class ABuilder(abs_builder):
            instance_class = A
            one: int
            two: str

            def validate_two(self, value, value_type):
                if value != '2':
                    raise ValidationException

        builder = ABuilder()
        builder.one = 1
        builder.two = 'not 2'
        with pytest.raises(ValidationException):
            builder.build()
        builder.two = '2'
        built_instance = builder.build()
        assert isinstance(built_instance, A)
        assert built_instance.one == 1
        assert built_instance.two == '2'

    def test_not_defined_fields_cant_be_created(self, abs_builder):
        class A:
            def __init__(self, one):
                pass

        class ABuilder(abs_builder):
            instance_class = A
            one: int

        builder = ABuilder()
        with pytest.raises(AttributeError):
            builder.two = 2
        builder.one = 1
        assert builder.one == 1
