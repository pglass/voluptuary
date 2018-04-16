from voluptuary import to_voluptuous
from .conversion import check_jsonschema_validation
from .conversion import check_voluptuous_validation


def test_type_string_schema():
    schema_in = {'type': 'string'}
    schema_out = to_voluptuous(schema_in)
    for target in (
        "",
        "a",
        "123",
        "0",
        "asdfadsfasdfasdfdsf",
        "Déjà vu",
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        1,
        None,
        False,
        {},
        [],
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_boolean_schema():
    schema_in = {'type': 'boolean'}
    schema_out = to_voluptuous(schema_in)
    for target in (
        False,
        True,
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        "true",
        "false",
        0,
        1,
        '',
        'abc',
        None,
        {},
        [],
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_null_schema():
    schema_in = {'type': 'null'}
    schema_out = to_voluptuous(schema_in)
    for target in (None, ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        {},
        [],
        '',
        0,
        False,
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_list_of_types_schema():
    schema_in = {'type': ['number', 'string']}
    schema_out = to_voluptuous(schema_in)
    for target in (
        -1,
        -0,
        0,
        1,
        1.5,
        float('inf'),
        float('+inf'),
        float('-inf'),
        float('NaN'),
        "",
        "a",
        "123",
        "0",
        "asdfadsfasdfasdfdsf",
        "Déjà vu",
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        None,
        {},
        [],
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_array_schema():
    schema_in = {'type': 'array'}
    schema_out = to_voluptuous(schema_in)
    for target in (
        [],
        [1],
        [[]],
        [1, 2, 3],
        ['a', 1, None],
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        {},
        None,
        1,
        'asd',
        1.5,
        False,
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_array_schema_with_items():
    schema_in = {
        'type': 'array',
        'items': {
            'type': 'boolean',
        },
    }
    schema_out = to_voluptuous(schema_in)

    for target in (
        [],
        [False],
        [True],
        [False, False, False],
        [False, True, False, True],
        [True, True, True],
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        [False, 1],
        [False, False, False, False, 'a', False],
        [1],
        [1.5],
        ['abc'],
        [[]],
        [[False]],
        {},
        False,
        True,
        0,
        3.14,
        'abc',

        # note: jsonschema will not validate python tuples as arrays, while
        # voluptuous will. I did not see an obvious way to enforce this,
        # but JSON arrays are typically lists anyway.
        # tuple(),
        # (False,),
        # (True,),
        # (False, False, False),
        # (True, True, True),
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_array_schema_with_items_list():
    # This form validates an _ordered_ array. The n-th schema in `items` must
    # validate the n-th element in the target being validated.
    #
    # However, it is also valid to have extra items at the end of the array.
    schema_in = {
        'type': 'array',
        'items': [{'type': 'number'}, {'type': 'string'}],
    }
    schema_out = to_voluptuous(schema_in)

    for target in (
        [],
        [1],
        [1.5],
        [1, 'abc'],
        [1, 'abc', 'abc'],
        [1.5, 'abc', 1],
        [1, 'abc', {}],
        [1, 'abc', []],
        [1, 'abc', False, None, {}, 'asdf'],
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        ['abc'],
        ['abc', 1],
        [1, 1],
        [[]],
        [{}],
        [None],
        ['abc'],
        [[False]],
        {},
        False,
        True,
        0,
        3.14,
        'abc',
        tuple(),
        (1, ),
        (1.5, ),
        (1, 'abc'),
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_array_with_items_list_and_additional_items_false():
    schema_in = {
        'type': 'array',
        'items': [{'type': 'boolean'}, {'type': 'integer'}],
        'additionalItems': False,
    }
    schema_out = to_voluptuous(schema_in)

    for target in (
        [],
        [True],
        [False],
        [True, 1],
        [False, 2],
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        [True, 1, 2],
        [True, 3, True],
        [True, 5, False],
        [True, 5, []],
        [True, 5, 'a', 'b', 'c'],
        [True, 5, 1, 2, 3],
        1,
        'a',
        None,
        False,
        {},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_array_with_min_and_max_items():
    schema_in = {
        'type': 'array',
        'items': {'type': 'integer'},
        'minItems': 2,
        'maxItems': 5,
    }
    schema_out = to_voluptuous(schema_in)

    for target in (
        [1, 2],
        [1, 2, 3],
        [1, 2, 3, 4],
        [1, 2, 3, 4, 5],
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        [],
        [1],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 'a'],
        [1, 2, 'b'],
        [1, 2, 'c', 4],
        [1, 'd', 3, 4, 5],
        1,
        'a',
        None,
        False,
        {},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_array_with_min_and_max_items_and_items_list():
    schema_in = {
        'type': 'array',
        'items': [
            {'type': 'integer'}, {'type': 'string'}, {'type': 'boolean'}
        ],
        'minItems': 1,
        'maxItems': 4,
    }
    schema_out = to_voluptuous(schema_in)

    for target in (
        [1],
        [2, 'a'],
        [3, '', True],
        [0, 'b', False, 0],
        [-1, 'abc', True, 'b'],
        [-2, 'Déjà vu', False, {'a': 1}],
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        [],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 2, 'b'],
        [1, 2, 'c', 4],
        [1, 'd', 3, 4, 5],
        1,
        'a',
        'aasdfadf',
        None,
        False,
        {},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_schema_with_any_of():
    schema_in = {'anyOf': [
        {'type': 'string'},
        {'type': 'integer'},
    ]}
    schema_out = to_voluptuous(schema_in)

    for target in (
        'a',
        1,
        'abdc',
        1234,
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        [],
        [1],
        ['a'],
        None,
        {},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_schema_with_all_of():
    schema_in = {'allOf': [
        {'type': 'string'},
        {'maxLength': 5},
    ]}
    schema_out = to_voluptuous(schema_in)

    for target in (
        '',
        'a',
        'ab',
        'abcde',
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        'abcdef',
        'abcdefg',
        1234,
        12345,
        [],
        [1],
        ['a'],
        None,
        {},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)
