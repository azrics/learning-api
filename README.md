# learning-api

## Modules
- 

## Route variables (path parameterss)
- A route variable is part of the URL path itself. Use it when you want to identify a particular resource.
- /users/123
- By default, the captured value is a string. You can specify a converter if you need a different type. <int: user_id>
- Query parameters pass additional information after a ? in the url. They are useful for filtering, searching , sorting and pagination. /users?role=student. This is stored in request.args. Read it with request.args.get('role')

```bash
@app.get("/users/<user_id>")
def get_user(user_id):
    return {"requested_user_id": user_id}
```

## Flask Route Variables and Data Types

Flask route variables allow an API endpoint to capture values directly from the URL path. Flask uses **URL converters** to specify which values a route accepts and what Python data type is passed to the route function.

### 1. Supported Route Converters

| Converter | Python data type | Example route | Example URL | Value received |
|---|---|---|---|---|
| `string` (default) | `str` | `/users/<user_id>` | `/users/haris` | `"haris"` |
| `int` | `int` | `/users/<int:user_id>` | `/users/123` | `123` |
| `float` | `float` | `/products/<float:price>` | `/products/19.99` | `19.99` |
| `path` | `str` | `/files/<path:filename>` | `/files/docs/report.pdf` | `"docs/report.pdf"` |
| `uuid` | `uuid.UUID` | `/users/<uuid:user_id>` | `/users/550e8400-e29b-41d4-a716-446655440000` | UUID object |
| `any` | Usually `str` | `/status/<any(active,inactive):status>` | `/status/active` | `"active"` |

**Note:** The `string` converter is the default. The `path` converter also captures forward slashes. The `any` converter restricts the URL to the listed values.

### 2. String Converter

A route variable without an explicit converter is treated as a string.

```python
@app.get("/users/<user_id>")
def get_user(user_id):
    return {
        "value": user_id,
        "type": type(user_id).__name__
    }
```

Request:

```bash
curl http://127.0.0.1:5000/users/123
```

Response:

```json
{
  "value": "123",
  "type": "str"
}
```

Although `123` looks like a number, Flask receives it as a string.

### 3. Integer Converter

Use the `int` converter when the route variable must be an integer.

```python
@app.get("/users/<int:user_id>")
def get_user(user_id):
    return {
        "value": user_id,
        "type": type(user_id).__name__
    }
```

Request:

```bash
curl http://127.0.0.1:5000/users/123
```

Response:

```json
{
  "value": 123,
  "type": "int"
}
```

A URL such as `/users/abc` does not match this route.

### 4. Float Converter

Use the `float` converter for decimal numeric values.

```python
@app.get("/products/<float:price>")
def get_product(price):
    return {"price": price}
```

Request:

```bash
curl http://127.0.0.1:5000/products/19.99
```

The route function receives `price` as a Python `float`.

### 5. Path Converter

Use the `path` converter when a route variable must contain forward slashes.

```python
@app.get("/files/<path:filename>")
def get_file(filename):
    return {"filename": filename}
```

Request:

```bash
curl http://127.0.0.1:5000/files/docs/report.pdf
```

Response:

```json
{
  "filename": "docs/report.pdf"
}
```

Unlike the default `string` converter, `path` can capture multiple path segments.

### 6. UUID Converter

A UUID is a universally unique identifier commonly used as a resource ID.

```python
@app.get("/users/<uuid:user_id>")
def get_user(user_id):
    return {
        "user_id": str(user_id),
        "type": type(user_id).__name__
    }
```

Example request:

```bash
curl http://127.0.0.1:5000/users/550e8400-e29b-41d4-a716-446655440000
```

The function receives a `uuid.UUID` object. Convert it to a string when returning it in a JSON response.

### 7. Any Converter

Use `any` when a route should accept only a predefined set of values.

```python
@app.get("/status/<any(active,inactive):status>")
def get_status(status):
    return {"status": status}
```

Valid request:

```bash
curl http://127.0.0.1:5000/status/active
```

A request to `/status/pending` does not match this route.

### 8. Route Variables vs. Query Parameters

| Feature | Route variable | Query parameter |
|---|---|---|
| Example | `/users/123` | `/users?limit=10` |
| Purpose | Identify a resource or path segment | Filter, search, sort, or paginate |
| Flask access | Function argument | `request.args` |
| Type handling | URL converter | Read as a string by default; can be converted explicitly |

Example of a query parameter:

```python
from flask import request

@app.get("/users")
def get_users():
    limit = request.args.get("limit", default=10, type=int)
    return {"limit": limit}
```

Request:

```bash
curl "http://127.0.0.1:5000/users?limit=10"
```

Flask converts the query parameter to an integer because `type=int` is specified.

### Key Takeaways

- Route variables are defined inside angle brackets in the route path.
- URL converters determine which values match the route and the Python type passed to the function.
- The default converter is `string`.
- Route matching does not verify whether a resource exists in the database.
- Query parameters are useful for optional filtering and pagination.
- Flask also supports custom URL converters when built-in converters do not meet the requirements.
