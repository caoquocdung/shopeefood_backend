import enum
import datetime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, ForeignKey,
    DECIMAL, Enum, Float
)

Base = declarative_base()

# -------- ENUMS --------
class UserRole(enum.Enum):
    customer = 'customer'
    shipper = 'shipper'
    admin = 'admin'
    merchant = 'merchant'

class OrderStatus(enum.Enum):
    pending = 'pending'
    accepted = 'accepted'
    preparing = 'preparing'
    delivering = 'delivering'
    delivered = 'delivered'
    cancelled = 'cancelled'

class VoucherStatus(enum.Enum):
    active = 'active'
    expired = 'expired'
    disabled = 'disabled'

class WalletTransType(enum.Enum):
    topup = 'topup'
    payment = 'payment'
    refund = 'refund'
    withdraw = 'withdraw'

# -------- USERS (firebase UID) --------
class User(Base):
    __tablename__ = "users"
    uid = Column(String(128), primary_key=True)   # Firebase UID
    email = Column(String(100), unique=True, index=True)
    name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.customer)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # relationships
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    # orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    wallet = relationship("Wallet", uselist=False, back_populates="user", cascade="all, delete-orphan")
    search_history = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")
    # Quan hệ với orders với tư cách là khách hàng
    orders_as_customer = relationship(
        "Order",
        back_populates="user",
        foreign_keys="Order.user_uid",
        cascade="all, delete-orphan"
    )
    # Quan hệ với orders với tư cách là shipper
    orders_as_shipper = relationship(
        "Order",
        back_populates="shipper",
        foreign_keys="Order.shipper_uid",
        cascade="all, delete-orphan"
    )

# -------- ADDRESSES --------
class Address(Base):
    __tablename__ = "addresses"
    address_id = Column(Integer, primary_key=True, index=True)
    user_uid = Column(String(128), ForeignKey('users.uid'))
    label = Column(String(50))
    receiver = Column(String(100))
    phone = Column(String(20))
    address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # relationships
    user = relationship("User", back_populates="addresses")

# -------- RESTAURANTS --------
class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id = Column(Integer, primary_key=True, index=True)
    owner_uid = Column(String(128), ForeignKey('users.uid'))
    name = Column(String(255), nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    open_time = Column(String(20))
    close_time = Column(String(20))
    status = Column(String(20), default='open')
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # relationships
    owner = relationship("User")
    menu_items = relationship("MenuItem", back_populates="restaurant", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="restaurant", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="restaurant", cascade="all, delete-orphan")
    vouchers = relationship("Voucher", back_populates="restaurant", cascade="all, delete-orphan")

# -------- MENU ITEMS --------
class MenuItem(Base):
    __tablename__ = "menu_items"
    item_id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10,2), nullable=False)
    image_url = Column(String(255))
    available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # relationships
    restaurant = relationship("Restaurant", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_item", cascade="all, delete-orphan")

# -------- ORDERS --------
class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    user_uid = Column(String(128), ForeignKey('users.uid'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'))
    shipper_uid = Column(String(128), ForeignKey('users.uid'), nullable=True)
    total_price = Column(DECIMAL(10,2))
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    address_id = Column(Integer, ForeignKey('addresses.address_id'), nullable=True)
    delivery_address = Column(Text)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # relationships
    user = relationship("User", back_populates="orders", foreign_keys=[user_uid])
    restaurant = relationship("Restaurant", back_populates="orders")
    shipper = relationship("User", foreign_keys=[shipper_uid])
    address = relationship("Address")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="order", cascade="all, delete-orphan")
    # Quan hệ với User (người đặt đơn)
    user = relationship(
        "User",
        back_populates="orders_as_customer",
        foreign_keys=[user_uid]
    )
    # Quan hệ với User (shipper)
    shipper = relationship(
        "User",
        back_populates="orders_as_shipper",
        foreign_keys=[shipper_uid]
    )
# -------- ORDER ITEMS --------
class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    item_id = Column(Integer, ForeignKey('menu_items.item_id'))
    quantity = Column(Integer, default=1)
    price = Column(DECIMAL(10,2))
    note = Column(Text)
    # relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")

# -------- REVIEWS --------
class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    user_uid = Column(String(128), ForeignKey('users.uid'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'))
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    # relationships
    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")
    order = relationship("Order", back_populates="reviews")

# -------- VOUCHERS --------
class Voucher(Base):
    __tablename__ = "vouchers"
    voucher_id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True)
    description = Column(Text)
    discount = Column(DECIMAL(10,2))
    min_order = Column(DECIMAL(10,2))
    max_discount = Column(DECIMAL(10,2))
    restaurant_id = Column(Integer, ForeignKey('restaurants.restaurant_id'), nullable=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    quantity = Column(Integer)
    status = Column(Enum(VoucherStatus), default=VoucherStatus.active)
    # relationships
    restaurant = relationship("Restaurant", back_populates="vouchers")

# -------- WALLETS --------
class Wallet(Base):
    __tablename__ = "wallets"
    wallet_id = Column(Integer, primary_key=True, index=True)
    user_uid = Column(String(128), ForeignKey('users.uid'), unique=True)
    balance = Column(DECIMAL(10,2), default=0)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # relationships
    user = relationship("User", back_populates="wallet")
    transactions = relationship("WalletTransaction", back_populates="wallet", cascade="all, delete-orphan")

# -------- WALLET TRANSACTIONS --------
class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    transaction_id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey('wallets.wallet_id'))
    type = Column(Enum(WalletTransType))
    amount = Column(DECIMAL(10,2))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.now)
    # relationships
    wallet = relationship("Wallet", back_populates="transactions")

# -------- SEARCH HISTORY --------
class SearchHistory(Base):
    __tablename__ = "search_history"
    search_id = Column(Integer, primary_key=True, index=True)
    user_uid = Column(String(128), ForeignKey('users.uid'))
    keyword = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.now)
    # relationships
    user = relationship("User", back_populates="search_history")
