from sqlalchemy import (
    create_engine, Column, Integer, Text, ForeignKey, func, Enum as SqlEnum,
    CheckConstraint, DECIMAL, ForeignKeyConstraint, text
)
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends
import config
from enum import Enum

database_engine = create_engine(config.URL_DATABASE)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=database_engine)

model_base = declarative_base()

# Enum untuk role user
class UserRole(str, Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'
    GUEST = 'GUEST'

class TUser(model_base):
    __tablename__ = 't_user'

    u_id = Column(VARCHAR(32), primary_key=True)
    u_name = Column(Text, nullable=False)
    u_email = Column(Text, nullable=False, unique=True)
    u_password = Column(Text, nullable=False)
    u_code = Column(Text)
    u_role = Column(SqlEnum(UserRole), nullable=False)
    u_time = Column(Integer, server_default=text("EXTRACT(EPOCH FROM now())::int"))

    orders = relationship("TOrder", back_populates="user")

class TPower(model_base):
    __tablename__ = 't_power'

    p_id = Column(VARCHAR(32), primary_key=True)
    p_kw = Column(Integer, nullable=False)

    articles = relationship("TArticle", back_populates="power")
    orders = relationship("TOrder", back_populates="power")

class TSpec(model_base):
    __tablename__ = 't_spec'

    s_id = Column(VARCHAR(32), primary_key=True)
    s_kw = Column(Text, nullable=False)

    articles = relationship("TArticle", back_populates="spec")

class TArticle(model_base):
    __tablename__ = 't_article'

    p_id = Column(VARCHAR(32), ForeignKey('t_power.p_id'), primary_key=True)
    s_id = Column(VARCHAR(32), ForeignKey('t_spec.s_id'), primary_key=True)
    a_name = Column(Text)
    a_description = Column(Text)
    a_price = Column(DECIMAL(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint('a_price >= 0', name='check_a_price_positive'),
    )

    power = relationship("TPower", back_populates="articles")
    spec = relationship("TSpec", back_populates="articles")
    order_specs = relationship("TOrderSpec", back_populates="article")

class TOrder(model_base):
    __tablename__ = 't_order'

    o_id = Column(VARCHAR(32), primary_key=True)
    p_id = Column(VARCHAR(32), ForeignKey('t_power.p_id'), primary_key=True)
    u_id = Column(VARCHAR(32), ForeignKey('t_user.u_id'), nullable=False)
    o_name = Column(Text)
    o_description = Column(Text)
    o_time = Column(Integer, nullable=False, server_default=text("EXTRACT(EPOCH FROM now())::int"))

    user = relationship("TUser", back_populates="orders")
    power = relationship("TPower", back_populates="orders")
    order_specs = relationship("TOrderSpec", back_populates="order")

class TOrderSpec(model_base):
    __tablename__ = 't_order_spec'

    os_id = Column(VARCHAR(32), primary_key=True)
    o_id = Column(VARCHAR(32), nullable=False)
    p_id = Column(VARCHAR(32), nullable=False)
    s_id = Column(VARCHAR(32), nullable=False)
    os_price = Column(DECIMAL(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint('os_price >= 0', name='check_os_price_positive'),
        ForeignKeyConstraint(
            ['o_id', 'p_id'], ['t_order.o_id', 't_order.p_id']
        ),
        ForeignKeyConstraint(
            ['p_id', 's_id'], ['t_article.p_id', 't_article.s_id']
        ),
    )

    order = relationship("TOrder", back_populates="order_specs")
    article = relationship("TArticle", back_populates="order_specs")

# Create all tables
model_base.metadata.create_all(bind=database_engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]