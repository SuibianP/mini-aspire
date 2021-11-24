#!/usr/bin/env python3

"""
Test loan application functionalities
"""

ENDPOINT = "/loan"


def test_apply_success(client):
    """
    Test successful application
    """
    assert client.post(ENDPOINT, auth=("mary", "666"), data={
        "amount": 50,
        "term": 10
    }).status_code == 201


def test_apply_unauthorised(client):
    """
    Unauthorised due to no credentials
    """
    assert client.post(ENDPOINT).status_code == 401


def test_apply_wrong_cred(client):
    """
    Unauthorised due to wrong credentials
    """
    assert client.post(ENDPOINT, auth=("nobody", "666")).status_code == 401


def test_repay_missing(client):
    """
    Missing required fields
    """
    assert client.post(ENDPOINT, auth=("mary", "666")).status_code == 400
