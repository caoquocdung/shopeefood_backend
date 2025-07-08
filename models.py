import enum
import datetime
from sqlalchemy.orm import declarative_base, relationship, mapped_column
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
    DECIMAL,
    Enum,
    Float,
)

Base = declarative_base()


# -------- ENUMS --------
class UserRole(enum.Enum):
    customer = "customer"
    shipper = "shipper"
    admin = "admin"
    merchant = "merchant"


class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    banned = "banned"


class RestaurantStatus(enum.Enum):
    open = "open"
    closed = "closed"
    suspended = "suspended"


class RestaurantRequest(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class OrderStatus(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    preparing = "preparing"
    delivering = "delivering"
    delivered = "delivered"
    cancelled = "cancelled"


class VoucherStatus(enum.Enum):
    active = "active"
    expired = "expired"
    disabled = "disabled"


class DiscountType(enum.Enum):
    percentage = "percentage"
    fixed = "fixed"


class WalletTransType(enum.Enum):
    topup = "topup"
    payment = "payment"
    refund = "refund"
    withdraw = "withdraw"


# -------- USERS (firebase UID) --------
class User(Base):
    __tablename__ = "users"
    uid = mapped_column(String(128), primary_key=True)  # Firebase UID
    email = mapped_column(String(100), unique=True, index=True)
    name = mapped_column(String(100), nullable=True)
    phone = mapped_column(String(20), nullable=True)
    gender = mapped_column(String(10), nullable=True)
    birthday = mapped_column(DateTime, nullable=True)
    avatar_url = mapped_column(String(255), nullable=True)
    status = mapped_column(Enum(UserStatus), default=UserStatus.active)
    role = mapped_column(Enum(UserRole), default=UserRole.customer)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    # relationships
    addresses = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    reviews = relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )
    wallet = relationship(
        "Wallet", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    search_history = relationship(
        "SearchHistory", back_populates="user", cascade="all, delete-orphan"
    )
    # Quan hệ với orders với tư cách là khách hàng
    orders_as_customer = relationship(
        "Order",
        back_populates="user",
        foreign_keys="Order.user_uid",
        cascade="all, delete-orphan",
    )
    # Quan hệ với orders với tư cách là shipper
    orders_as_shipper = relationship(
        "Order",
        back_populates="shipper",
        foreign_keys="Order.shipper_uid",
        cascade="all, delete-orphan",
    )


# -------- ADDRESSES --------
class Address(Base):
    __tablename__ = "addresses"
    address_id = mapped_column(Integer, primary_key=True, index=True)
    user_uid = mapped_column(String(128), ForeignKey("users.uid"))
    label = mapped_column(String(50))
    receiver = mapped_column(String(100))
    phone = mapped_column(String(20))
    address = mapped_column(Text, nullable=False)
    latitude = mapped_column(Float, nullable=True)
    longitude = mapped_column(Float, nullable=True)
    is_default = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    # relationships
    user = relationship("User", back_populates="addresses")


# -------- RESTAURANTS --------
class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id = mapped_column(Integer, primary_key=True, index=True)
    owner_uid = mapped_column(String(128), ForeignKey("users.uid"))
    name = mapped_column(String(255), nullable=False)
    address = mapped_column(Text)
    phone = mapped_column(String(20))
    open_time = mapped_column(DateTime)
    close_time = mapped_column(DateTime)
    is_favorite = mapped_column(Boolean, default=False)
    description = mapped_column(Text)
    image_url = mapped_column(String(255))
    status = mapped_column(
        SqlEnum(RestaurantStatus, native_enum=False), default=RestaurantStatus.open
    )
    request = mapped_column(
        SqlEnum(RestaurantRequest, native_enum=False), default=RestaurantRequest.pending
    )
    rating = mapped_column(Float, default=0.0)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    # relationships
    owner = relationship("User")
    menu_items = relationship(
        "MenuItem", back_populates="restaurant", cascade="all, delete-orphan"
    )
    orders = relationship(
        "Order", back_populates="restaurant", cascade="all, delete-orphan"
    )
    reviews = relationship(
        "Review", back_populates="restaurant", cascade="all, delete-orphan"
    )
    # vouchers = relationship("Voucher", back_populates="restaurant", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"
    category_id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(255), nullable=False)
    description = mapped_column(Text)
    image_url = mapped_column(String(255))
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    # relationships
    menu_items = relationship(
        "MenuItem", back_populates="category", cascade="all, delete-orphan"
    )


# -------- MENU ITEMS --------
class MenuItem(Base):
    __tablename__ = "menu_items"
    item_id = mapped_column(Integer, primary_key=True, index=True)
    restaurant_id = mapped_column(Integer, ForeignKey("restaurants.restaurant_id"))
    category_id = mapped_column(Integer, ForeignKey("categories.category_id"))
    name = mapped_column(String(255), nullable=False)
    description = mapped_column(Text)
    price = mapped_column(DECIMAL(10, 2), nullable=False)
    available = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    # relationships
    category = relationship("Category", back_populates="menu_items")
    restaurant = relationship("Restaurant", back_populates="menu_items")
    order_items = relationship(
        "OrderItem", back_populates="menu_item", cascade="all, delete-orphan"
    )
    images = relationship(
        "MenuItemImage", back_populates="menu_item", cascade="all, delete-orphan"
    )
    cart_items = relationship(
        "CartItem", back_populates="menu_item", passive_deletes=True
    )


# -------- MENU ITEM IMAGES --------
class MenuItemImage(Base):
    __tablename__ = "menu_item_images"
    image_id = mapped_column(Integer, primary_key=True, index=True)
    item_id = mapped_column(Integer, ForeignKey("menu_items.item_id"))
    image_url = mapped_column(String(255), nullable=False)
    is_primary = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    # relationships
    menu_item = relationship("MenuItem", back_populates="images")


# -------- ORDERS --------
class Order(Base):
    __tablename__ = "orders"
    order_id = mapped_column(Integer, primary_key=True, index=True)
    user_uid = mapped_column(String(128), ForeignKey("users.uid"))
    restaurant_id = mapped_column(Integer, ForeignKey("restaurants.restaurant_id"))
    shipper_uid = mapped_column(String(128), ForeignKey("users.uid"), nullable=True)
    total_price = mapped_column(DECIMAL(10, 2))
    status = mapped_column(Enum(OrderStatus), default=OrderStatus.pending)
    address_id = mapped_column(
        Integer, ForeignKey("addresses.address_id"), nullable=True
    )
    delivery_address = mapped_column(Text)
    note = mapped_column(Text)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    # relationships
    user = relationship("User", back_populates="orders", foreign_keys=[user_uid])
    restaurant = relationship("Restaurant", back_populates="orders")
    shipper = relationship("User", foreign_keys=[shipper_uid])
    address = relationship("Address")
    order_items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    reviews = relationship(
        "Review", back_populates="order", cascade="all, delete-orphan"
    )
    # Quan hệ với User (người đặt đơn)
    user = relationship(
        "User", back_populates="orders_as_customer", foreign_keys=[user_uid]
    )
    # Quan hệ với User (shipper)
    shipper = relationship(
        "User", back_populates="orders_as_shipper", foreign_keys=[shipper_uid]
    )


# -------- ORDER ITEMS --------
class OrderItem(Base):
    __tablename__ = "order_items"
    order_item_id = mapped_column(Integer, primary_key=True, index=True)
    order_id = mapped_column(Integer, ForeignKey("orders.order_id"))
    item_id = mapped_column(Integer, ForeignKey("menu_items.item_id"))
    quantity = mapped_column(Integer, default=1)
    price = mapped_column(DECIMAL(10, 2))
    note = mapped_column(Text)
    # relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")


# -------- REVIEWS --------
class Review(Base):
    __tablename__ = "reviews"
    review_id = mapped_column(Integer, primary_key=True, index=True)
    user_uid = mapped_column(String(128), ForeignKey("users.uid"))
    restaurant_id = mapped_column(Integer, ForeignKey("restaurants.restaurant_id"))
    order_id = mapped_column(Integer, ForeignKey("orders.order_id"))
    rating = mapped_column(Integer)
    comment = mapped_column(Text)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    # relationships
    user = relationship("User", back_populates="reviews")
    restaurant = relationship("Restaurant", back_populates="reviews")
    order = relationship("Order", back_populates="reviews")


# -------- VOUCHERS --------
class Voucher(Base):
    __tablename__ = "vouchers"
    voucher_id = mapped_column(Integer, primary_key=True, index=True)
    code = mapped_column(String(20), unique=True)
    title = mapped_column(Text)
    discount_type = mapped_column(
        Enum(DiscountType), default=DiscountType.percentage, nullable=False
    )
    discount_value = mapped_column(DECIMAL(10, 2), nullable=False)
    min_order = mapped_column(DECIMAL(10, 2))
    max_discount = mapped_column(DECIMAL(10, 2))
    start_date = mapped_column(DateTime)
    end_date = mapped_column(DateTime)
    usage_limit = mapped_column(Integer)
    used_count = mapped_column(Integer, default=0)
    seller_uid = mapped_column(String(128), ForeignKey("users.uid"))
    status = mapped_column(Enum(VoucherStatus), default=VoucherStatus.active)
    created_by_admin = mapped_column(Boolean, default=False, nullable=False)

    seller = relationship("User")


# -------- WALLETS --------
class Wallet(Base):
    __tablename__ = "wallets"
    wallet_id = mapped_column(Integer, primary_key=True, index=True)
    user_uid = mapped_column(String(128), ForeignKey("users.uid"), unique=True)
    balance = mapped_column(DECIMAL(10, 2), default=0)
    updated_at = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    # relationships
    user = relationship("User", back_populates="wallet")
    transactions = relationship(
        "WalletTransaction", back_populates="wallet", cascade="all, delete-orphan"
    )


# -------- WALLET TRANSACTIONS --------
class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    transaction_id = mapped_column(Integer, primary_key=True, index=True)
    wallet_id = mapped_column(Integer, ForeignKey("wallets.wallet_id"))
    type = mapped_column(Enum(WalletTransType))
    amount = mapped_column(DECIMAL(10, 2))
    description = mapped_column(Text)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    # relationships
    wallet = relationship("Wallet", back_populates="transactions")


# -------- SEARCH HISTORY --------
class SearchHistory(Base):
    __tablename__ = "search_history"
    search_id = mapped_column(Integer, primary_key=True, index=True)
    user_uid = mapped_column(String(128), ForeignKey("users.uid"))
    keyword = mapped_column(String(255))
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    # relationships
    user = relationship("User", back_populates="search_history")


class CartItem(Base):
    __tablename__ = "cart_items"
    cart_item_id = mapped_column(Integer, primary_key=True, index=True)
    user_uid = mapped_column(String(128), ForeignKey("users.uid"))
    restaurant_id = mapped_column(Integer, ForeignKey("restaurants.restaurant_id"))
    item_id = mapped_column(
        Integer,
        ForeignKey("menu_items.item_id", ondelete="CASCADE"),
    )
    quantity = mapped_column(Integer, default=1)
    note = mapped_column(Text)
    created_at = mapped_column(DateTime, default=datetime.datetime.now)
    updated_at = mapped_column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    user = relationship("User")
    restaurant = relationship("Restaurant")
    menu_item = relationship("MenuItem")
