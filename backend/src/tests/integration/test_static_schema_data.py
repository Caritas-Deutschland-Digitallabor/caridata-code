import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

SOURCE_PATH = Path(__file__).parent.parent.parent.parent.parent

SCHEMA_DEFINITION_PATH = (
    SOURCE_PATH
    / "data"
    / "raw"
    / "Schnittstellendefinition_der_GSDA_stand_2023__1_.xlsx"
)

PARSED_SCHEMATA_PATH = SOURCE_PATH / "data" / "static" / "schemas"


def load_json(file_path: str) -> dict:
    with open(file=file_path, mode="r", encoding="utf8") as f:
        return json.load(f)


def is_integer(value_from, value_to):
    try:
        int(value_from)
        int(value_to)
        return True
    except (ValueError, TypeError):
        return False


def is_float(value_from, value_to):
    try:
        float(value_from)
        float(value_to)
        return True
    except (ValueError, TypeError):
        return False


def is_date(value_from, value_to):
    try:
        datetime.strptime(value_from, "%d.%m.%Y")
        datetime.strptime(value_to, "%d.%m.%Y")
        return True
    except (ValueError, TypeError):
        return False


@pytest.fixture
def SBKERN1_Inhalte(scope="module"):
    schema = pd.read_excel(
        io=SCHEMA_DEFINITION_PATH,
        sheet_name="SBKERN1_Inhalte",
    )
    parsed_schema = load_json(file_path=PARSED_SCHEMATA_PATH / "SBKERN1_Inhalte.json")
    schema_structure = pd.read_excel(
        io=SCHEMA_DEFINITION_PATH,
        sheet_name="SBKERN1_Struktur",
    )
    return {
        "schema": schema,
        "parsed_schema": parsed_schema,
        "schema_structure": schema_structure,
    }


@pytest.fixture
def SBKERN2_Inhalte(scope="module"):
    schema = pd.read_excel(
        io=SCHEMA_DEFINITION_PATH,
        sheet_name="SBKERN2_Inhalte",
    )
    parsed_schema = load_json(file_path=PARSED_SCHEMATA_PATH / "SBKERN2_Inhalte.json")
    schema_structure = pd.read_excel(
        io=SCHEMA_DEFINITION_PATH,
        sheet_name="SBKERN2_Struktur",
    )
    return {
        "schema": schema,
        "parsed_schema": parsed_schema,
        "schema_structure": schema_structure,
    }


@pytest.fixture
def SBKONT(scope="module"):
    schema = pd.read_excel(
        io=SCHEMA_DEFINITION_PATH,
        sheet_name="SBKONT",
    )
    parsed_schema = load_json(file_path=PARSED_SCHEMATA_PATH / "SBKONT.json")
    return {
        "schema": schema,
        "parsed_schema": parsed_schema,
    }


@pytest.fixture
def SBVERAN(scope="module"):
    schema = pd.read_excel(
        io=SCHEMA_DEFINITION_PATH,
        sheet_name="SBVERAN",
    )
    parsed_schema = load_json(file_path=PARSED_SCHEMATA_PATH / "SBVERAN.json")
    schema_structure = pd.read_excel(
        io=SCHEMA_DEFINITION_PATH,
        sheet_name="SBVERAN_Struktur",
    )
    return {
        "schema": schema,
        "parsed_schema": parsed_schema,
        "schema_structure": schema_structure,
    }


@pytest.fixture
def STELLE(scope="module"):
    schema = pd.read_excel(
        io=SCHEMA_DEFINITION_PATH,
        sheet_name="STELLE",
    )
    parsed_schema = load_json(file_path=PARSED_SCHEMATA_PATH / "STELLE.json")
    schema_structure = pd.read_excel(
        io=SCHEMA_DEFINITION_PATH,
        sheet_name="STELLE_Struktur",
    )
    return {
        "schema": schema,
        "parsed_schema": parsed_schema,
        "schema_structure": schema_structure,
    }


def test_row_count_SBVERAN(SBVERAN):
    number_of_rows_parsed_schema = 0
    for variable in SBVERAN["parsed_schema"]:
        number_of_rows_parsed_schema += 1
        if "categories" in variable and variable["categories"] is not None:
            number_of_rows_parsed_schema += len(variable["categories"]) - 1
    assert len(SBVERAN["schema"]) == number_of_rows_parsed_schema


