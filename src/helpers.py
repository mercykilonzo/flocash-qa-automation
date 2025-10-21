import os
from requests.auth import HTTPBasicAuth

class AuthHelper:
    def __init__(self, config):
        self.config = config

    def get_auth(self):
        """Return auth object for requests or None"""
        if self.config.basic_auth_username and self.config.basic_auth_password:
            return HTTPBasicAuth(self.config.basic_auth_username, self.config.basic_auth_password)
        return None

    def build_headers(self):
        return {"Content-Type": "application/json"}
