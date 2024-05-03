from pydantic import BaseModel

class CartItem(BaseModel):
    name: str
    quantity: int

class UserCart(BaseModel):
    items: list[CartItem]


class BuyRequest(BaseModel):
    pharmacy_name: str
    items: list[CartItem]

class RemoveRequest(BaseModel):
    pharmacy_name: str
    items: list[str]