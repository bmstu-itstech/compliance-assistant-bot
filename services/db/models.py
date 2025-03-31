from datetime import datetime

from sqlalchemy import Column, BigInteger, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship

from core import domain
from services.db.base import Base


class BaseModel(Base):
    __abstract__ = True

    id         = Column(BigInteger, primary_key=True)
    created_on = Column(DateTime,   default=datetime.now)
    updated_on = Column(DateTime,   default=datetime.now, onupdate=datetime.now)


class Material(BaseModel):
    __tablename__ = "materials"

    name          = Column(Text,                      nullable=False)
    description   = Column(Text,                      nullable=True)
    codex         = Column(Enum(domain.Codex),        nullable=False)
    material_type = Column(Enum(domain.MaterialType), nullable=False)
    themes        = relationship('Theme', secondary='material_themes', back_populates='materials')
    content       = Column(Text,                      nullable=False)

    @classmethod
    def from_domain(cls, material: domain.MaterialRecord) -> "Material":
        return Material(
            name=material.name,
            description=material.description,
            codex=material.codex,
            material_type=material.material_type,
            content=material.content,
        )

    def to_domain(self) -> domain.MaterialRecord:
        return domain.MaterialRecord(
            id=self.id,
            name=self.name,
            description=self.description,
            codex=self.codex,
            material_type=self.material_type,
            themes=[theme.to_domain() for theme in self.themes],
            content=self.content,
        )


class Theme(BaseModel):
    __tablename__ = "themes"

    name      = Column(Text, nullable=False)
    materials = relationship('Material', secondary='material_themes', back_populates='themes')

    @classmethod
    def from_domain(cls, theme: domain.ThemeRecord) -> "Theme":
        return Theme(name=theme.name)

    def to_domain(self) -> domain.ThemeRecord:
        return domain.ThemeRecord(
            id=self.id,
            name=self.name,
            materials=[],
            # materials=[material.to_domain() for material in self.materials],
        )


class MaterialTheme(Base):
    __tablename__ = "material_themes"

    id          = Column(BigInteger, primary_key=True)
    material_id = Column(BigInteger, ForeignKey('materials.id'))
    theme_id    = Column(BigInteger, ForeignKey('themes.id'))
