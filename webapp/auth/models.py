from .. import db
import os
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
import hashlib
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time


from binascii import hexlify
import functools as func




class Referrer(db.Model):
    __tablename__ = 'referrer'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(18))
    user_referred = db.Column(db.String)

    def __init__(self, code, user_referred):
        self.code = code
        self.user_referred = user_referred


# class Permission:
#     BASIC = 1
#     COMMENT = 2
#     MODERATE = 4
#     ADMIN = 8
#
#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __init__(self, **kwargs):
#         super(Role, self).__init__(**kwargs)
#         if self.permissions is None:
#             self.permissions = 0
#
#     @staticmethod
#     def insert_roles():
#         roles = {
#             'User': [Permission.BASIC, Permission.COMMENT],
#             'Moderator': [Permission.BASIC, Permission.COMMENT, Permission.MODERATE],
#             'Administrator': [Permission.BASIC, Permission.COMMENT, Permission.MODERATE, Permission.ADMIN]
#         }
#
#         default_role = 'User'
#         for r in roles:
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)
#             role.reset_permissions()
#             for perm in roles[r]:
#                 role.add_permission(perm)
#             role.default = (role.name == default_role)
#             db.session.add(role)
#         db.session.commit()
#
#     def add_permission(self, perm):
#         if not self.has_permission(perm):
#             self.permissions += perm
#
#     def remove_permission(self, perm):
#         if self.has_permission(perm):
#             self.permissions -= perm
#
#     def reset_permissions(self):
#         self.permissions = 0
#
#     def has_permission(self, perm):
#         return self.permissions & perm == perm
#
#     def __repr__(self):
#         return '<Role %r>' % self.name

roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    country = db.Column(db.String(64))
    phone = db.Column(db.String(15))
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    coin = db.Column(db.String(20))
    wallet_address = db.Column(db.String(64))

    profile_pic = db.Column(db.String(), nullable=True)

    account_balance = db.Column(db.Integer)
    deposit_amount = db.Column(db.Integer)
    total_deposit = db.Column(db.Integer)
    total_payouts = db.Column(db.Integer)
    transaction_image = db.Column(db.String(255))
    transaction = db.relationship('Transactions', backref='user', lazy='dynamic')

    investment = db.relationship('Investments', backref='user', lazy='dynamic')

    referral_code = db.Column(db.String(20), unique=True)
    referrals = db.Column(db.Integer, default=0)

#    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
    )

    # def __init__(self, email, username,):
    #     default = Role.query.filter_by(name="default").one()
    #     self.roles.append(default)
    #     self.username = username
    #     self.email = email

    # def __repr__(self):
    #     return '<User {}>'.format(self.username)

    def has_role(self, name):
        for role in self.roles:
            if role.name == name:
                return True
        return False

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def generate_ref(self):
        if not self.referral_code:
            new_code = self.username
            collision = User.query.filter_by(referral_code=new_code).first()
            while collision:
                new_code = self.username
                collision = User.query.filter_by(referral_code=new_code).first()
            self.referral_code = new_code

    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.role is None:
    #         if self.email == current_app.config['ADMINS']:
    #             self.role = Role.query.filter_by(name='Administrator').first()
    #         if self.role is None:
    #             self.role = Role.query.filter_by(default=True).first()
    #
    # def can(self, perm):
    #     return self.role is not None and self.role.has_permission(perm)
    #
    # def is_administrator(self):
    #     return self.can(Permission.ADMIN)

    def __repr__(self):
        return f"<User '{self.email}'"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    # @password.setter

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=900):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # def generate_reset_token(self, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps({'reset': self.id}).decode('utf-8')
    #
    # @staticmethod
    # def reset_password(token, new_password):
    #     s = Serializer(current_app.config['SECRET_KEY'])
    #     try:
    #         data = s.loads(token.encode('utf-8'))
    #     except:
    #         return False
    #     user = User.query.get(data.get('reset_password'))
    #     if user is None:
    #         return False
    #     user.password = new_password
    #     db.session.add(user)
    #     return True
    #
    # def generate_email_change_token(self, new_email, expiration=3600):
    #     s = Serializer(current_app.config['SECRET_KEY'], expiration)
    #     return s.dumps(
    #         {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, index=True)
    transaction_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    transaction_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    transaction_amount = db.Column(db.Integer)
    transaction_imgs = db.Column(db.String(255), nullable=True)
    transaction_type = db.Column(db.String(15))
    transaction_status = db.Column(db.String(15))
    transaction_email = db.Column(db.String(64), index=True)
    receiver_email = db.Column(db.String(64), index=True)

    def __init__(self, transaction_time, transaction_id, transaction_amount, transaction_imgs, transaction_type
                 , transaction_status, transaction_email, receiver_email):
        self.transaction_time = transaction_time
        self.transaction_id = transaction_id
        self.transaction_amount = transaction_amount
        self.transaction_imgs = transaction_imgs
        self.transaction_type = transaction_type
        self.transaction_status = transaction_status
        self.transaction_email = transaction_email
        self.receiver_email = receiver_email


class Investments(db.Model):
    __tablename__ = 'investments'
    id = db.Column(db.Integer, primary_key=True, index=True)
    investment_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    investment_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    investment_amount = db.Column(db.Integer)
    investment_plan = db.Column(db.String(15))
    investment_status = db.Column(db.String(15))

    def __init__(self, investment_id, investment_amount, investment_plan, investment_time
                 , investment_status):

        self.investment_id = investment_id
        self.investment_time = investment_time
        self.investment_amount = investment_amount
        self.investment_plan = investment_plan
        self.investment_status = investment_status


class Share(db.Model):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True, index=True)
    share_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    share_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    share_amount = db.Column(db.Integer)
    share_type = db.Column(db.String(15))
    share_email = db.Column(db.String(64), index=True)

    def __init__(self, share_time, share_id, share_amount, share_type, share_email):
        self.share_time = share_time
        self.share_id = share_id
        self.share_amount = share_amount
        self.share_type = share_type
        self.share_email = share_email


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

