from flask import Blueprint, jsonify, request
from api.models.models import RedFlag, red_flags, Users, users_list
from api.validations import empty_record_fields, invalid_input_types, empty_strings_add_red_flag
from api.Handlers.error_handlers import InvalidUsage
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

from functools import wraps
import datetime
import uuid


red_flag_blueprint = Blueprint("red_flag", __name__)
user_blueprint = Blueprint("user", __name__)


def token_req(end_point):
    @wraps(end_point)
    def check(*args, **kwargs):
        if 'token' in request.headers:
            tk = request.headers['token']
        else:
            return jsonify({'message': 'you should login'})
        try:
            jwt.decode(tk, 'derek_mananu_scretekey')
        except:
            return jsonify({'message': 'user not authenticated'})
        return end_point(*args, **kwargs)
    return check


@user_blueprint.route('/api/auth/signup', methods=['POST'], strict_slashes=False)
def signup():
    data = request.get_json()
    user_id = uuid.uuid4()
    username = data.get('username')
    password = generate_password_hash('password', method='sha256')
    email = data.get('email')

    signup_data = Users(user_id, username, password, email)

    users_list.append(signup_data.to_dict())
    return jsonify({"message": "user added"})


@user_blueprint.route('/api/v1/user', methods=['GET'])
def get_all_users():
    if not users_list:
        return jsonify({"message": "there are no users currently"})
    return jsonify({"users": users_list})


@user_blueprint.route('/api/auth/login', methods=['POST'], strict_slashes=False)
def login():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    for user in users_list:
        if not user['username'] == username:
            return jsonify({"message": "wrong username"})
        if not check_password_hash(user['password'], 'password'):
            return jsonify({"message": "wrong password"})

    tk = jwt.encode({
        'username': user['username'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    }, 'derek_mananu_scretekey')
    return jsonify({"message": "you are now logged in", 'token': tk.decode('UTF-8')})


@red_flag_blueprint.route('/api/v1/red_flag', methods=['POST'], strict_slashes=False)
@token_req
def create_red_flag():

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.get_json()
    red_flag_id = len(red_flags) + 1
    red_flag_latitude = data.get('red_flag_latitude')
    red_flag_longitude = data.get('red_flag_longitude')
    red_flag_desc = data.get('red_flag_desc')
    user_id = data.get('user_id')
    status = data.get('status')

    val = empty_record_fields(red_flag_latitude, red_flag_longitude, red_flag_desc, user_id, status)
    if val:
        raise InvalidUsage(val, 400)
    input_type = invalid_input_types(red_flag_latitude, red_flag_longitude, red_flag_desc, user_id, status)
    if input_type:
        raise InvalidUsage(input_type, 400)
    empty_strings = empty_strings_add_red_flag(red_flag_latitude, red_flag_longitude, red_flag_desc, user_id, status)
    if empty_strings:
        raise InvalidUsage(empty_strings, 400)

    record = RedFlag(red_flag_id, red_flag_latitude, red_flag_longitude, red_flag_desc, user_id, status)
    red_flags.append(record.to_dict() )
    return jsonify({"message": "red flag successfully added ", "red_flag": record.to_dict()}), 201


@red_flag_blueprint.route('/api/v1/red_flag', methods=['GET'], strict_slashes=False)
@token_req
def get_all_red_flags():
    if not red_flags:
        return jsonify({"message": "List is empty first post"})
    return jsonify({"red_flags": red_flags})


@red_flag_blueprint.route('/api/v1/red_flag/<int:red_flag_id>', methods=['GET'], strict_slashes=False)
@token_req
def get_single_red_flag(red_flag_id):
    for record in red_flags:
        if record['red_flag_id'] == red_flag_id:
            return jsonify({"message": "your request is successfull", "data": record}), 200
    return jsonify({"message": "the red flag doesnt exist"}), 400


@red_flag_blueprint.route('/api/v1/red_flag/<int:red_flag_id>/cancel', methods=['PUT'], strict_slashes=False)
@token_req
def cancel_red_flag(red_flag_id):
    for record in red_flags:
        if record['red_flag_id'] == red_flag_id:
            record['status'] = 'Resolved'
            return jsonify(record), 200
    return jsonify({"message": "the red flag does not exist"}), 400


@red_flag_blueprint.route('/api/v1/users/<int:user_id>/red_flag', methods=['GET'], strict_slashes=False)
@token_req
def get_red_flag_by_user_id(user_id):
    single = []
    for record in red_flags:
        if record['user_id'] == user_id:
            single.append(record)

    if len(single) > 0:
        return jsonify(single), 200
    return jsonify({"message": "there is no such user"}), 400


@red_flag_blueprint.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



