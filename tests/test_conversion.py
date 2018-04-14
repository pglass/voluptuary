import voluptuous
import jsonschema

from voluptuary import to_voluptuous, to_string


def check_jsonschema_validation(schema, target, should_validate):
    return check_validation(
        'jsonschema.Draft4Validator',
        jsonschema.Draft4Validator(schema).validate,
        jsonschema.ValidationError,
        schema,
        target,
        should_validate,
    )


def check_voluptuous_validation(schema, target, should_validate):
    return check_validation(
        'voluptuous.Schema',
        voluptuous.Schema(schema),
        voluptuous.Invalid,
        schema,
        target,
        should_validate,
    )


def check_validation(
    validator_name, validator, validator_exception, schema, target,
    should_validate
):
    try:
        validator(target)
    except validator_exception as e:
        if should_validate:
            msg = (
                'Schema failed to validate target:\nvalidator=%s\n'
                'schema=%r\nschema-str=%s\ntarget=%s' %
                (validator_name, schema, to_string(schema), target)
            )
            raise Exception("%s\nerror: %s" % (msg, e))
    else:
        if not should_validate:
            msg = (
                'Schema erroneously validated the target, but should not '
                'have validated:\n'
                'validator  = %s\n'
                'schema     = %r\n'
                'schema-str = %s\n'
                'target     = %s' %
                (validator_name, schema, to_string(schema), target)
            )
            raise Exception(msg)


def test_empty_schema():
    schema_in = {}
    schema_out = to_voluptuous(schema_in)
    for target in (
        None,
        '',
        False,
        42,
        "I'm a string",
        {},
        [],
        {"an": ["arbitrarily", "nested"], "data": "structure"},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)


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


def test_type_integer_schema():
    schema_in = {'type': 'integer'}
    schema_out = to_voluptuous(schema_in)
    for target in (
        -1,
        0,
        1,
        11234567890,
        10**100,
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    # note: bool is a subclass of int in python, so False and True will
    # validate.
    for target in (
        '',
        'abc',
        None,
        {},
        [],
        1.0,
        1.5,
        float('inf'),
        float('+inf'),
        float('-inf'),
        float('NaN'),
        "123",
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_number_schema():
    schema_in = {'type': 'number'}
    schema_out = to_voluptuous(schema_in)
    for target in (
        -1,
        0,
        1,
        1.5,
        float('inf'),
        float('+inf'),
        float('-inf'),
        float('NaN'),
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    # note: bool is a subclass of int in python, so False and True will
    # validate.
    for target in (
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


def test_type_string_or_number_schema():
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


def test_type_object_schema():
    schema_in = {'type': 'object'}
    schema_out = to_voluptuous(schema_in)

    for target in (
        {},
        {'a': 1},
        {'a': {'a': {'a': 1}}},
        {'a': [{'a': {'a': 1}}]},
        # Using non-string keys is invalid JSON. Technically, this shouldn't
        # validate. However, we match the behavior of `jsonschema`.
        {1: 1},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        None,
        [],
        ['wumbo'],
        [{"wumbo": 'abc'}],
        1,
        '',
        1.5,
        True,
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_object_with_properties():
    schema_in = {
        'type': 'object', 'properties': {
            'a-string': {'type': 'string'},
            'an-integer': {'type': 'integer'},
        }
    }
    schema_out = to_voluptuous(schema_in)

    for target in (
        {},
        {'a-string': 'a'},
        {'an-integer': 1},
        {'a-string': '', 'an-integer': 0},
        {'a-string': 'a', 'an-integer': 123},
        {'extra-key': 1},
        {'a-string': 'abc', 'extra-key': 1},
        {'a-string': 'abc', 'an-integer': 1234, 'extra-key': 1},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        {'a-string': {}},
        {'a-string': 1},
        {'a-string': 'a', 'an-integer': 'adsf'},
        {'a-string': 'a', 'an-integer': 1.5},
        None,
        1,
        1.5,
        'abc',
        False,
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_object_with_additional_properties_false():
    schema_in = {
        'type': 'object',
        'properties': {'a': {'type': 'null'}},
        'additionalProperties': False,
    }
    schema_out = to_voluptuous(schema_in)

    for target in (
        {},
        {'a': None},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        {'b': None},
        {'a': None, 'b': None},
        None,
        1,
        1.5,
        'abc',
        False,
    ):
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


def test_type_object_with_additional_properties_schema():
    schema_in = {
        'type': 'object',
        'properties': {'a': {'type': 'boolean'}},
        'additionalProperties': {'type': 'string'},
    }
    schema_out = to_voluptuous(schema_in)
    print(schema_out)

    works = voluptuous.Schema(
        {
            'a': voluptuous.Schema(bool),
            voluptuous.Extra: voluptuous.Schema(str),
        }
    )
    print(works)

    for target in (
        {},
        {'a': True},
        {'a': False},
        {'b': 'abc'},
        {'a': True, 'b': 'abc'},
        {'a': False, 'b': 'abc'},
        {'a': False, 'b': 'abc', 1: 'adf'},
    ):
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)

    for target in (
        {'b': False},
        {'b': 1},
        {'b': 1.5},
        {'b': {'asdf': 'asdf'}},
        {'b': ['asdf']},
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
