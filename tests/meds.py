from core.meds import BuyMeds
import pytest
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_BuyMeds():
    # Mock the necessary dependencies
    pharmacy = MagicMock()
    pharmacy.find.return_value.to_list.return_value = [
        {
            "_id": "1",
            "name": "Pharmacy A",
            "items": [
                {"name": "Medicine A", "quantity": 10},
                {"name": "Medicine B", "quantity": 5},
            ],
            "owner": "Owner A",
        },
        {
            "_id": "2",
            "name": "Pharmacy B",
            "items": [
                {"name": "Medicine C", "quantity": 8},
                {"name": "Medicine D", "quantity": 3},
            ],
            "owner": "Owner B",
        },
    ]
    pharmacy.update_one.return_value.modified_count = 1

    # Call the function with sample data
    pharmacy_name = "Pharmacy A"
    meds = [
        {"name": "Medicine A", "quantity": 2},
        {"name": "Medicine B", "quantity": 3},
    ]
    result = await BuyMeds(pharmacy_name, meds)

    # Assert the expected result
    assert result == {"success": True}

    # Assert the mock calls
    pharmacy.find.assert_called_once_with(
        {
            "$and": [
                {
                    "items": {
                        "$elemMatch": {
                            "name": "Medicine A",
                            "quantity": {"$gte": 2},
                        }
                    }
                },
                {
                    "items": {
                        "$elemMatch": {
                            "name": "Medicine B",
                            "quantity": {"$gte": 3},
                        }
                    }
                },
            ]
        }
    )
    pharmacy.update_one.assert_called_once_with(
        {"name": "Pharmacy A"},
        {"$inc": {"items.$[elem].quantity": -1}},
        array_filters=[
            {"elem.name": {"$in": ["Medicine A", "Medicine B"]}}
        ],
    )