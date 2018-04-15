Overview
--------

This documents support (or lack thereof) for conversion of different JSON
Schema features.

Official JSON Schema draft references can be found
[here](http://json-schema.org/specification-links.html). This library targets
support for the [draft 4 specification](https://tools.ietf.org/html/draft-fge-json-schema-validation-00)


### [types](https://tools.ietf.org/html/draft-zyp-json-schema-04#section-3.5)

Supported | Feature                | Example
--------- | ---------------------- | -------
Y         | `array` type           | `{ "type": "array" }`
Y         | `boolean` type         | `{ "type": "boolean" }`
Y         | `integer` type         | `{ "type": "integer" }`
Y         | `number` type          | `{ "type": "number" }`
Y         | `null` type            | `{ "type": "null" }`
Y         | `object` type          | `{ "type": "object" }`
Y         | `string` type          | `{ "type": "string" }`


### [numbers](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5)

Supported | Feature                | Example
--------- | ---------------------- | -------
Y         | `multipleOf`           | `{"multipleOf": 2}`
Y         | `minimum`              | `{"minimum": 1.1}`
Y         | `maximum`              | `{"maximum": 3.5}`
Y         | `exclusiveMinimum`     | `{"exclusiveMinimum": True}`
Y         | `exclusiveMaximum`     | `{"exclusiveMaximum": True}`


### [strings](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.2)

Supported | Feature       | Example
--------- | ------------- | -------
Y         | `string` type | `{ "type": "string" }`
Y         | `minLength`   | `{ "minLength": 2 }`
Y         | `maxLength`   | `{ "maxLength": 5 }`
n         | Pattern       |


### [arrays](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.3)

Supported | Feature                                  | Example
--------- | ---------------------------------------- | -------
Y         | Items Schema                             | `{ "items": { "type": "integer" }}`
Y         | Items Schema List                        | `{ "items": [{ "type": "integer" }, { "type": "boolean" }]}`
Y         | Items Schema List with `additionalItems` | `{ "items": [...], "additionalItems": false }`
Y         | Min Items                                | `{ "type": "array", "minItems": 2 }`
Y         | Max Items                                | `{ "type": "array", "maxItems": 5 }`
n         | Unique Items                             |


### [objects](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.4)

Supported | Feature                         | Example
--------- | --------------------------------| -------
Y         | `object` type                   | `{ "type": "object" }`
n         | `minProperties`                 |
n         | `maxProperties`                 |
n         | `required`                      |
Y         | `additionalProperties=False`    | `{ "additionalProperties": false }`
Y         | `additionalProperties=<schema>` | `{ "additionalProperties": {"type": "string"}`
Y         | `properties`                    | `{ "properties": { "key": { "type": "string" }}}`
n         | `patternProperties`             |
n         | `dependencies`                  |


### [other keywords](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-5.5)

Supported    | Feature         | Example
------------ | --------------- | -------
ignored      | `$schema`       |
n            | `enum`          |
Y            | `type=<string>` | `{ "type": "integer"} `
Y            | `type=<list>`   | `{ "type": ["integer", "string"] }`
Y            | `allOf`         | `{ "allOf": [{"type": "string"}, {"maxLength": 5}] }`
Y            | `anyOf`         | `{ "anyOf": [{"type": "string"}, {"type": "integer"}] }`
n            | `oneOf`         | `{ "oneOf": [{ "multipleOf": 5 }, { "multipleOf": 3 }] }`
n            | `not`           |
Y (see note) | `definitions`   |

note: The `definitions` is a place for content that can be included elsewhere
in the schema. `voluptuary` supports following JSON references (specified with
the `$ref` keyword) to read and process content in the `definitions` section
(`voluptuary` reuses the ref resolution functionality from
[jsonschema](https://github.com/Julian/jsonschema)).

note: The `$schema` is ignored. `voluptuary` only explicitly supports
converting Draft 4 JSON Schema specification.


### [metadata keywords](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-6)

`voluptuary` ignores metadata keywords, as these do not affect validation
behavior.

Supported   | Feature       | Example
----------- | -------       | -------
ignored     | `title`       |
ignored     | `description` |
ignored     | `default`     |


### [formats](https://tools.ietf.org/html/draft-fge-json-schema-validation-00#section-7)

Supported   | Feature       | Example
----------- | -------       | -------
n           | `date-time`   |
n           | `email`       |
n           | `hostname`    |
n           | `ipv4`        |
n           | `ipv6`        |
n           | `ipv6`        |
n           | `uri`         |
