from sqlalchemy import (
    Column, Integer, Text, ForeignKey, Enum as SqlEnum,
    CheckConstraint, DECIMAL, ForeignKeyConstraint, text, Boolean
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

class UserStatus(str, Enum):
    NOT_ACTIVATED = 'NOT_ACTIVATED'
    ACTIVATED = 'ACTIVATED'
    LOCKED = 'LOCKED'
    DELETED = 'DELETED'

class OrderStatus(str, Enum):
    PROCESSING = "PROCESSING"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"
    FAILED = "FAILED"
    ON_HOLD = "ON_HOLD"

class TUser(model_base):
    __tablename__ = 't_user'

    u_id = Column(VARCHAR(32), primary_key=True)
    u_name = Column(Text, nullable=False)
    u_email = Column(Text, nullable=False, unique=True)
    u_password = Column(Text, nullable=False)
    u_code = Column(Text)
    u_role = Column(SqlEnum(UserRole), nullable=False, default=UserRole.USER)
    u_status = Column(SqlEnum(UserStatus), nullable=False)
    u_time = Column(Integer, server_default=text("EXTRACT(EPOCH FROM now())::int"))

    # child
    orders = relationship("TOrder", back_populates="user", cascade="all, delete-orphan")

class TPower(model_base):
    __tablename__ = 't_power'

    p_id = Column(VARCHAR(32), primary_key=True)
    p_power = Column(Integer, nullable=False, unique=True)
    p_unit = Column(Integer, nullable=False, default=0)

    # child
    pricelistes = relationship("TPriceList", back_populates="power", cascade="all, delete-orphan")
    order_articles = relationship("TOrderArticle", back_populates="power")

class TSpec(model_base):
    __tablename__ = 't_spec'

    s_id = Column(VARCHAR(32), primary_key=True)
    s_spec = Column(Text, nullable=False, unique=True)
    s_corrective = Column(Boolean, default=False)

    # child
    pricelistes = relationship("TPriceList", back_populates="spec", cascade="all, delete-orphan")

class TPriceList(model_base):
    __tablename__ = 't_price_list'

    p_id = Column(VARCHAR(32), ForeignKey('t_power.p_id', ondelete='CASCADE', onupdate='RESTRICT'), primary_key=True)
    s_id = Column(VARCHAR(32), ForeignKey('t_spec.s_id', ondelete='CASCADE', onupdate='RESTRICT'), primary_key=True)
    pl_price = Column(DECIMAL(10, 2), nullable=False)
    pl_description = Column(Text)
    __table_args__ = (
        CheckConstraint('pl_price >= 0', name='check_pl_price_positive'),
    )

    # parent
    power = relationship("TPower", back_populates="pricelistes")
    spec = relationship("TSpec", back_populates="pricelistes")
    # child
    order_specs = relationship("TOrderSpec", back_populates="pricelist", overlaps="order_article,order_specs", cascade="all, delete-orphan")

class TOrder(model_base):
    __tablename__ = 't_order'

    o_id = Column(VARCHAR(32), primary_key=True)
    u_id = Column(VARCHAR(32), ForeignKey('t_user.u_id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)
    o_description = Column(Text, nullable=False)
    o_time = Column(Integer, nullable=False, server_default=text("EXTRACT(EPOCH FROM now())::int"))
    o_status = Column(SqlEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)

    # parent
    user = relationship("TUser", back_populates="orders")
    # child
    order_articles = relationship("TOrderArticle", back_populates="order", cascade="all, delete-orphan")

class TOrderArticle(model_base):
    __tablename__ = 't_order_article'

    oa_id = Column(VARCHAR(32), primary_key=True)
    p_id = Column(VARCHAR(32), ForeignKey('t_power.p_id', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
    o_id = Column(VARCHAR(32), ForeignKey('t_order.o_id', ondelete='CASCADE', onupdate='RESTRICT'), nullable=False)
    oa_power = Column(Integer, nullable=False)
    oa_description = Column(Text, nullable=False)

    # parent
    power = relationship("TPower", back_populates="order_articles")
    order = relationship("TOrder", back_populates="order_articles")
    # child
    order_specs = relationship("TOrderSpec", back_populates="order_article", overlaps="pricelist,order_specs", cascade="all, delete-orphan")

class TOrderSpec(model_base):
    __tablename__ = 't_order_spec'

    oa_id = Column(VARCHAR(32), nullable=False, primary_key=True)
    s_id = Column(VARCHAR(32), nullable=False, primary_key=True)
    p_id = Column(VARCHAR(32), nullable=False)
    os_price = Column(DECIMAL(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint('os_price >= 0', name='check_os_price_positive'),
        ForeignKeyConstraint(['oa_id', 'p_id'], ['t_order_article.oa_id', 't_order_article.p_id'], ondelete='CASCADE', onupdate='RESTRICT'),
        ForeignKeyConstraint(['p_id', 's_id'], ['t_price_list.p_id', 't_price_list.s_id'], ondelete='RESTRICT', onupdate='RESTRICT'),
    )

    # parent
    order_article = relationship("TOrderArticle", back_populates="order_specs", overlaps="order_specs,pricelist")
    pricelist = relationship("TPriceList", back_populates="order_specs", overlaps="order_specs,pricelist")