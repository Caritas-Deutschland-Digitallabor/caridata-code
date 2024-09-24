import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_get_happy_path_without_parameters(test_client: AsyncClient) -> None:
    response = await test_client.get("/variables/", params={})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 460
    assert "id" in response_data[0]
    assert "name" in response_data[0]
    assert "source" in response_data[0]
    assert "text" in response_data[0]
    assert "type" in response_data[0]
    assert "value_from" in response_data[0]
    assert "value_to" in response_data[0]
    assert "mandatory" in response_data[0]
    assert "file_position" in response_data[0]
    assert "missing" in response_data[0]
    assert "created_at" in response_data[0]
    assert "deprecated_at" in response_data[0]
    assert "categories" in response_data[0]
    assert "technical_mandatory" in response_data[0]


@pytest.mark.asyncio
async def test_get_happy_path_with_both_parameters(test_client: AsyncClient) -> None:
    response = await test_client.get(
        "/variables/", params={"variable_name": "anonym1", "source": "sbkern1"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 1
    assert "id" in response_data[0]
    assert "name" in response_data[0]
    assert "source" in response_data[0]
    assert "text" in response_data[0]
    assert "type" in response_data[0]
    assert "value_from" in response_data[0]
    assert "value_to" in response_data[0]
    assert "mandatory" in response_data[0]
    assert "file_position" in response_data[0]
    assert "missing" in response_data[0]
    assert "created_at" in response_data[0]
    assert "deprecated_at" in response_data[0]
    assert "categories" in response_data[0]
    assert "technical_mandatory" in response_data[0]


@pytest.mark.asyncio
async def test_get_happy_path_with_variable_name(test_client: AsyncClient) -> None:
    response = await test_client.get("/variables/", params={"variable_name": "anonym1"})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 1
    assert "id" in response_data[0]
    assert "name" in response_data[0]
    assert "source" in response_data[0]
    assert "text" in response_data[0]
    assert "type" in response_data[0]
    assert "value_from" in response_data[0]
    assert "value_to" in response_data[0]
    assert "mandatory" in response_data[0]
    assert "file_position" in response_data[0]
    assert "missing" in response_data[0]
    assert "created_at" in response_data[0]
    assert "deprecated_at" in response_data[0]
    assert "categories" in response_data[0]
    assert "technical_mandatory" in response_data[0]


@pytest.mark.asyncio
async def test_get_happy_path_with_variable_name_duplicate(
    test_client: AsyncClient,
) -> None:
    response = await test_client.get("/variables/", params={"variable_name": "tsnr"})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 5
    assert "id" in response_data[0]
    assert "name" in response_data[0]
    assert "source" in response_data[0]
    assert "text" in response_data[0]
    assert "type" in response_data[0]
    assert "value_from" in response_data[0]
    assert "value_to" in response_data[0]
    assert "mandatory" in response_data[0]
    assert "file_position" in response_data[0]
    assert "missing" in response_data[0]
    assert "created_at" in response_data[0]
    assert "deprecated_at" in response_data[0]
    assert "categories" in response_data[0]
    assert "technical_mandatory" in response_data[0]


@pytest.mark.asyncio
async def test_get_happy_path_with_source(test_client: AsyncClient) -> None:
    response = await test_client.get("/variables/", params={"source": "sbkern1"})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 202
    assert "id" in response_data[0]
    assert "name" in response_data[0]
    assert "source" in response_data[0]
    assert "text" in response_data[0]
    assert "type" in response_data[0]
    assert "value_from" in response_data[0]
    assert "value_to" in response_data[0]
    assert "mandatory" in response_data[0]
    assert "file_position" in response_data[0]
    assert "missing" in response_data[0]
    assert "created_at" in response_data[0]
    assert "deprecated_at" in response_data[0]
    assert "categories" in response_data[0]
    assert "technical_mandatory" in response_data[0]


@pytest.mark.asyncio
async def test_categories_none(test_client: AsyncClient) -> None:
    response = await test_client.get(
        "/variables/", params={"variable_name": "kinalte2", "source": "sbkern1"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data[0]["categories"] is None


@pytest.mark.asyncio
async def test_categories_exists(test_client: AsyncClient) -> None:
    response = await test_client.get(
        "/variables/", params={"variable_name": "anonym1", "source": "sbkern1"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data[0]["categories"] is not None
    categories = response_data[0]["categories"]
    assert len(categories) == 3
    assert "name" in categories[0]
    assert "value" in categories[0]


@pytest.mark.asyncio
async def test_correct_output_of_one_schema(test_client: AsyncClient) -> None:
    response = await test_client.get(
        "/variables/", params={"variable_name": "eksklb01", "source": "sbkern1"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data[0]["id"] == "eksklb01"
    assert response_data[0]["name"] == "eksklb01"
    assert response_data[0]["source"] == "sbkern1"
    assert (
        response_data[0]["text"]
        == "Einkommensart Klient/in (Beginn) - Erwerbstätigkeit (unselbständig)"
    )
    assert response_data[0]["type"] == "categorical"
    assert response_data[0]["value_from"] == "None"
    assert response_data[0]["value_to"] == "None"
    assert response_data[0]["technical_mandatory"] is False
    assert response_data[0]["mandatory"] is True
    assert response_data[0]["file_position"] == 40
    assert response_data[0]["missing"] is None
    assert response_data[0]["created_at"] is not None
    assert response_data[0]["deprecated_at"] is None
    assert response_data[0]["categories"] is not None
    categories = response_data[0]["categories"]
    assert len(categories) == 3
    assert categories[0]["name"] == "keine Angaben"
    assert categories[0]["value"] == "0"
