#!/usr/bin/env python3

from flask import Blueprint, current_app
from flask_restx import Resource, Api, reqparse

from .auth import get_auth
from .data import add_loan

loan_blueprint = Blueprint('apply', __name__)
loan_api = Api(loan_blueprint, authorizations={
    'basic': {
        'type': 'basic'
    }
}, security='basic')


@loan_api.route("/loan")
@loan_api.response(401, 'Not authenticated')
@loan_api.response(400, 'Parameter error')
class Loan(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument('amount', type=int, required=True, help='The total amount of loan')
    post_parser.add_argument('term', type=int, required=True, help='The loan term')

    @get_auth().login_required
    @loan_api.response(201, 'Successfully applied for loan')
    @loan_api.expect(post_parser)
    def post(self):
        args = self.post_parser.parse_args(strict=True)
        amount = args["amount"]
        term = args["term"]
        current_app.logger.info(f"Term: {term}; Amount: {amount}")
        loan_id = add_loan(get_auth().current_user(), amount, term)
        return loan_id, 201
