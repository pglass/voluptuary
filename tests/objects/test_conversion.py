import pytest

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


def test_type_object_with_min_and_max_properties():
    check_conversion(
        schema_in={
            'type': 'object',
            'minProperties': 2,
            'maxProperties': 4,
        },
        accepted_targets=(
            {'a': 1, 'b': 2},
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 1, 'b': 2, 'c': 3, 'd': 4},
            {'a': {}, 'b': {}},
            {'a': {'': ''}, 'b': {'': ''}},
        ),
        unaccepted_targets=(
            {},
            {'a': 1},
            {'b': 2},
            {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5},
            [],
            [1],
            [1, 2],
            [1, 2, 3],
            False,
            None,
            0,
            'abc',
        ),
    )


def test_type_object_with_min_properties():
    check_conversion(
        schema_in={
            'type': 'object',
            'minProperties': 2,
        },
        accepted_targets=(
            {'a': 1, 'b': 2},
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6},
        ),
        unaccepted_targets=(
            {},
            {'a': 1},
            {'b': 2},
            [],
            [1],
            [1, 2],
            [1, 2, 3],
            False,
            None,
            0,
            'abc',
        ),
    )


def test_type_object_with_max_properties():
    check_conversion(
        schema_in={
            'type': 'object',
            'maxProperties': 2,
        },
        accepted_targets=(
            {},
            {'a': 1},
            {'b': 2},
            {'a': 1, 'b': 2},
        ),
        unaccepted_targets=(
            {'a': 1, 'b': 2, 'c': 3},
            {'a': 1, 'b': 2, 'c': 3, 'd': 4},
            {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5},
            {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6},
            [],
            [1],
            [1, 2],
            [1, 2, 3],
            False,
            None,
            0,
            'abc',
        ),
    )


def test_object_with_required_properties():
    check_conversion(
        schema_in={
            'type': 'object',
            'required': ['name', 'id'],
        },
        accepted_targets=(
            {'name': 'spongebob', 'id': 1234},
            {'name': 'spongebob', 'id': 1234, 'extra': 'abc'},
            {'name': 'spongebob', 'id': 1234, 'extra': {'thing': 1}},
            {'name': 'spongebob', 'id': 1234, 'extra': 'abc', 'extra2': False},
        ),
        unaccepted_targets=(
            {},
            {'id': 1234},
            {'name': 'spongebob'},
            {'extra': 'abc'},
            None,
            False,
            [],
            0,
            'abc',
        ),
    )


def test_object_with_properties_and_required_properties():
    # any fields mentioned in `required` must respect schemas for those fields
    # found in `properties`
    check_conversion(
        schema_in={
            'type': 'object',
            'required': ['name', 'id'],
            'properties': {
                'name': {'type': 'string'},
            },
        },
        accepted_targets=(
            {'name': '', 'id': None},
            {'name': 'spongebob', 'id': 1234},
            {'name': 'spongebob', 'id': False},
            {'name': 'spongebob', 'id': 1.23},
            {'name': 'spongebob', 'id': {"abc": "1234"}},
            {'name': 'spongebob', 'id': [1, {2: {3: 4}}, False, None]},
        ),
        unaccepted_targets=(
            {},
            {'name': 1, 'id': 2},
            {'name': None, 'id': 2},
            {'name': False, 'id': 2},
            {'name': 'spongebob'},
            {'id': 1},
            [],
            None,
            False,
            1,
            '',
        ),
    )


def test_object_with_properties_and_required_properties_and_additional_props():
    # any fields mentioned in `required` must respect schemas for those fields
    # found in both `properties` and `additionalProperties`
    #
    # In the following, `name` must be a string, while `id` must be a
    # non-negative integer (due to the additionalProperties schema)
    check_conversion(
        schema_in={
            'type': 'object', 'required': ['name', 'id'], 'properties': {
                'name': {'type': 'string'},
            }, 'additionalProperties': {
                'type': 'integer',
                'minimum': 0,
            }
        },
        accepted_targets=(
            {'name': '', 'id': 0},
            {'name': 'spongebob', 'id': 10},
        ),
        unaccepted_targets=(
            {},
            {'name': '', 'id': None},
            {'name': '', 'id': -1},
            {'name': '', 'id': 1.23},
            {'name': '', 'id': {"abc": "1234"}},
            {'name': '', 'id': [1, {2: {3: 4}}, False, None]},
            {'id': 1},
            [],
            None,
            False,
            1,
            '',
        ),
    )


@pytest.mark.skip(
    reason="Cannot express conflict between required properties "
    "and additionalProperties=False with voluptuous"
)
def test_object_with_unspecified_required_prop_and_no_additional_props():
    # What happens if a property is required, but is not mentioned in
    # `properties` and additional properties are not allowed?
    #
    # the `required` and `additionalProperties=False` conflict. The schema
    # will validate nothing.
    check_conversion(
        schema_in={
            'type': 'object',
            'required': ['name', 'id'],
            'properties': {
                'name': {'type': 'string'},
            },
            'additionalProperties': False,
        },
        # note: This accepts nothing. jsonschema errors on both,
        #
        # {'name': ''}          "id is required"
        # {'name': '', 'id': 1} "id unexpected" (additional props not allowed)
        #
        # I can't find a way to express this conflict with voluptuous.
        #
        # For the time being, we respect the required properties over
        # additionalProperties in the voluptuous result.
        accepted_targets=(),
        unaccepted_targets=(
            {},
            # {'name': ''},
            {'name': '', 'id': 1},
            {'name': '', 'id': 1},
        ),
    )
