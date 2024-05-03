from fastapi import APIRouter

from core.database import BuyMeds, CreateMeds, RemoveMeds, SearchMeds, UpdateMeds
from models.cart import BuyRequest, RemoveRequest, UserCart

router=APIRouter(prefix="/cart")

@router.post("/price")
async def price(cart: UserCart):
    search_results = await SearchMeds(cart.items)
    return search_results

@router.post("/buy")
async def buy(cart: BuyRequest):
    out=await BuyMeds(cart.pharmacy_name, cart.items)
    return out

@router.post("/update")
async def update(cart: BuyRequest):
    out=await UpdateMeds(cart.pharmacy_name, cart.items)
    return out

@router.post("/remove")
async def remove(cart: RemoveRequest):
    out=await RemoveMeds(cart.pharmacy_name, cart.items)
    return out


@router.post("/create")
async def create(cart: BuyRequest):
    out=await CreateMeds(cart.pharmacy_name, cart.items)
    return out