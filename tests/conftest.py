#!/usr/bin/env python3

import pytest

from mini_aspire import data
from mini_aspire.app import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app


@pytest.fixture(autouse=True)
def _db(app):
    with app.app_context():
        data.db.drop_all()
        data.db.create_all()
        data.add_user("mary", "666")
        data.add_user("bob", "000")
        data.db.session.commit()
    return data.db
