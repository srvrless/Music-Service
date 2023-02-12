import json
from uuid import uuid4

import pytest


async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "nickname": "nickname",
        "email": "example@gmail.com",
        "is_active": True,
    }
    user_data_updated = {
        "nickname": "nickname",
        "email": "example@gmail.com",
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["nickname"] == user_data_updated["nickname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_update_user_check_one_is_updated(
    client, create_user_in_database, get_user_from_database
):
    user_data_1 = {
        "user_id": uuid4(),
        "nickname": "nickname",
        "email": "example@gmail.com",
        "is_active": True,
    }
    user_data_2 = {
        "user_id": uuid4(),
        "nickname": "nickname",
        "surname": "Ivanov",
        "email": "example@gmail.com",
        "is_active": True,
    }
    user_data_3 = {
        "user_id": uuid4(),
        "nickname": "nickname",
        "surname": "Petr",
        "email": "example@gmail.com",
        "is_active": True,
    }
    user_data_updated = {
        "nickname": "nickname",
        "email": "example@gmail.com",
    }
    for user_data in [user_data_1, user_data_2, user_data_3]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data_1["user_id"])
    users_from_db = await get_user_from_database(user_data_1["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["nickname"] == user_data_updated["nickname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data_1["is_active"]
    assert user_from_db["user_id"] == user_data_1["user_id"]

    # check other users that data has not been changed
    users_from_db = await get_user_from_database(user_data_2["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["nickname"] == user_data_2["nickname"]
    assert user_from_db["email"] == user_data_2["email"]
    assert user_from_db["is_active"] is user_data_2["is_active"]
    assert user_from_db["user_id"] == user_data_2["user_id"]

    users_from_db = await get_user_from_database(user_data_3["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["nickname"] == user_data_3["nickname"]
    assert user_from_db["email"] == user_data_3["email"]
    assert user_from_db["is_active"] is user_data_3["is_active"]
    assert user_from_db["user_id"] == user_data_3["user_id"]


@pytest.mark.parametrize(
    "user_data_updated, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": "At least one parameter for user update info should be provided"
            },
        ),
        ({"nickname": "123"}, 422, {"detail": "nickname should contains only letters"}),
        (
            {"email": ""},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address",
                        "type": "value_error.email",
                    }
                ]
            },
        ),
        (
            {"nickname": ""},
            422,
            {
                "detail": [
                    {
                        "loc": ["body", "nickname"],
                        "msg": "ensure this value has at least 1 characters",
                        "type": "value_error.any_str.min_length",
                        "ctx": {"limit_value": 1},
                    }
                ]
            },
        ),
    ],
)
async def test_update_user_validation_error(
    client,
    create_user_in_database,
    get_user_from_database,
    user_data_updated,
    expected_status_code,
    expected_detail,
):
    user_data = {
        "user_id": uuid4(),
        "nickname": "nickname",
        "email": "example@gmail.com",
        "is_active": True,
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}", data=json.dumps(user_data_updated)
    )
    assert resp.status_code == expected_status_code
    resp_data = resp.json()
    assert resp_data == expected_detail


async def test_update_user_id_validation_error(client):
    user_data_updated = {
        "nickname": "nickname",
        "email": "example@gmail.com",
    }
    resp = client.patch("/user/?user_id=123", data=json.dumps(user_data_updated))
    assert resp.status_code == 422
    data_from_response = resp.json()
    assert data_from_response == {
        "detail": [
            {
                "loc": ["query", "user_id"],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid",
            }
        ]
    }
