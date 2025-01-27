from enum import Enum

class OrderTypeEnum(str, Enum):
    CONSUMPTION = "consumption"
    SALE = "sale"
    RETURN = "return"
    PURCHASE = "purchase"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"
    DAMAGE = "damage"
    CHECKIN = "checkin"
    EXPIRATION = "expiration"

class MeasurementUnitsEnum(str, Enum):
    UNIT = "unit"
    KG = "kg"
    LITER = "liter"
    GRAM = "gram"
    MILLILITER = "milliliter"
    BOX = "box"
    CARTON = "carton"
    DOZEN = "dozen"

class OrderStatusEnum(str, Enum):
    PROVISIONING = "provisioning"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PENDING = "pending"
    ON_HOLD = "on_hold"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    RETURNED = "returned"
    
class PaymentTypeEnum(str, Enum):
    CASH = "cash"
    UPI = "upi"
    CARD = "card"

class Salutation(str, Enum):
    MR = "Mr"
    MISS = "Miss"
    MRS = "Mrs"

class QRCodeType(str, Enum):
    INTERNAL_UPIC = "Internal UPIC"
    EPS = "EPS"
    UPC = "UPC"

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    SUPER_ADMIN = "super_admin"