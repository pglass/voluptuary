from voluptuous import Schema, All, Any, Length

from voluptuary import to_string


def check(schema, expected):
    actual = to_string(schema)
    msg = (
        "Schema to_string did not match\n"
        "schema   = %r\n"
        "actual   = %s\n"
        "expected = %s" % (schema, actual, expected)
    )
    assert actual == expected, msg


def test_primitive_schema_to_string():
    check(Schema(dict), 'Schema(dict)')
    check(Schema(str), 'Schema(str)')
    check(Schema(int), 'Schema(int)')
    check(Schema(float), 'Schema(float)')
    check(Schema({}), 'Schema({})')
    check(Schema([]), 'Schema([])')


def test_list_to_string():
    check(Schema([float]), 'Schema([float])')
    check(Schema([float, int]), 'Schema([float, int])')
    check(Schema([Schema(int)]), 'Schema([Schema(int)])')
    check(
        Schema([Schema(int), float, Schema({})]),
        'Schema([Schema(int), float, Schema({})])',
    )


def test_dict_to_string():
    check(Schema({}), 'Schema({})')
    check(Schema({'a': 1}), "Schema({'a': 1})")
    check(
        Schema({'a': 1, 'b': [{'c': str}]}),
        "Schema({'a': 1, 'b': [{'c': str}]})",
    )


def test_any_and_all_to_string():
    check(Any(), 'Any()')
    check(Any(int, str), 'Any(int, str)')
    check(All(), 'All()')
    check(All(int, str), 'All(int, str)')
    check(Any(Schema(int), Schema(str)), 'Any(Schema(int), Schema(str))')
    check(All(Schema(int), Schema(str)), 'All(Schema(int), Schema(str))')
    check(
        Any(All(str, Length(min=1)), All(list, Length(max=2))),
        'Any(All(str, Length(min=1, max=None)), All(list, Length(min=None, max=2)))',
    )
