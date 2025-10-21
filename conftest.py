import os
import pytest
import requests
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

@pytest.fixture
def vcn_token(config, auth, headers):
    url = f"{config.base_url}/vcns"
    resp = requests.post(url, headers=headers, auth=auth, timeout=config.timeout)
    assert resp.status_code in (200, 201), f"Failed to create VCN: {resp.status_code} {resp.text}"
    token = resp.json()["vcn"]["token"]
    yield token

    cleanup_url = f"{config.base_url}/vcns/{token}/deactivate"
    requests.post(cleanup_url, headers=headers, auth=auth, timeout=config.timeout)