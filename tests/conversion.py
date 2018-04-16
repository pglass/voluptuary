import voluptuous
import jsonschema

from voluptuary import to_string, to_voluptuous


def check_conversion(schema_in, accepted_targets, unaccepted_targets):
    schema_out = to_voluptuous(schema_in)
    for target in accepted_targets:
        check_jsonschema_validation(schema_in, target, should_validate=True)
        check_voluptuous_validation(schema_out, target, should_validate=True)
    for target in unaccepted_targets:
        check_jsonschema_validation(schema_in, target, should_validate=False)
        check_voluptuous_validation(schema_out, target, should_validate=False)


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
                'Schema failed to validate target:\n'
                'validator   = %s\n'
                'schema-repr = %r\n'
                'schema-str  = %s\n'
                'target      = %s' %
                (validator_name, schema, to_string(schema), target)
            )
            raise Exception("%s\nerror: %s" % (msg, e))
    else:
        if not should_validate:
            msg = (
                'Schema erroneously validated the target, but should not '
                'have validated:\n'
                'validator   = %s\n'
                'schema-repr = %r\n'
                'schema-str  = %s\n'
                'target      = %s' %
                (validator_name, schema, to_string(schema), target)
            )
            raise Exception(msg)
