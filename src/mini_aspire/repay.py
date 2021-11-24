#!/usr/bin/env python3

"""
Repay requests
"""

from flask import Blueprint, current_app
from flask_restx import Resource, reqparse, Api

from .auth import get_auth
from .data import repay_loan, NoSuchLoanException, WrongUserException

repay_blueprint = Blueprint('repay', __name__)
repay_api = Api(repay_blueprint, authorizations={
    'basic': {
        'type': 'basic'
    }
}, security='basic')


@repay_api.route("/loan/<int:loan_id>")
@repay_api.response(404, 'Loan not found')
@repay_api.response(401, 'Not authenticated')
@repay_api.response(403, 'Loan does not belong to the current user')
@repay_api.response(400, 'Parameter error')
class Repay(Resource):
    """
    Repayment handling
    """
    patch_parser = reqparse.RequestParser()
    patch_parser.add_argument('amount', type=int, required=True, help='The repay amount')

    @get_auth().login_required
    @repay_api.response(204, 'Successfully repaid')
    @repay_api.expect(patch_parser)
    def patch(self, loan_id):
        args = self.patch_parser.parse_args(strict=True)
        amount = args["amount"]
        current_app.logger.info(f"ID: {loan_id}; Amount: {amount}")
        try:
            repay_loan(loan_id, amount)
        except NoSuchLoanException:
            repay_api.abort(404)
        except WrongUserException:
            repay_api.abort(403)
        return '', 204
