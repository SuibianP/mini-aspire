#!/usr/bin/env python3

"""
Expose app factory
"""

from flask import Flask

from .apply import loan_blueprint
from .repay import repay_blueprint


def create_app():
    """
    Factory method
    """
    app = Flask(__name__)
    app.register_blueprint(repay_blueprint)
    app.register_blueprint(loan_blueprint)
    from .data import db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db.init_app(app)
    db.create_all(app=app)
    return app


if __name__ == '__main__':
    create_app().run()
