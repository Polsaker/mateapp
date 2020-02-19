import bcrypt
from flask import Blueprint, request, jsonify
from peewee import fn
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_jwt_extended import jwt_refresh_token_required, jwt_optional

from ..models import User

token = Blueprint('token', __name__)

@token.route('/new', methods=['POST'])
def login():
    """ Creates a new access token from a username & password tuple """
    if not request.is_json:
        return jsonify(msg="Missing parameters"), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify(msg="Missing username or password"), 400

    try:
        user = User.get(fn.Lower(User.username) == username.lower())
    except User.DoesNotExist:
        return jsonify(msg="Bad username or password"), 401

    if user.status != 0:
        return jsonify(msg="Forbidden"), 403

    if user.crypto == 1:  # bcrypt
        thash = bcrypt.hashpw(password.encode('utf-8'),
                              user.password.encode('utf-8'))
        if thash != user.password.encode('utf-8'):
            return jsonify(msg="Bad username or password"), 401
    else:
        return jsonify(msg="Bad user data"), 400

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(access_token=access_token, refresh_token=refresh_token), 200


@token.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """ Returns a new access token. Requires providing a refresh token """
    current_user = get_jwt_identity()
    try:
        user = User.get_by_id(current_user)
    except User.DoesNotExist:
        return jsonify(msg="User does not exist"), 400

    if user.status != 0:
        return jsonify(msg="Forbidden"), 403

    new_token = create_access_token(identity=current_user, fresh=False)
    return jsonify(access_token=new_token), 200
