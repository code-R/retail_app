from datetime import datetime, timedelta
import falcon
import jwt
import os
from passlib.hash import sha256_crypt

from retailstore.control.base import BaseResource


class AuthService:
    DATA_STORE = {
        'email': 'vamsi.skrishna@gmail.com',
        'encrypted_password': sha256_crypt.encrypt('s3cr3t')
    }

    def __init__(
        self,
        data,
        secret=None,
        token_expiration_seconds=3600,
        algorithm = 'HS256',
    ):
        self.email = data['email']
        self.password = data['password']
        self.secret = secret or os.environ.get('JWT_SECRET')
        self.token_expiration_seconds = token_expiration_seconds
        self.algorithm = algorithm

    def _verify_email(self):
        return self.email == self.DATA_STORE['email']

    def _verify_password(self):
        return sha256_crypt.verify(
            self.password, self.DATA_STORE['encrypted_password'])

    @property
    def _token_expires_at(self):
        return datetime.utcnow() + timedelta(
            seconds=self.token_expiration_seconds)

    def is_valid(self):
        return self._verify_email() and self._verify_password()

    def generate_jwt_token(self):
        encode_data = {
            'user_identifier': self.email,
            'exp': self._token_expires_at
        }
        return jwt.encode(
            encode_data,
            self.secret,
            algorithm=self.algorithm).decode("utf-8")


class CollectionResource(BaseResource):

    def on_post(self, req, resp):
        auth_service = AuthService(req.context['json'])

        if auth_service.is_valid():
            resp.body = auth_service.generate_jwt_token()
            resp.status = falcon.HTTP_201
        else:
            resp.status = falcon.HTTP_401
