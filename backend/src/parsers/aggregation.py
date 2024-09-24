import json
import pathlib

import pandas as pd

SOURCE_PATH = pathlib.Path(__file__).parent.parent.parent.parent
AGGREGATION_RAW_PATH = SOURCE_PATH / "data" / "raw" / "aggregations.xlsx"
SCHEMAS_OUTPUT_PATH = SOURCE_PATH / "data" / "static" / "aggregations"


def read_excel(path: pathlib.Path) -> pd.DataFrame:
    """
    Read the excel file and return the DataFrame

    Parameters:
    ----------
    path : pathlib.Path
        The path to the excel file
    Returns:
    -------
    df : pd.DataFrame
        The DataFrame
    """
    df = pd.read_excel(path)
    return df


def get_aggregation_id(row: pd.core.series.Series) -> str | None:
    """
    Get the aggregation id
    """
    if str(row["id"]) == "nan":
        return None
    else:
        float_id = float(row["id"])
        string_id = "{:.2f}".format(float_id)
        return string_id


def get_aggregation_name(row: pd.core.series.Series) -> str | None:
    """
    Get the aggregation name
    """
    if str(row["name"]) == "nan":
        return None
    else:
        return str(row["name"])


def get_schema_id(row: pd.core.series.Series) -> str | None:
    """
    Get the schema id
    """
    if str(row["schema_id"]) == "nan":
        return None
    else:
        id_int = int(row["schema_id"])
        match id_int:
            case 1:
                id = "a572ccb3-540c-4e3b-bda3-11fd1223342d"
            case 2:
                id = "817abf54-6cbf-4da3-b447-4581aa56614d"
            case 3:
                id = "6696a1cd-4edb-4479-9b8c-943d10c42720"
            case 4:
                id = "3e75a25e-65b8-43ef-ad26-e57a3cf4f44c"
            case 5:
                id = "9ce7eca1-9b7b-4d6b-96b2-3e557ace7b45"
            case 6:
                id = "499777b8-6417-45a0-a3f9-5f00e1f4a861"
            case 7:
                id = "4427aae4-61eb-483e-9307-167d80a1cabf"
            case 8:
                id = "082d0514-9974-488c-b89f-020a65491ca3"
        return id


def get_description(row: pd.core.series.Series) -> str | None:
    """
    Get the description
    """
    if str(row["description"]) == "nan":
        return None
    else:
        return str(row["description"])


def get_study_variable(row: pd.core.series.Series) -> str | None:
    """
    Get the study variable
    """
    if row["study_variable_id"] == "nan":
        return None
    elif row["study_variable_id"] == "fallnr":
        return "fallnr" + "_" + str(row["source"])
    else:
        return str(row["study_variable_id"])


def get_group_variable_1(row: pd.core.series.Series) -> str | None:
    """
    Get the group variable 1
    """
    if str(row["group_variable_1_id"]) == "nan":
        return None
    else:
        return str(row["group_variable_1_id"])


def get_group_variable_2(row: pd.core.series.Series) -> str | None:
    """
    Get the group variable 2
    """
    if str(row["group_variable_2_id"]) == "nan":
        return None
    else:
        return str(row["group_variable_2_id"])


def get_deprecated_at(row: pd.core.series.Series) -> str | None:
    """
    Get the depreciated at
    """
    if str(row["deprecated_at"]) == "nan":
        return None
    else:
        return str(row["deprecated_at"])


def get_source(row: pd.core.series.Series) -> str | None:
    """
    Get the source
    """
    if str(row["source"]) == "nan":
        return None
    else:
        return str(row["source"])


def parse_schema(schema_data: pd.DataFrame) -> list[dict]:
    """
    Parse the df into the machine readable schema

    Parameters:
    ----------
    df : pd.DataFrame
        The DataFrame to be parsed
    Returns:
    -------
    schema : list[dict]
        The machine readable schema

    """
    schema = []
    for _, row in schema_data.iterrows():
        position = get_aggregation_id(row)
        aggregation_name = get_aggregation_name(row)
        schema_id = get_schema_id(row)
        description = get_description(row)
        study_variable = get_study_variable(row)
        group_variable_1 = get_group_variable_1(row)
        group_variable_2 = get_group_variable_2(row)
        source = get_source(row)
        deprecated_at = get_deprecated_at(row)

        schema.append(
            {
                "id": position,
                "schema_id": schema_id,
                "name": aggregation_name,
                "description": description,
                "aggregation_variable_id": study_variable,
                "group_variable_1_id": group_variable_1,
                "group_variable_2_id": group_variable_2,
                "source": source,
                "deprecated_at": deprecated_at,
            }
        )

    return schema


if __name__ == "__main__":
    df = read_excel(AGGREGATION_RAW_PATH)
    schema = parse_schema(df)
    with open(SCHEMAS_OUTPUT_PATH / "aggregations.json", "w") as f:
        json.dump(schema, f, indent=4)
