import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.asyncio
async def test_get_happy_path_without_parameters(test_client: AsyncClient) -> None:
    response = await test_client.get("/aggregations/", params={})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 209
    assert "id" in response_data[0]
    assert "name" in response_data[0]
    assert "schema_id" in response_data[0]
    assert "source" in response_data[0]
    assert "description_aggregation" in response_data[0]
    assert "description_schema" in response_data[0]
    assert "aggregation_variable_id" in response_data[0]
    assert "aggregation_variable_name" in response_data[0]
    assert "grouping_variable_1_id" in response_data[0]
    assert "grouping_variable_2_id" in response_data[0]
    assert "is_distinct" in response_data[0]
    assert "aggregation_type" in response_data[0]
    assert "filter" in response_data[0]
    if response_data[0]["filter"] is not None:
        assert "operator" in response_data[0]["filter"]
        assert "conditions" in response_data[0]["filter"]
        assert response_data[0]["filter"]["conditions"] is not None
        conditions = response_data[0]["filter"]["conditions"]
        assert "field" in conditions[0]
        assert "condition" in conditions[0]
        assert "value" in conditions[0]


@pytest.mark.asyncio
async def test_get_happy_path_with_both_parameters(test_client: AsyncClient) -> None:
    response = await test_client.get(
        "/aggregations/",
        params={
            "schema_id": "a572ccb3-540c-4e3b-bda3-11fd1223342d",
            "source": "sbkern1",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 80
    assert "id" in response_data[0]
    assert "name" in response_data[0]
    assert "schema_id" in response_data[0]
    assert "source" in response_data[0]
    assert "description_aggregation" in response_data[0]
    assert "description_schema" in response_data[0]
    assert "aggregation_variable_id" in response_data[0]
    assert "aggregation_variable_name" in response_data[0]
    assert "grouping_variable_1_id" in response_data[0]
    assert "grouping_variable_2_id" in response_data[0]
    assert "is_distinct" in response_data[0]
    assert "aggregation_type" in response_data[0]
    assert "filter" in response_data[0]
    if response_data[0]["filter"] is not None:
        assert "operator" in response_data[0]["filter"]
        assert "conditions" in response_data[0]["filter"]
        assert response_data[0]["filter"]["conditions"] is not None
        conditions = response_data[0]["filter"]["conditions"]
        assert "field" in conditions[0]
        assert "condition" in conditions[0]
        assert "value" in conditions[0]


@pytest.mark.asyncio
async def test_get_happy_path_with_schema_id(test_client: AsyncClient) -> None:
    response = await test_client.get(
        "/aggregations/", params={"schema_id": "a572ccb3-540c-4e3b-bda3-11fd1223342d"}
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 81
    assert "id" in response_data[0]
    assert "name" in response_data[0]
    assert "schema_id" in response_data[0]
    assert "source" in response_data[0]
    assert "description_aggregation" in response_data[0]
    assert "description_schema" in response_data[0]
    assert "aggregation_variable_id" in response_data[0]
    assert "aggregation_variable_name" in response_data[0]
    assert "grouping_variable_1_id" in response_data[0]
    assert "grouping_variable_2_id" in response_data[0]
    assert "is_distinct" in response_data[0]
    assert "aggregation_type" in response_data[0]
    assert "filter" in response_data[0]
    if response_data[0]["filter"] is not None:
        assert "operator" in response_data[0]["filter"]
        assert "conditions" in response_data[0]["filter"]
        assert response_data[0]["filter"]["conditions"] is not None
        conditions = response_data[0]["filter"]["conditions"]
        assert "field" in conditions[0]
        assert "condition" in conditions[0]
        assert "value" in conditions[0]


@pytest.mark.asyncio
async def test_get_happy_path_with_source(test_client: AsyncClient) -> None:
    response = await test_client.get("/aggregations/", params={"source": "sbkern1"})
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 207
    assert "id" in response_data[0]
    assert "name" in response_data[0]
    assert "schema_id" in response_data[0]
    assert "source" in response_data[0]
    assert "description_aggregation" in response_data[0]
    assert "description_schema" in response_data[0]
    assert "aggregation_variable_id" in response_data[0]
    assert "aggregation_variable_name" in response_data[0]
    assert "grouping_variable_1_id" in response_data[0]
    assert "grouping_variable_2_id" in response_data[0]
    assert "is_distinct" in response_data[0]
    assert "aggregation_type" in response_data[0]
    assert "filter" in response_data[0]
    if response_data[0]["filter"] is not None:
        assert "operator" in response_data[0]["filter"]
        assert "conditions" in response_data[0]["filter"]
        assert response_data[0]["filter"]["conditions"] is not None
        conditions = response_data[0]["filter"]["conditions"]
        assert "field" in conditions[0]
        assert "condition" in conditions[0]
        assert "value" in conditions[0]


@pytest.mark.asyncio
async def test_correct_output_of_one_aggregation(test_client: AsyncClient) -> None:
    response = await test_client.get(
        "/aggregations/",
        params={
            "schema_id": "a572ccb3-540c-4e3b-bda3-11fd1223342d",
            "source": "sbkern2",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["id"] == "8.00"
    assert response_data[0]["name"] == "Digitale Beratung"
    assert response_data[0]["schema_id"] == "a572ccb3-540c-4e3b-bda3-11fd1223342d"
    assert response_data[0]["source"] == "sbkern2"
    assert (
        response_data[0]["description_aggregation"]
        == "Anzahl der eindeutigen Fallnummern fallnr (gefiltert nach der ersten Episode betrnr = 1) gruppiert nach der Variable Online Beratung - Chat (online1) und der Variable Online Beratung - Mail (online2)."
    )
    assert response_data[0]["aggregation_variable_id"] == "fallnr_sbkern2"
    assert response_data[0]["aggregation_variable_name"] == "fallnr"
    assert response_data[0]["grouping_variable_1_id"] == "online1"
    assert response_data[0]["grouping_variable_2_id"] == "online2"
    assert (
        response_data[0]["description_schema"]
        == "Count gefiltert nach Episodennummer 1 und distinct"
    )
    assert response_data[0]["filter"] == {
        "operator": None,
        "conditions": [{"field": "betrnr", "condition": "=", "value": "1"}],
    }
    assert response_data[0]["is_distinct"] is True
    assert response_data[0]["aggregation_type"] == "COUNT"
