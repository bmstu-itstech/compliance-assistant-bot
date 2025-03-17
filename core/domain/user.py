from dataclasses import dataclass

from core.domain.role import Role


@dataclass
class User:
    id: int
    is_bot_blocked: bool
    role: Role
    username: str | None = None
