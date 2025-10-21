from dataclasses import dataclass

@dataclass
class Config:
    base_url: str
    basic_auth_username: str = None
    basic_auth_password: str = None
    timeout: int = 30
