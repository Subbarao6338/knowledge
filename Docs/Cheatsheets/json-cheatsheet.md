# JSON Cheatsheet

JSON (JavaScript Object Notation) is a strict, minimal data interchange format. Unlike YAML/TOML, it has no comments, no trailing commas, and a small fixed set of types.

## Basic Syntax & Types

```json
{
  "string_value": "hello world",
  "number_int": 42,
  "number_float": 3.14,
  "number_negative": -17,
  "number_exponent": 1.5e10,
  "boolean_true": true,
  "boolean_false": false,
  "null_value": null,
  "array_value": [1, 2, 3],
  "object_value": {
    "nested_key": "nested_value"
  }
}
```

**Rules:**
- Keys must be **double-quoted strings** — single quotes and unquoted keys are invalid.
- No trailing commas after the last element in an array/object.
- No comments of any kind (`//`, `#`, `/* */` are all invalid JSON).
- Strings must use double quotes, not single quotes.
- Numbers have no distinct int/float type at the format level — parsers decide based on presence of `.`/`e`.

## Arrays

```json
{
  "numbers": [1, 2, 3, 4, 5],
  "strings": ["a", "b", "c"],
  "mixed": [1, "two", true, null, [3, 4]],
  "objects": [
    { "id": 1, "name": "Alice" },
    { "id": 2, "name": "Bob" }
  ],
  "empty_array": []
}
```

## Nested Objects

```json
{
  "user": {
    "id": 1,
    "name": "Subbarao",
    "address": {
      "city": "Berlin",
      "country": "Germany",
      "coordinates": {
        "lat": 52.52,
        "lng": 13.405
      }
    },
    "roles": ["admin", "developer"]
  }
}
```

## String Escaping

```json
{
  "quote": "She said \"hello\"",
  "backslash": "C:\\path\\to\\file",
  "newline": "line one\nline two",
  "tab": "col1\tcol2",
  "unicode": "\u00e9\u00e8",
  "control_chars": "\b \f \r \n \t"
}
```

## JSON Lines / NDJSON (one JSON object per line — common for logs, streaming data)

```jsonl
{"id": 1, "event": "login", "timestamp": "2026-07-17T10:00:00Z"}
{"id": 2, "event": "click", "timestamp": "2026-07-17T10:01:00Z"}
{"id": 3, "event": "logout", "timestamp": "2026-07-17T10:05:00Z"}
```

## Python: Reading/Writing JSON

```python
import json

# Read from file
with open("data.json") as f:
    data = json.load(f)

# Read from string
data = json.loads('{"key": "value"}')

# Write to file
with open("out.json", "w") as f:
    json.dump(data, f, indent=2)

# Write to string
json_str = json.dumps(data, indent=2, sort_keys=True)
json_str = json.dumps(data, separators=(",", ":"))     # compact, no extra whitespace

# Custom serialization for non-standard types (e.g. datetime)
import datetime
def default_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

json.dumps({"ts": datetime.datetime.now()}, default=default_serializer)

# Handling errors
try:
    data = json.loads(bad_json_string)
except json.JSONDecodeError as e:
    print(f"Invalid JSON at line {e.lineno}, col {e.colno}: {e.msg}")

# NDJSON / JSON Lines
with open("data.jsonl") as f:
    records = [json.loads(line) for line in f if line.strip()]

with open("out.jsonl", "w") as f:
    for record in records:
        f.write(json.dumps(record) + "\n")
```

## JavaScript: Reading/Writing JSON

```javascript
const obj = JSON.parse('{"key": "value"}');
const jsonString = JSON.stringify(obj);
const prettyJson = JSON.stringify(obj, null, 2);          // indented
const filtered = JSON.stringify(obj, ["key1", "key2"]);       // only include specific keys

// Custom serialization
JSON.stringify(obj, (key, value) => {
    if (value instanceof Date) return value.toISOString();
    return value;
});

// Deep clone via JSON round-trip (simple, but loses functions/undefined/Dates)
const clone = JSON.parse(JSON.stringify(obj));
```

## JSON Schema (validating JSON structure)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["id", "name"],
  "properties": {
    "id": { "type": "integer" },
    "name": { "type": "string", "minLength": 1 },
    "email": { "type": "string", "format": "email" },
    "age": { "type": "integer", "minimum": 0, "maximum": 150 },
    "tags": {
      "type": "array",
      "items": { "type": "string" }
    },
    "status": {
      "type": "string",
      "enum": ["active", "inactive", "pending"]
    }
  },
  "additionalProperties": false
}
```

```python
import jsonschema

jsonschema.validate(instance=data, schema=schema)      # raises ValidationError if invalid
```

## jq — Command-Line JSON Processing

```bash
echo '{"name": "Alice", "age": 30}' | jq '.'          # pretty-print
cat data.json | jq '.name'                                # extract a field
cat data.json | jq '.users[0].name'                          # nested access
cat data.json | jq '.users[]'                                    # iterate array elements
cat data.json | jq '.users[] | select(.age > 25)'                  # filter
cat data.json | jq '[.users[] | .name]'                               # map to a new array
cat data.json | jq '.users | length'                                     # array length
cat data.json | jq '.users | sort_by(.age)'                                 # sort
cat data.json | jq -r '.name'                                                  # raw output, no quotes
cat data.json | jq '{name: .name, city: .address.city}'                          # reshape/project
cat data.json | jq 'keys'                                                           # object keys
cat data.json | jq 'to_entries'                                                        # object -> array of {key,value}

curl -s https://api.example.com/data | jq '.results[] | {id, name}'
```

## Common Patterns

```json
// API response envelope
{
  "success": true,
  "data": { "id": 1, "name": "example" },
  "error": null,
  "meta": { "page": 1, "total_pages": 5 }
}

// Error response
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}

// Config file
{
  "version": "1.0",
  "environment": "production",
  "features": {
    "darkMode": true,
    "betaFeatures": false
  },
  "endpoints": {
    "api": "https://api.example.com",
    "timeout": 30000
  }
}
```

## Common Gotchas

- No comments — if you need documented config, use YAML/TOML/JSONC (JSON with Comments, a superset some tools like VS Code settings support) instead.
- No trailing commas — `{"a": 1, "b": 2,}` is invalid JSON and will fail to parse in strict parsers.
- Keys must be double-quoted strings — `{key: "value"}` and `{'key': 'value'}` are both invalid.
- Numbers have no distinction between int/float in the spec itself, and very large integers (beyond JavaScript's safe integer range, ~2^53) can lose precision when parsed by JS-based tools — represent large IDs as strings if precision matters.
- `NaN`, `Infinity`, and `undefined` are NOT valid JSON values — `JSON.stringify` in JS silently converts them to `null` or drops them (for `undefined` in objects).
- Duplicate keys in an object are technically allowed by the grammar but behavior is undefined — most parsers keep the last occurrence, but don't rely on this.
- Trailing/leading whitespace and newlines outside the top-level value are fine, but the overall document must have exactly one top-level value (object, array, string, number, boolean, or null).
