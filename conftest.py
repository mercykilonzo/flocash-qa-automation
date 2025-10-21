import os
import pytest
from dotenv import load_dotenv
from src.config import Config
from src.helpers import AuthHelper

load_dotenv()

@pytest.fixture(scope="session")
def config():
    return Config(
        base_url=os.getenv("BASE_URL", "https://sandbox.flocash.com/rest/v2"),
        basic_auth_username=os.getenv("BASIC_AUTH_USERNAME"),
        basic_auth_password=os.getenv("BASIC_AUTH_PASSWORD"),
        timeout=int(os.getenv("DEFAULT_TIMEOUT", 30))
    )

@pytest.fixture(scope="session")
def auth_helper(config):
    return AuthHelper(config)

@pytest.fixture
def auth(auth_helper):
    return auth_helper.get_auth()

@pytest.fixture
def headers(auth_helper):
    return auth_helper.build_headers()