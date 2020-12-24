from functools import wraps
import json


def jsonify(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(*args, **kwargs)
        return json.loads(func(*args, **kwargs))
    return decorated_function