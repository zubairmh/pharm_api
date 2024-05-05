from pydantic import BaseModel


class AddItem(BaseModel):
    name: str
    quantity: int
    price: int


class UpdateItems(BaseModel):
    pharmacy_name: str
    items: list[AddItem]


class CartItem(BaseModel):
    name: str
    quantity: int

class BuyRequest(BaseModel):
    pharmacy_name: str
    items: list[CartItem]


class UserCart(BaseModel):
    items: list[CartItem]


class RemoveRequest(BaseModel):
    pharmacy_name: str
    items: list[str]
