from flask import request
from flask import current_app, g
from functools import wraps
import jwt
from model.user import User

def token_required(roles=None):
    """
    Guard API endpoints that require authentication.

    This function performs the following steps:
    
    1. Checks for the presence of a valid JWT token in the request cookie.
    2. Decodes the token and retrieves the user data.
    3. Checks if the user data is found in the database.
    4. Checks if the user has the required role.
    5. Sets the current_user in the global context (Flask's g object).
    6. Returns the decorated function if all checks pass.

    Possible error responses:
    
    - 401 / Unauthorized: token is missing or invalid.
    - 403 / Forbidden: user has insufficient permissions.
    - 500 / Internal Server Error: something went wrong with the token decoding.

    Args:
        roles (list, optional): A list of roles that are allowed to access the endpoint. Defaults to None.

    Returns:
        function: The decorated function if all checks pass.
    """
    def decorator(func_to_guard):
        @wraps(func_to_guard)
        def decorated(*args, **kwargs):
            token = request.cookies.get(current_app.config["JWT_TOKEN_NAME"])
            if not token:
                return {
                    "message": "Token is missing",
                    "error": "Unauthorized"
                }, 401

            try:
                data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
                current_user = User.query.filter_by(_uid=data["_uid"]).first()
                if not current_user:
                    return {
                        "message": "User not found",
                        "error": "Unauthorized",
                        "data": data
                    }, 401

                if roles and current_user.role not in roles:
                    return {
                        "message": "User does not have the required role",
                        "error": "Forbidden",
                        "data": data
                    }, 403
                    
                # Authentication succes, set the current_user in the global context (Flask's g object)
                g.current_user = current_user
            except jwt.ExpiredSignatureError:
                return {
                    "message": "Token has expired",
                    "error": "Unauthorized"
                }, 401
            except jwt.InvalidTokenError:
                return {
                    "message": "Invalid token",
                    "error": "Unauthorized"
                }, 401
            except Exception as e:
                return {
                    "message": "An error occurred",
                    "error": str(e)
                }, 500

            # Call back to the guarded function if all checks pass
            return func_to_guard(*args, **kwargs)
        return decorated
    return decorator