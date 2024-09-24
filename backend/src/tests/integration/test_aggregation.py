import json
from pathlib import Path
from uuid import UUID

import pandas as pd
import pytest

SOURCE_PATH = Path(__file__).parent.parent.parent.parent.parent
AGGREGATION_RAW_PATH = SOURCE_PATH / "data" / "raw" / "aggregations.xlsx"
AGGREGATION_SCHEMAS_PATH = SOURCE_PATH / "data" / "raw" / "aggregation_schemas.xlsx"
SCHEMAS_OUTPUT_PATH = SOURCE_PATH / "data" / "static" / "aggregations"


def load_json(file_path: str) -> dict:
    with open(file=file_path, mode="r", encoding="utf8") as f:
        return json.load(f)


def is_float(id):
    try:
        float(id)
        return True
    except (ValueError, TypeError):
        return False


def is_str(
    name,
    schema_id,
    description,
    aggregation_variable_id,
    group_variable_1_id,
    group_variable_2_id,
    source,
):
    try:
        str(name)
        str(schema_id)
        str(description)
        str(aggregation_variable_id)
        str(group_variable_1_id)
        str(group_variable_2_id)
        str(source)
        return True
    except (ValueError, TypeError):
        return False


def is_str_schemas(id, description, aggegration_type):
    try:
        str(id)
        str(description)
        str(aggegration_type)
        return True
    except (ValueError, TypeError):
        return False


def is_bool(is_distinct):
    try:
        bool(is_distinct)
        return True
    except (ValueError, TypeError):
        return False


def is_dict(filter):
    try:
        dict(filter)
        return True
    except (ValueError, TypeError):
        return False


def is_uuid(id):
    try:
        UUID(id)
        return True
    except (ValueError, TypeError):
        return False


@pytest.fixture
def aggregations(scope="module"):
    schema = pd.read_excel(
        io=AGGREGATION_RAW_PATH,
    )
    parsed_schema = load_json(file_path=SCHEMAS_OUTPUT_PATH / "aggregations.json")
    return {
        "schema": schema,
        "parsed_schema": parsed_schema,
    }


@pytest.fixture
def aggregation_schemas(scope="module"):
    schema = pd.read_excel(
        io=AGGREGATION_SCHEMAS_PATH,
    )
    parsed_schema = load_json(
        file_path=SCHEMAS_OUTPUT_PATH / "aggregation_schemas.json"
    )
    return {
        "schema": schema,
        "parsed_schema": parsed_schema,
    }


def test_row_count_aggregations(aggregations):
    number_of_rows_parsed_schema = 0
    for variable in aggregations["parsed_schema"]:
        number_of_rows_parsed_schema += 1
    assert len(aggregations["schema"]) == number_of_rows_parsed_schema


def test_row_count_aggregation_schemas(aggregation_schemas):
    number_of_rows_parsed_schema = 0
    for variable in aggregation_schemas["parsed_schema"]:
        if variable["filter"] is not None:
            filter = variable["filter"]
            if filter["conditions"] is not None:
                number_of_rows_parsed_schema += len(filter["conditions"])
        else:
            number_of_rows_parsed_schema += 1
    assert len(aggregation_schemas["schema"]) == number_of_rows_parsed_schema


def test_type_aggregations(aggregations):
    for variable in aggregations["parsed_schema"]:
        id = variable["id"]
        schema_id = variable["schema_id"]
        aggregation_name = variable["name"]
        description = variable["description"]
        study_variable = variable["aggregation_variable_id"]
        group_variable_1 = variable["group_variable_1_id"]
        group_variable_2 = variable["group_variable_2_id"]
        source = variable["source"]
        assert is_float(id)
        assert is_str(
            name=aggregation_name,
            schema_id=schema_id,
            description=description,
            aggregation_variable_id=study_variable,
            group_variable_1_id=group_variable_1,
            group_variable_2_id=group_variable_2,
            source=source,
        )


def test_type_aggregation_schemas(aggregation_schemas):
    for variable in aggregation_schemas["parsed_schema"]:
        id = variable["id"]
        description = variable["description"]
        aggregation_type = variable["aggregation_type"]
        is_distinct = variable["is_distinct"]
        filter = variable["filter"]

        assert isinstance(id, str)
        assert isinstance(description, (str, type(None)))
        assert isinstance(aggregation_type, (str, type(None)))
        assert isinstance(is_distinct, (bool, type(None)))
        assert isinstance(filter, (dict, type(None)))


def test_id_aggregations(aggregations):
    for variable in aggregations["parsed_schema"]:
        id = variable["id"]
        aggregation_name = variable["name"]
        matching_ids = []
        for index, row in aggregations["schema"].iterrows():
            if row["name"] == aggregation_name:
                formatted_row_id = "{:.2f}".format(row["id"])
                matching_ids.append(formatted_row_id)
        assert id in matching_ids


def test_schema_id_aggregation(aggregation_schemas, aggregations):
    valid_schema_ids = set(aggregation_schemas["schema"]["id"])
    for variable in aggregations["parsed_schema"]:
        schema_id = variable["schema_id"]
        assert schema_id in valid_schema_ids


def test_variable_name_aggregations(aggregations):
    aggregation_names_parsed_schema = set(
        [agg["name"] for agg in aggregations["parsed_schema"]]
    )
    variable_names_structure = set(list(aggregations["schema"]["name"]))
    assert aggregation_names_parsed_schema == variable_names_structure


def test_variable_name_aggregation_schemas(aggregation_schemas):
    aggregation_names_parsed_schema = set(
        [agg["description"] for agg in aggregation_schemas["parsed_schema"]]
    )
    variable_names_structure = set(list(aggregation_schemas["schema"]["description"]))
    assert aggregation_names_parsed_schema == variable_names_structure


def test_multiple_aggregations(aggregations):
    for agg in aggregations["parsed_schema"]:
        if (
            agg["group_variable_2_id"] is not None
            and agg["group_variable_1_id"] is not None
        ):
            id = agg["id"]
            if id[-2:] == "00":
                continue
            group_variable_1 = agg["group_variable_1_id"]
            group_variable_2 = agg["group_variable_2_id"]
            end1 = group_variable_1[-2:]
            end2 = group_variable_2[-2:]
            assert (
                (id[-2:] == end1)
                or (id[-2:] == end2)
                # case of one digit variable id e.g. antrag6
                or (str(id)[-2] == end1[-1])
                or (str(id)[-2] == end2[-1])
            )
