from flask import jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .users import User

parser = reqparse.RequestParser()
parser.add_argument('id', required=False, type=int)
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('specialization', required=True)
parser.add_argument('about', required=True)
parser.add_argument('address', required=True)
parser.add_argument('email', required=True)
parser.add_argument('hashed_password', required=True)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(user_id)
        return jsonify({'users': users.to_dict(
            only=('surname', 'name', 'age', 'specialization', 'about', 'address', 'email', 'hashed_password'))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        db_sess = db_session.create_session()
        users = db_sess.query(User).get(user_id)
        db_sess.delete(users)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('surname', 'name', 'age', 'specialization', 'about', 'address', 'email', 'hashed_password')) for
            item
            in users]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            specialization=args['specialization'],
            about=args['about'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )

        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def abort_if_users_not_found(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')