def test_row_count_SBKERN1_Inhalte(SBKERN1_Inhalte):
    number_of_rows_parsed_schema = 0
    for variable in SBKERN1_Inhalte["parsed_schema"]:
        number_of_rows_parsed_schema += 1
        if "categories" in variable and variable["categories"] is not None:
            number_of_rows_parsed_schema += len(variable["categories"]) - 1
    assert len(SBKERN1_Inhalte["schema"]) == number_of_rows_parsed_schema


def test_row_count_SBKERN2_Inhalte(SBKERN2_Inhalte):
    number_of_rows_parsed_schema = 0
    for variable in SBKERN2_Inhalte["parsed_schema"]:
        number_of_rows_parsed_schema += 1
        if "categories" in variable and variable["categories"] is not None:
            number_of_rows_parsed_schema += len(variable["categories"]) - 1
    assert len(SBKERN2_Inhalte["schema"]) == number_of_rows_parsed_schema


def test_row_count_SBKONT(SBKONT):
    number_of_rows_parsed_schema = 0
    for variable in SBKONT["parsed_schema"]:
        number_of_rows_parsed_schema += 1
        if "categories" in variable and variable["categories"] is not None:
            number_of_rows_parsed_schema += len(variable["categories"]) - 1
    assert len(SBKONT["schema"]) == number_of_rows_parsed_schema


def test_row_count_STELLE(STELLE):
    number_of_rows_parsed_schema = 0
    for variable in STELLE["parsed_schema"]:
        number_of_rows_parsed_schema += 1
        if "categories" in variable and variable["categories"] is not None:
            number_of_rows_parsed_schema += len(variable["categories"]) - 1
    assert len(STELLE["schema"]) == number_of_rows_parsed_schema


def test_position_STELLE(SBVERAN):
    for variable in SBVERAN["parsed_schema"]:
        position = variable["position"]
        variable_name = variable["variable_name"]
        assert position == SBVERAN["schema_structure"][variable_name].iloc[0]


def test_position_SBKERN1_Inhalte(SBKERN1_Inhalte):
    for variable in SBKERN1_Inhalte["parsed_schema"]:
        position = variable["position"]
        variable_name = variable["variable_name"]
        if variable_name == "berfor03":
            assert position == 122
        elif variable_name == "berfor04":
            assert position == 123
        else:
            assert (
                position == SBKERN1_Inhalte["schema_structure"][variable_name].iloc[0]
            )


def test_position_SBKERN2_Inhalte(SBKERN2_Inhalte):
    for variable in SBKERN2_Inhalte["parsed_schema"]:
        position = variable["position"]
        variable_name = variable["variable_name"]
        if variable_name == "ekspav07":
            assert position == 57
        elif variable_name == "bundesausw":
            assert position == 149
        else:
            assert (
                position == SBKERN2_Inhalte["schema_structure"][variable_name].iloc[0]
            )


def test_position_SBVERAN(SBVERAN):
    for variable in SBVERAN["parsed_schema"]:
        position = variable["position"]
        variable_name = variable["variable_name"]
        assert position == SBVERAN["schema_structure"][variable_name].iloc[0]


def test_position_SBKONT(SBKONT):
    positions = []
    for variable in SBKONT["parsed_schema"]:
        positions.append(int(variable["position"]))
    # check if it counts from 1 to n
    assert positions == list(range(1, 25))


def test_variable_name_extracted_SBKERN_1_Inhalte(SBKERN1_Inhalte):
    variable_names_parsed_schema = set(
        [variable["variable_name"] for variable in SBKERN1_Inhalte["parsed_schema"]]
    )
    variable_names_parsed_schema.remove("berfor03")
    variable_names_parsed_schema.remove("berfor04")
    variable_names_structure = set(list(SBKERN1_Inhalte["schema_structure"].columns))
    variable_names_structure.remove("Variable")
    variable_names_structure.remove("befor03")
    variable_names_structure.remove("befor04")
    assert variable_names_parsed_schema == variable_names_structure


