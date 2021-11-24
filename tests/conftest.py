#!/usr/bin/env python3

"""
pytest fixtures
"""

import pytest

from mini_aspire import data
from mini_aspire.app import create_app


@pytest.fixture(scope='session')
def app():
    """
    Scope is session since the app itself is not stateful
    """
    new_app = create_app()
    return new_app


@pytest.fixture(autouse=True)
def _db(app):
    """
    pytest-flask-sqlalchemy required fixture
    Get a blank database each time
    """
    with app.app_context():
        data.db.drop_all()
        data.db.create_all()
        data.add_user("mary", "666")
        data.add_user("bob", "000")
        data.db.session.commit()
    return data.db
