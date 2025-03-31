from enum import Enum
from dataclasses import dataclass

from core import domain


@dataclass
class ThemeRecord:
    id: int | None
    name: str
    materials: list["MaterialRecord"] | None


class MaterialType(str, Enum):
    LAW               = "law"
    JUDICIAL_PRACTICE = "judicial_practice"
    CASE              = "case"
    ADVICE            = "advice"


@dataclass
class MaterialRecord:
    id: int | None
    name: str
    codex: domain.Codex
    material_type: MaterialType
    themes: list["ThemeRecord"]
    content: str
    description: str | None = None
