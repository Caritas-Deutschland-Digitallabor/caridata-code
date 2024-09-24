import json
import pathlib
from typing import Any, Dict, List

import pandas as pd

SOURCE_PATH = pathlib.Path(__file__).parent.parent.parent.parent
AGGREGATION_SCHEMAS_RAW_PATH = SOURCE_PATH / "data" / "raw" / "aggregation_schemas.xlsx"
SCHEMAS_OUTPUT_PATH = (
    SOURCE_PATH / "data" / "static" / "aggregations" / "aggregation_schemas.json"
)


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


def get_schema_id(row: pd.core.series.Series) -> int | None:
    """
    Get the schema id
    """
    if str(row["id"]) == "nan":
        return None
    else:
        return row["id"]


def get_description(row: pd.core.series.Series) -> str | None:
    """
    Get the description
    """
    if str(row["description"]) == "nan":
        return None
    else:
        return str(row["description"])


def extract_filter(idx: int, data: pd.DataFrame) -> Dict[str, Any] | None:
    """
    Extract the filter
    Parameters:
    ----------
    idx : int
        The current schema id, for which the filter is extracted
    data : pd.DataFrame
    -------
    filter : dict
        The filter json (suggestion from haystack)
    """

    filter: Dict[str, Any] = {
        "operator": str(data.iloc[idx]["operator"]).strip('"')
        if str(data.iloc[idx]["operator"]).strip('"') != "nan"
        else None,
        "conditions": [],
    }

    filter["conditions"].append(
        {
            "field": str(data.iloc[idx]["key"]).strip('"')
            if str(data.iloc[idx]["key"]) != "nan"
            else None,
            "condition": str(data.iloc[idx]["condition"]).strip('"')
            if str(data.iloc[idx]["condition"]) != "nan"
            else None,
            "value": str(data.iloc[idx]["value"]).strip('"')
            if str(data.iloc[idx]["value"]) != "nan"
            else None,
        }
    )

    if (
        filter["operator"] is None
        and filter["conditions"][0]["field"] is None
        and filter["conditions"][0]["condition"] is None
        and filter["conditions"][0]["value"] is None
    ):
        return None

    while idx + 1 < len(data) and get_schema_id(data.iloc[idx]) == get_schema_id(
        data.iloc[idx + 1]
    ):
        filter["conditions"].append(
            {
                "field": str(data.iloc[idx + 1]["key"]).strip('"')
                if str(data.iloc[idx + 1]["key"]) != "nan"
                else None,
                "condition": str(data.iloc[idx + 1]["condition"]).strip('"')
                if str(data.iloc[idx + 1]["condition"]) != "nan"
                else None,
                "value": str(data.iloc[idx + 1]["value"]).strip('"')
                if str(data.iloc[idx + 1]["value"]) != "nan"
                else None,
            }
        )
        idx += 1
    return filter


def get_is_disctinct(row: pd.core.series.Series) -> bool | None:
    """
    Get the is distinct
    """
    if str(row["is_distinct"]) == "nan":
        return None
    else:
        return bool(row["is_distinct"])


def get_aggregation_type(row: pd.core.series.Series) -> str | None:
    """
    Get the aggregation type
    """
    if str(row["aggregation_type"]) == "nan":
        return None
    else:
        return str(row["aggregation_type"]).strip('"')


def get_deprecated_at(row: pd.core.series.Series) -> str | None:
    """
    Get the depreciated at
    """
    if str(row["deprecated_at"]) == "nan":
        return None
    else:
        return str(row["deprecated_at"])


def parse_schema(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Parse the schema

        Parameters:
        ----------
        df : pd.DataFrame
            The DataFrame
        Returns:
        -------
        df : pd.DataFrame
            The DataFrame
    """
    schema: List[Dict[str, Any]] = []
    for idx, row in df.iterrows():
        id = get_schema_id(row)
        current_ids = [x["id"] for x in schema]
        # Check if the id is already in the schema
        if id in current_ids:
            continue

        filter = extract_filter(idx, df)
        description = get_description(row)
        is_distinct = get_is_disctinct(row)
        aggregation_type = get_aggregation_type(row)
        deprecated_at = get_deprecated_at(row)

        schema.append(
            {
                "id": id,
                "description": description,
                "filter": filter,
                "is_distinct": is_distinct,
                "aggregation_type": aggregation_type,
                "deprecated_at": deprecated_at,
            }
        )
    return schema


if __name__ == "__main__":
    df = read_excel(AGGREGATION_SCHEMAS_RAW_PATH)
    schema = parse_schema(df)
    with open(SCHEMAS_OUTPUT_PATH, "w") as f:
        json.dump(schema, f, indent=4)
