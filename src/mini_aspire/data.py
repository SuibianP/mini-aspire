#!/usr/bin/env python3

import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import PasswordType, DateRangeType

db = SQLAlchemy()


class User(db.Model):
    username = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    password = db.Column(PasswordType(schemes=["sha256_crypt"]), nullable=False)


def add_user(username, password):
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()


class Loan(db.Model):
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
    new_entry = Loan(username=username, amount=amount, term=term)
    db.session.add(new_entry)
    db.session.commit()
    return new_entry.id


class NoSuchLoanException(Exception):
    pass


class WrongUserException(Exception):
    pass


def repay_loan(loan_id, amount):
    from auth import auth
    try:
        loan = Loan.query.filter_by(id=loan_id).one()
    except NoResultFound:
        raise NoSuchLoanException()
    if loan.username != auth.current_user():
        raise WrongUserException()
    loan.amount -= amount
    db.session.commit()


def verify_password(username, password):
    try:
        if User.query.filter_by(username=username).one().password == password:
            return username
    except NoResultFound:
        pass
    return False
