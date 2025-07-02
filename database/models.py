from sqlalchemy import (
    Column, Integer, Text, ForeignKey, func, Enum as SqlEnum,
    CheckConstraint, DECIMAL, ForeignKeyConstraint, text
)
from sqlalchemy.dialects.postgresql import VARCHAR
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

model_base = declarative_base()

# role user
class UserRole(str, Enum):
    ADMIN = 'ADMIN' # Admun     : bisa delete, ganti harga, dll
    USER = 'USER'   # Karyawan  : bisa input orderan, update orderan
    GUEST = 'GUEST' # Client    : hanya bisa read pricelist

class TUser(model_base):
    __tablename__ = 't_user'

    u_id = Column(VARCHAR(32), primary_key=True)
    u_name = Column(Text, nullable=False)
    u_email = Column(Text, nullable=False, unique=True)
    u_password = Column(Text, nullable=False)
    u_code = Column(Text)
    u_role = Column(SqlEnum(UserRole), nullable=False)
    u_time = Column(Integer, server_default=text("EXTRACT(EPOCH FROM now())::int"))

    # child
    orders = relationship("TOrder", back_populates="user")

class TPower(model_base):
    __tablename__ = 't_power'

    p_id = Column(VARCHAR(32), primary_key=True)
    p_power = Column(Integer, nullable=False)

    # child
    pricelistes = relationship("TPriceList", back_populates="power")
    order_articles = relationship("TOrderArticle", back_populates="power")

class TSpec(model_base):
    __tablename__ = 't_spec'

    s_id = Column(VARCHAR(32), primary_key=True)
    s_spec = Column(Text, nullable=False)

    # child
    pricelistes = relationship("TPriceList", back_populates="spec")

class TPriceList(model_base):
    __tablename__ = 't_price_list'

    p_id = Column(VARCHAR(32), ForeignKey('t_power.p_id'), primary_key=True)
    s_id = Column(VARCHAR(32), ForeignKey('t_spec.s_id'), primary_key=True)
    pl_price = Column(DECIMAL(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint('pl_price >= 0', name='check_pl_price_positive'),
    )

    # parent
    power = relationship("TPower", back_populates="pricelistes")
    spec = relationship("TSpec", back_populates="pricelistes")
    # child
    order_specs = relationship("TOrderSpec", back_populates="pricelist", overlaps="order_article,order_specs")

class TOrder(model_base):
    __tablename__ = 't_order'

    o_id = Column(VARCHAR(32), primary_key=True)
    u_id = Column(VARCHAR(32), ForeignKey('t_user.u_id'), nullable=False)
    o_description = Column(Text)
    o_time = Column(Integer, nullable=False, server_default=text("EXTRACT(EPOCH FROM now())::int"))

    # parent
    user = relationship("TUser", back_populates="orders")
    # child
    order_articles = relationship("TOrderArticle", back_populates="order")

class TOrderArticle(model_base):
    __tablename__ = 't_order_article'

    oa_id = Column(VARCHAR(32), primary_key=True)
    p_id = Column(VARCHAR(32), ForeignKey('t_power.p_id'), primary_key=True)
    o_id = Column(VARCHAR(32), ForeignKey('t_order.o_id'), nullable=False)
    opl_description = Column(Text)

    # parent
    power = relationship("TPower", back_populates="order_articles")
    order = relationship("TOrder", back_populates="order_articles")
    # child
    order_specs = relationship("TOrderSpec", back_populates="order_article", overlaps="pricelist,order_specs")

class TOrderSpec(model_base):
    __tablename__ = 't_order_spec'

    oa_id = Column(VARCHAR(32), nullable=False, primary_key=True)
    s_id = Column(VARCHAR(32), nullable=False, primary_key=True)
    p_id = Column(VARCHAR(32), nullable=False)
    os_price = Column(DECIMAL(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint('os_price >= 0', name='check_os_price_positive'),
        ForeignKeyConstraint(['oa_id', 'p_id'], ['t_order_article.oa_id', 't_order_article.p_id']),
        ForeignKeyConstraint(['p_id', 's_id'], ['t_price_list.p_id', 't_price_list.s_id']),
    )

    # parent
    order_article = relationship("TOrderArticle", back_populates="order_specs", overlaps="order_specs,pricelist")
    pricelist = relationship("TPriceList", back_populates="order_specs", overlaps="order_specs,pricelist")