def test_variable_name_extracted_SBKERN_2_Inhalte(SBKERN2_Inhalte):
    variable_names_parsed_schema = set(
        [variable["variable_name"] for variable in SBKERN2_Inhalte["parsed_schema"]]
    )
    variable_names_parsed_schema.remove("ekspav07")
    variable_names_parsed_schema.remove("bundesausw")
    variable_names_structure = set(list(SBKERN2_Inhalte["schema_structure"].columns))
    variable_names_structure.remove("beraform")
    variable_names_structure.remove("Variable")
    variable_names_structure.remove("ekspa07")
    variable_names_structure.remove("bundausw")
    assert variable_names_parsed_schema == variable_names_structure


def test_variable_name_extracted_SBVERAN(SBVERAN):
    variable_names_parsed_schema = set(
        [variable["variable_name"] for variable in SBVERAN["parsed_schema"]]
    )
    variable_names_structure = set(list(SBVERAN["schema_structure"].columns))
    variable_names_structure.remove("Variable")
    assert variable_names_parsed_schema == variable_names_structure


def test_variable_name_extracted_STELLE(STELLE):
    variable_names_parsed_schema = set(
        [variable["variable_name"] for variable in STELLE["parsed_schema"]]
    )
    variable_names_structure = set(list(STELLE["schema_structure"].columns))
    variable_names_structure.remove("Variable")
    assert variable_names_parsed_schema == variable_names_structure


def test_category_value_type_SBKERN1_Inhalte(SBKERN1_Inhalte):
    for variable in SBKERN1_Inhalte["parsed_schema"]:
        if variable["variable_name"] in ["fallnr", "betrnr"]:
            continue
        if "categories" in variable and variable["categories"] is not None:
            assert variable["value_type"] == "categorical"
        else:
            value_from = variable["value_from"]
            value_to = variable["value_to"]
            if is_integer(value_from, value_to):
                assert variable["value_type"] == "integer"
            elif is_float(value_from, value_to):
                assert variable["value_type"] == "float"
            elif is_date(value_from, value_to):
                assert variable["value_type"] == "date"
            else:
                assert variable["value_type"] in {"string", "boolean", "integer"}


def test_category_value_type_SBKERN2_Inhalte(SBKERN2_Inhalte):
    for variable in SBKERN2_Inhalte["parsed_schema"]:
        if variable["variable_name"] in ["fallnr", "betrnr"]:
            continue
        if "categories" in variable and variable["categories"] is not None:
            assert variable["value_type"] == "categorical"
        else:
            value_from = variable["value_from"]
            value_to = variable["value_to"]
            if is_integer(value_from, value_to):
                assert variable["value_type"] == "integer"
            elif is_float(value_from, value_to):
                assert variable["value_type"] == "float"
            elif is_date(value_from, value_to):
                assert variable["value_type"] == "date"
            else:
                assert variable["value_type"] in {"string", "boolean", "integer"}


def test_category_value_type_STELLE(STELLE):
    for variable in STELLE["parsed_schema"]:
        if variable["variable_name"] in ["fallnr", "betrnr"]:
            continue
        if "categories" in variable and variable["categories"] is not None:
            assert variable["value_type"] == "categorical"
        else:
            value_from = variable["value_from"]
            value_to = variable["value_to"]
            if is_integer(value_from, value_to):
                assert variable["value_type"] == "integer"
            elif is_float(value_from, value_to):
                assert variable["value_type"] == "float"
            elif is_date(value_from, value_to):
                assert variable["value_type"] == "date"
            else:
                assert variable["value_type"] in {"string", "boolean", "integer"}


def test_category_value_type_SBVERAN(SBVERAN):
    for variable in SBVERAN["parsed_schema"]:
        if variable["variable_name"] in ["fallnr", "betrnr"]:
            continue
        if "categories" in variable and variable["categories"] is not None:
            assert variable["value_type"] == "categorical"
        else:
            value_from = variable["value_from"]
            value_to = variable["value_to"]
            if is_integer(value_from, value_to):
                assert variable["value_type"] == "integer"
            elif is_float(value_from, value_to):
                assert variable["value_type"] == "float"
            elif is_date(value_from, value_to):
                assert variable["value_type"] == "date"
            else:
                assert variable["value_type"] in {"string", "boolean", "integer"}
