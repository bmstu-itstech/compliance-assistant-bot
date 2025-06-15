from enum import StrEnum
from dataclasses import dataclass

from core import domain


@dataclass
class ThemeRecord:
    id: int | None
    name: str


class MaterialType(StrEnum):
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
    content: str
    description: str | None = None
