from ..conversion import check_conversion


def test_type_number_schema():
    check_conversion(
        schema_in={'type': 'number'},
        accepted_targets=(
            -1,
            0,
            1,
            1.5,
            float('inf'),
            float('+inf'),
            float('-inf'),
            float('NaN'),
        ),
        unaccepted_targets=(
            '',
            'abc',
            None,
            {},
            [],
        ),
    )


def test_type_integer_schema():
    check_conversion(
        schema_in={'type': 'integer'},
        accepted_targets=(
            -1,
            0,
            1,
            11234567890,
            10**100,
        ),
        unaccepted_targets=(
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
        ),
    )


def test_integer_multiple_of_schema():
    check_conversion(
        schema_in={'type': 'integer', 'multipleOf': 2},
        accepted_targets=(
            -10,
            -4,
            0,
            2,
            8,
        ),
        unaccepted_targets=(
            -9,
            -1,
            1,
            3,
            11,
            '',
            '2',
            [],
            {},
            [2],
        ),
    )


def test_number_multiple_of_schema():
    check_conversion(
        schema_in={'type': 'number', 'multipleOf': 1.1},
        accepted_targets=(
            -4.4,
            -2.2,
            -1.1,
            0,
            1.1,
            2.2,
            4.4,
        ),
        unaccepted_targets=(
            # 3.3 fails due to floating point errors. we're matching behavior
            # of jsonschema here (no approximate float comparisons)
            -3.3,
            3.3,
            1.100001,
            1.10001,
            1.0999,
            2.20001,
            2.19999,
            1,
            2,
            [],
            None,
        ),
    )


def test_number_minimum_schema():
    check_conversion(
        schema_in={'type': 'number', 'minimum': 1},
        accepted_targets=(1, 2, 2.5, 3, 4, 10, 100, 5**100),
        unaccepted_targets=(0.999, 0, -1, -2, -10, -100, None, [], {}, ''),
    )


def test_number_exclusive_minimum_schema():
    check_conversion(
        schema_in={'type': 'number', 'minimum': 2.1, 'exclusiveMinimum': True},
        accepted_targets=(2.1001, 3, 4, 5.5, 10**100),
        unaccepted_targets=(2.1, 1, 0.5, 0, -1.5, None, [], {}, ''),
    )


def test_number_maximum_schema():
    check_conversion(
        schema_in={'type': 'number', 'maximum': 300},
        accepted_targets=(300, 299.9999, 200, 0, -100, -300),
        unaccepted_targets=(300.0001, 301, 302, 99999, None, [], {}, ''),
    )


def test_number_exclusive_maximum_schema():
    check_conversion(
        schema_in={'type': 'number', 'maximum': 300, 'exclusiveMaximum': True},
        accepted_targets=(299.9999, 200, 0, -100, -300),
        unaccepted_targets=(300, 300.0001, 301, 302, 99999, None, [], {}, ''),
    )


def test_integer_with_maximum_and_minimum():
    check_conversion(
        schema_in={'type': 'integer', 'minimum': -1, 'maximum': 1},
        accepted_targets=(-1, 0, 1),
        unaccepted_targets=(-2, -1.1, -0.5, 0.5, 1.1, 2, None, [], {}, ''),
    )


def test_integer_with_exclusive_maximum_and_exclusive_minimum():
    check_conversion(
        schema_in={
            'type': 'integer',
            'minimum': -1,
            'maximum': 1,
            'exclusiveMinimum': True,
            'exclusiveMaximum': True,
        },
        accepted_targets=(0, ),
        unaccepted_targets=(-2, -1.1, -0.5, 0.5, 1.1, 2, None, [], {}, ''),
    )


def test_integer_with_maximum_less_than_minimum():
    check_conversion(
        schema_in={'type': 'integer', 'minimum': 1, 'maximum': -1},
        accepted_targets=(),
        unaccepted_targets=(
            -2, -1.1, -1, -0.5, 0, 0.5, 1, 1.1, 2, None, [], {}, ''
        ),
    )


def test_number_with_exclusive_minimum_true_but_no_minimum_value():
    # the exclusiveMaximum should be ignored if there is no minimum
    check_conversion(
        schema_in={'type': 'number', 'exclusiveMinimum': True},
        accepted_targets=(1, 2.2, 3, 4.4, -1.1, -2, -3.3, -4),
        unaccepted_targets=(None, [], {}, '', '1', '0', '1.1'),
    )
