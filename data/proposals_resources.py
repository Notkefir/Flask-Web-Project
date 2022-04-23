from flask import jsonify
from flask_restful import reqparse, abort, Resource

from . import db_session
from .proposal import Proposal

parser = reqparse.RequestParser()
parser.add_argument('id', required=False, type=int)
parser.add_argument('title', required=True)
parser.add_argument('phone_number', required=True)
parser.add_argument('coast', required=True, type=float)
parser.add_argument('user_id', required=True, type=int)


class ProposalsResource(Resource):
    def get(self, proposals_id):
        abort_if_news_not_found(proposals_id)
        db_sess = db_session.create_session()
        news = db_sess.query(Proposal).get(proposals_id)
        return jsonify(
            {'proposals': news.to_dict(rules=('-user',
                                              ))})

    def delete(self, proposals_id):
        abort_if_news_not_found(proposals_id)
        db_sess = db_session.create_session()
        proposals = db_sess.query(Proposal).get(proposals_id)
        db_sess.delete(proposals)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class ProposalsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        proposals = db_sess.query(Proposal).all()
        return jsonify({'proposals': [item.to_dict(
            rules=('-user')) for item in proposals]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        proposals = Proposal(
            title=args['title'],
            phone_number=args['phone_number'],
            user_id=args['user_id'],
            coast=args['coast'],
        )

        db_sess.add(proposals)
        db_sess.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(proposals_id):
    db_sess = db_session.create_session()
    proposals = db_sess.query(Proposal).get(proposals_id)
    if not proposals:
        abort(404, message=f"News {proposals_id} not found")
