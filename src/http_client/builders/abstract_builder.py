class AbstractBuilder:
    """
    The abstract builder of the instance of specific class.
    Calls type checks and additional validators before the
    instance of class is created.
    """

    instance_class: type = None

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
        for attr_name, attr_type in self._get_instance_attrs_annotations():
            attr_value = getattr(self, attr_name, None)
            if not isinstance(attr_value, attr_type):
                raise TypeError(
                    f"`{self.__class__}.{attr_name}` equals `{attr_value}` which is not a `{attr_type}` type."
                )
            if (
                    attr_name != 'instance_class' and
                    (validate_property_method := getattr(self, 'validate_' + attr_name, None))
            ):
                validate_property_method(attr_value)

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
            if attr_name != 'instance_class'
        }
