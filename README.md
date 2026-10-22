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