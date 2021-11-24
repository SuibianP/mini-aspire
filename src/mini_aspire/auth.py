#!/usr/bin/env python3

"""
Authentication related
"""

from flask_httpauth import HTTPBasicAuth

from .data import verify_password

auth = HTTPBasicAuth()


@auth.verify_password
def verify(username, password):
    """
    Routine for verifying if username-password pair match our records
    """
    return verify_password(username, password)


def get_auth():
    """
    Getter for auth object
    """
    return auth
