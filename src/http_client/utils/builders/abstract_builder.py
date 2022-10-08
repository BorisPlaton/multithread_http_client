from exceptions.client_exceptions import ValidationException


class AbstractBuilder:
    """
    The abstract builder of the instance of specific class.
    Calls type checks and additional validators before the
    instance of class is created.
    """

    instance_class: type = None

    @classmethod
    def construct(cls):
        """
        Creates the instance of defined class. You must set
        corresponding attributes in the `configure_instance` method
        if it is needed.
        """
        builder = cls()
        builder.configure_instance()
        return builder.build()

    def configure_instance(self):
        """Override it if an instance must have defined attributes."""

    def build(self):
        """Builds the instance of `instance_class` type."""
        self.enforce_checks()
        return self.instance_class(**self._get_instance_attrs_values())

    def enforce_checks(self):
        """
        Calls before an instance initialization. Checks if builder's
        attributes have correct types and may call additional validations
        if they are defined.
        """
        for attr_name, attr_type in self._get_instance_attrs_annotations().items():
            attr_value = getattr(self, attr_name, None)
            self._check_attr_type(attr_name, attr_type, attr_value)
            self._call_additional_validation(attr_name, attr_value)

    def _check_attr_type(self, attr_name: str, attr_type: type, attr_value):
        """Checks a given attribute is a correct type. Otherwise, raises an exception."""
        try:
            if not isinstance(attr_value, attr_type):
                raise ValidationException(
                    f"`{self.__class__.__name__}().{attr_name}` equals `{attr_value}` "
                    f"and is `{type(attr_value).__name__}` type"
                    f" which is not a defined `{attr_type}` type."
                )
        except TypeError:
            pass

    def _call_additional_validation(self, attr_name: str, attr_value):
        """Calls an additional validation method if it is defined in builder's class body."""
        additional_validation_method = getattr(self, 'validate_' + attr_name, None)
        if attr_name != 'instance_class' and additional_validation_method:
            additional_validation_method(attr_value)

    def _get_instance_attrs_values(self):
        """
        Returns all builder's attributes that will be passed
        before an instance initialization.
        """
        return {
            attr: getattr(self, attr)
            for attr, value in vars(self).items()
        }

    def _get_instance_attrs_annotations(self):
        """Returns annotations for instance's attributes."""
        return {
            attr_name: attr_type
            for attr_name, attr_type in self.__class__.__annotations__.items()
        }

    def __setattr__(self, key, value):
        """Checks if a correct attribute assignment is performed."""
        if key not in self.__class__.__annotations__:
            raise AttributeError(f"`{key}` is not a builder instance attribute.")
        super().__setattr__(key, value)
