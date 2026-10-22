# Consider the DB team has created a DB for our application without tables
from uuid import uuid4
from flask import Flask, request

"""
Flask needs to know exactly where your script is located so it can seamlessly look up and serve.
This finds your /static and /templates folder when structured inside the script folder.
"""
app = Flask(__name__)

database = {}

@app.get("/")
def home():
    return {
        "app_name": "Nexverse Learning",
        "title": "Learn by Doing",
        "message": "Welcome to Nexverse Learning",
        "description": (
            "Build practical engineering skills by solving "
            "real-world problems and developing working systems."
        ),
        "navigation": [
            {"label": "Home", "url": "/"},
            {"label": "Courses", "url": "/courses"},
            {"label": "Login", "url": "/login"}
        ],
        "status": "under_development"
    }

@app.route("/tables", methods=["GET"])
def get_tables():
    return {"tables": list(database.keys())}

@app.post('/create_table')
def create_table():
    # If the JSON is invalid, body becomes None instead of raising a 400 error
    data = request.get_json(silent=True)

    print(data)

    # checking if the data belong to dict class.
    if not isinstance(data, dict):
        return {"error": "A JSON object is required"}, 400

    table_name = data.get("table_name")
    print(table_name)

    if not isinstance(table_name, str) or not table_name.strip():
        return {"error": "A valid table_name is required"}, 400

    table_name = table_name.strip()

    if table_name in database:
        return {"error": "Table already exists"}, 409

    database[table_name] = {}

    return {
        "message": "Table created successfully",
        "table_name": table_name,
        "database": database
    }, 201

# READ ONE TABLE
@app.get("/tables/<table_name>")
def get_table(table_name):
    if table_name not in database:
        return {"error": "Table not found"}, 404

    return {
        "table_name": table_name,
        "records": database[table_name]
    }

# DELETE TABLE
@app.delete("/tables/<table_name>")
def delete_table(table_name):
    if table_name not in database:
        return {"error": "Table not found"}, 404

    del database[table_name]

    return {"message": "Table deleted"}

@app.post("/tables/users/records")
def create_user():
    # Check whether the users table exists
    if "users" not in database:
        return {"error": "Users table does not exist"}, 404

    # Read the incoming JSON
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return {"error": "A JSON object is required"}, 400

    # Validate required fields
    name = data.get("name")
    email = data.get("email")

    if not isinstance(name, str) or not name.strip():
        return {"error": "A valid name is required"}, 400

    if not isinstance(email, str) or not email.strip():
        return {"error": "A valid email is required"}, 400

    name = name.strip()
    email = email.strip().lower()

    # Prevent duplicate email addresses
    for user in database["users"].values():
        if user["email"] == email:
            return {"error": "Email already exists"}, 409

    # Create the user record
    user_id = str(uuid4())

    user = {
        "id": user_id,
        "name": name,
        "email": email,
        "role": "student"
    }

    database["users"][user_id] = user

    return {
        "message": "User created successfully",
        "user": user
    }, 201

from flask import request

@app.get("/users")
def get_users():
    role = request.args.get("role")

    if role is None:
        return {
            "message": "Please provide a role query parameter"
        }, 400

    if role not in ["admin", "staff", "student"]:
        return {
            "error": "Invalid role"
        }, 400

    matching_users = []

    for user in database["users"].values():
        if user["role"] == role:
            matching_users.append(user)

    return {
        "filter": role,
        "count": len(matching_users),
        "users": matching_users
    }

# Test the endpoint with qury parameter
# curl "http://127.0.0.1:5000/users?role=staff"
    
"""The functions are stored in a dictioanry by flask. To see them use the command below.
This is useful for debugging and understanding the routes available in your application.
These functions are called when a request is made to the corresponding route. 
The keys in the dictionary are the endpoint names, and the values are the function objects themselves.
If no route is defined for a specific endpoint, Flask will return a 404 error when that endpoint is accessed."""
print(app.view_functions)

if __name__ == "__main__":
    app.run(debug=True)