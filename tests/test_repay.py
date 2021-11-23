#!/usr/bin/env python3

import pytest

from mini_aspire.data import add_loan


def endpoint_of(index):
    return f"/loan/{index}"


@pytest.mark.depends(name='test_apply.py::test_apply_success')
def test_repay_success(client):
    add_loan("mary", 200, 5)
    assert client.patch(endpoint_of(1), auth=("mary", "666"), data={
        "amount": 10
    }).status_code == 204


def test_repay_missing(client):
    assert client.patch(endpoint_of(1), auth=("mary", "666")).status_code == 400


def test_repay_unauthorised(client):
    """
    Unauthorised due to no credentials
    """
    assert client.patch(endpoint_of(1)).status_code == 401


def test_repay_wrong_cred(client):
    """
    Unauthorised due to wrong credentials
    """
    assert client.patch(endpoint_of(1)).status_code == 401


@pytest.mark.depends(name='test_apply.py::test_apply_success')
def test_repay_wrong_user(client):
    """
    User authorised but is not the owner of the debt
    """
    add_loan("mary", 200, 5)
    assert client.patch(endpoint_of(1), auth=("bob", "000"), data={
        "amount": 10
    }).status_code == 403


def test_repay_nonexistent(client):
    """
    No such debt
    """
    assert client.patch(endpoint_of(99), auth=("mary", "666"), data={
        "amount": 10
    }).status_code == 404
