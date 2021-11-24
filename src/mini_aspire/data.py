#!/usr/bin/env python3

"""
Routines for handling database interfacing operations
"""

import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import PasswordType, DateRangeType

db = SQLAlchemy()


class User(db.Model):
    """
    User database model
    """
    # pylint: disable=too-few-public-methods
    username = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    password = db.Column(PasswordType(schemes=["sha256_crypt"]), nullable=False)


def add_user(username, password):
    """
    Add a new user to the records
    """
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()


class Loan(db.Model):
    """
    Loan database model
    """
    # pylint: disable=too-few-public-methods
    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False, autoincrement=True)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    user = db.relationship('User', backref=db.backref('loans', lazy=True))
    amount = db.Column(db.Numeric, nullable=False)
    # TODO For SQLite, numeric type may incur floating calculations
    # term = db.Column(DateRangeType)
    # TODO Due to bug in this type for non-Postgres dbs, it is not used for now.
    start = db.Column(db.Date, nullable=False, default=datetime.date.today)
    term = db.Column(db.Integer, nullable=False)


def add_loan(username, amount, term):
    """
    Append a loan with given information into the records
    """
    new_entry = Loan(username=username, amount=amount, term=term)
    db.session.add(new_entry)
    db.session.commit()
    return new_entry.id


class NoSuchLoanException(Exception):
    """
    Exception to signal that a loan id is not valid
    """


class WrongUserException(Exception):
    """
    Exception to signal that a user is not the owner of a loan
    """


def repay_loan(loan_id, amount):
    """
    Deduct loan amount from record
    """
    from .auth import auth
    try:
        loan = Loan.query.filter_by(id=loan_id).one()
    except NoResultFound as nrf:
        raise NoSuchLoanException(nrf)
    if loan.username != auth.current_user():
        raise WrongUserException()
    loan.amount -= amount
    db.session.commit()


def verify_password(username, password):
    """
    Do password verification by querying the database
    """
    try:
        if User.query.filter_by(username=username).one().password == password:
            return username
    except NoResultFound:
        pass
    return False
