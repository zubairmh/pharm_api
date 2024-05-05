from typing import Annotated
from fastapi import APIRouter, Depends

from core.auth import get_current_active_user
from core.meds import AllPharmacies, BuyMeds, CreateMeds, ListMeds, RemoveMeds, SearchMeds, UpdateMeds
from models.auth import User
from models.cart import AddItem, BuyRequest, RemoveRequest, UpdateItems, UserCart

router=APIRouter(prefix="/cart")

@router.get("/list_pharmacies")
async def list_pharmacies():
    results=await AllPharmacies()
    return results

@router.post("/price")
async def price(cart: UserCart):
    search_results = await SearchMeds(cart.items)
    return search_results

@router.post("/buy")
async def buy(cart: BuyRequest):
    out=await BuyMeds(cart.pharmacy_name, cart.items)
    return out

@router.post("/list")
async def list_meds(pharmacy_name: str):
    out=await ListMeds(pharmacy_name)
    return out

@router.post("/update")
async def update(cart: UpdateItems):
    out=await UpdateMeds(cart.pharmacy_name, cart.items)
    return out

@router.post("/remove")
async def remove(cart: RemoveRequest):
    out=await RemoveMeds(cart.pharmacy_name, cart.items)
    return out


@router.post("/create")
async def create(cart: UpdateItems):
    out=await CreateMeds(cart.pharmacy_name, cart.items)
    return out