from ..conversion import check_conversion


def test_empty_schema():
    check_conversion(
        schema_in={},
        accepted_targets=(
            None,
            '',
            False,
            42,
            1.5,
            "I'm a string",
            {},
            [],
            {"an": ["arbitrarily", "nested"], "data": "structure"},
        ),
        unaccepted_targets=(),
    )


def test_type_object_schema():
    check_conversion(
        schema_in={'type': 'object'},
        accepted_targets=(
            {},
            {'a': 1},
            {'a': {'a': {'a': 1}}},
            {'a': [{'a': {'a': 1}}]},
            # Using non-string keys is invalid JSON. Technically, this
            # shouldn't validate. But we match the behavior of jsonschema.
            {1: 1},
        ),
        unaccepted_targets=(
            None,
            [],
            ['wumbo'],
            [{"wumbo": 'abc'}],
            1,
            '',
            1.5,
            True,
        ),
    )


def test_type_object_with_properties():
    check_conversion(
        schema_in={
            'type': 'object', 'properties': {
                'a-string': {'type': 'string'},
                'an-integer': {'type': 'integer'},
            }
        },
        accepted_targets=(
            {},
            {'a-string': 'a'},
            {'an-integer': 1},
            {'a-string': '', 'an-integer': 0},
            {'a-string': 'a', 'an-integer': 123},
            {'extra-key': 1},
            {'a-string': 'abc', 'extra-key': 1},
            {'a-string': 'abc', 'an-integer': 1234, 'extra-key': 1},
        ),
        unaccepted_targets=(
            {'a-string': {}},
            {'a-string': 1},
            {'a-string': 'a', 'an-integer': 'adsf'},
            {'a-string': 'a', 'an-integer': 1.5},
            None,
            1,
            1.5,
            'abc',
            False,
        ),
    )


def test_type_object_with_additional_properties_false():
    check_conversion(
        schema_in={
            'type': 'object',
            'properties': {'a': {'type': 'null'}},
            'additionalProperties': False,
        },
        accepted_targets=(
            {},
            {'a': None},
        ),
        unaccepted_targets=(
            {'b': None},
            {'a': None, 'b': None},
            None,
            1,
            1.5,
            'abc',
            False,
        ),
    )


def test_type_object_with_additional_properties_schema():
    check_conversion(
        schema_in={
            'type': 'object',
            'properties': {'a': {'type': 'boolean'}},
            'additionalProperties': {'type': 'string'},
        },
        accepted_targets=(
            {},
            {'a': True},
            {'a': False},
            {'b': 'abc'},
            {'a': True, 'b': 'abc'},
            {'a': False, 'b': 'abc'},
            {'a': False, 'b': 'abc', 1: 'adf'},
        ),
        unaccepted_targets=(
            {'b': False},
            {'b': 1},
            {'b': 1.5},
            {'b': {'asdf': 'asdf'}},
            {'b': ['asdf']},
        ),
    )
