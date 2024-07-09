#!/usr/bin/env python3
"""basic auth module"""
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """basic auth class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract_base64_authorization_header method"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decode_base64_authorization_header method"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            import base64
            message_bytes = base64.b64decode(base64_authorization_header)
            message = message_bytes.decode('utf-8')
            return message
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """extract_user_credentials method"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email, password = decoded_base64_authorization_header.split(':')
        return (email, password)

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """user_object_from_credentials method"""
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        User.load_from_file()
        users = User.search({'email': user_email})
        if users == []:
            return None
        if not users[0].is_valid_password(user_pwd):
            return None
        return users[0]
