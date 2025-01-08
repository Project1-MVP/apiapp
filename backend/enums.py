from enum import Enum

class OrderStatus(Enum):
    PROVISIONING = 'Provisioning'
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'
    
    @classmethod
    def choices(cls):
        # Generate choices in the format required by Django
        return [(tag.name, tag.value) for tag in cls]

class PaymentStatus(Enum):
    PAID = 'Paid'
    UNPAID = 'Pending'
    REFUNDED = 'Refunded'
    COMPLETED = 'Completed'
    FAILED = 'Failed'
        
    @classmethod
    def choices(cls):
        # Generate choices in the format required by Django
        return [(tag.name, tag.value) for tag in cls]

class UserRoles(Enum):
    ADMIN = 'Admin'
    STAFF = 'Staff'
    SALES = 'Sales'

    @classmethod
    def choices(cls):
        # Generate choices in the format required by Django
        return [(tag.name, tag.value) for tag in cls]

class OrderType(Enum):
    PROVISIONING = 'Provisioning'
    SALE = 'Sale'
    BACKORDER = 'Backorder'
    RETURN = 'Return'
    EXCHANGE = 'Exchange'
    TRIAL = 'Trial'
    GIFT = 'Gift'
    PROMOTIONAL = 'Promotional'
    STOCK_ADJUSTMENT = 'Stock Adjustment'
    INTERNAL_TRANSFER = 'Internal Transfer'
    PURCHASE_ORDER = 'Purchase Order'
    STOCK_DAMAGE = 'Stock Damage'
    STOCK_RETURN = 'Stock Return'
    STOCK_ENTRY = 'Stock Entry'

    @classmethod
    def choices(cls):
        # Generate choices in the format required by Django
        return [(tag.name, tag.value) for tag in cls]

class PaymentType(Enum):
    CASH = 'Cash'
    POS = 'POS'
    UPI = 'UPI'
    CHECK = 'Check'
    COMPANY_CREDIT = 'Company Credit'

    @classmethod
    def choices(cls):
        # Generate choices in the format required by Django
        return [(tag.name, tag.value) for tag in cls]

class DispatchType(Enum):
    STORE = 'Store'
    SHIPPING = 'Shipping'

    @classmethod
    def choices(cls):
        # Generate choices in the format required by Django
        return [(tag.name, tag.value) for tag in cls]

class UnitType(Enum):
    KG = 'Kilogram'
    METER = 'Meter'
    LITRE = 'Litre'
    PACK = 'Pack'
    PIECE = 'Piece'

    @classmethod
    def choices(cls):
        # Generate choices in the format required by Django
        return [(tag.name, tag.value) for tag in cls]