# models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    JSON,
    Table,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship
from sql.database import Base

# ----------------------------------------
# Table "Item"
# ----------------------------------------
class Item(Base):
    __tablename__ = "items"

    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255), nullable=False)

    item_Goals = Column(String(50), nullable=False) # ex. "weapon (+ type arme) / descendant"
    item_type = Column(String(50), nullable=False) # ex. "weapon (+ type arme) / descendant"
    item_capabilities = Column(Text, nullable=True) # "compétences / effectifs de l’arme"
    item_statistiques = Column(JSON, nullable=True) # ex. "ATK", "fire Rate", "HP"
    # no need for now
    # builds = relationship("Build", back_populates="item")

    def __repr__(self):
        return f"<Item(item_id={self.item_id}, name='{self.item_name}')>"


# ----------------------------------------
# Table "Modifier"
# ----------------------------------------
class Modifier(Base):
    __tablename__ = "modifiers"

    modifier_id = Column(Integer, primary_key=True, index=True)
    modifier_name = Column(String(255), nullable=False)

    modifier_type = Column(String(50), nullable=False)  # ex. "module, composant_ext, reacteur"
    modifier_statistiques = Column(JSON, nullable=True) # ex. " module stats"
    modifier_stack_id = Column(String(50), nullable=True)
    modifier_stack_description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Modifier(modifier_id={self.modifier_id}, name='{self.modifier_name}')>"

# ----------------------------------------
# Table "Build"
# ----------------------------------------
class Build(Base):
    __tablename__ = "builds"

    build_id = Column(Integer, primary_key=True, index=True)
    build_name = Column(String(255), nullable=True)

    # FK vers l'Item de base
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False)
    score_per_goal = Column(JSON, nullable=True)
    item = relationship("Item", back_populates="builds")
    modifiers = relationship("Modifier", secondary="build_modifiers", backref="builds")

    def __repr__(self):
        return f"<Build(build_id={self.build_id}, name='{self.build_name}')>"


# ----------------------------------------
# Table "BuildModifier"
# ----------------------------------------
build_modifiers_table = Table(
    "build_modifiers",
    Base.metadata,
    Column("build_id", Integer, ForeignKey("builds.build_id"), primary_key=True),
    Column("modifier_id", Integer, ForeignKey("modifiers.modifier_id"), primary_key=True),
    # Exemple d'un champ 'quantity' si on veut plusieurs exemplaires du même modifier
    Column("quantity", Integer, nullable=True, default=1),
)


# ----------------------------------------
# Table "User" (minimal definition)
# ----------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    photo_url = Column(String(255), nullable=True)


# ----------------------------------------
# Table "user_builds"
# ----------------------------------------
class UserBuild(Base):
    __tablename__ = "user_builds"

    build_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.id"), nullable=False)
    build_name = Column(String(255), nullable=False)
    build_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User")

    def __repr__(self):
        return f"<UserBuild(build_id={self.build_id}, name='{self.build_name}')>"
