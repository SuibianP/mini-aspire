#!/usr/bin/env python3

from flask_httpauth import HTTPBasicAuth

from .data import verify_password

auth = HTTPBasicAuth()


@auth.verify_password
def verify(username, password):
    return verify_password(username, password)


def get_auth():
    return auth
