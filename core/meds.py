from core.database import pharmacy
from models.cart import CartItem

def pharmacy_helper(p) -> dict:
    return {
        "id": str(p["_id"]),
        "fullname": p["name"],
        "items": p["items"],
        "owner": p["owner"],
    }


async def SearchMeds(meds: list[CartItem]) -> dict:
    query = {
        "$and": [
            {
                "items": {
                    "$elemMatch": {
                        "name": m.name,
                        "quantity": {"$gte": m.quantity},
                    }
                }
            }
            for m in meds
        ]
    }
    results = pharmacy.find(query)
    results = await results.to_list(length=10)
    print(results)
    return {"results": [pharmacy_helper(r) for r in results]}

async def ListMeds(pharmacy_name: str) -> dict:
    query = {"name": pharmacy_name}
    results = await pharmacy.find_one(query)
    return pharmacy_helper(results)

async def FindPharmacy(owner: str) -> dict:
    query = {"owner": owner}
    results = await pharmacy.find_one(query)
    return pharmacy_helper(results)

async def BuyMeds(pharmacy_name: str, meds: list[CartItem]) -> dict:
    results = await SearchMeds(meds)
    results = results["results"]
    for r in results:
        if r["fullname"] == pharmacy_name:
            query = {"name": pharmacy_name}
            update = {"$inc": {"items.$[elem].quantity": -m.quantity for m in meds}}
            out = await pharmacy.update_one(
                query,
                update,
                array_filters=[{"elem.name": {"$in": [m.name for m in meds]}}],
            )
            return {"success": out.modified_count > 0}
    return {"success": False}


async def UpdateMeds(pharmacy_name, meds: list[CartItem]) -> dict:
    query = {"name": pharmacy_name}
    update = {"$set": {"items.$[elem].quantity": m.quantity for m in meds}}
    out = await pharmacy.update_one(
        query,
        update,
        array_filters=[{"elem.name": {"$in": [m.name for m in meds]}}],
    )
    return {"success": out.modified_count > 0}


async def CreateMeds(pharmacy_name, meds: list[CartItem]) -> dict:
    query = {
        "name": pharmacy_name,
        "items.name": {"$nin": [m.name for m in meds]}
    }
    update = {
        "$push": {
            "items": {
                "$each": [
                    {"name": m.name, "quantity": m.quantity}
                    for m in meds
                ]
            }
        }
    }
    out = await pharmacy.update_one(
        query,
        update,
    )
    return {"success": out.modified_count > 0}


async def RemoveMeds(pharmacy_name, meds: list[str]) -> dict:
    query = {"name": pharmacy_name}
    update = {"$pull": {"items": {"name": m for m in meds}}}
    out = await pharmacy.update_one(
        query,
        update,
    )
    return {"success": out.modified_count > 0}
