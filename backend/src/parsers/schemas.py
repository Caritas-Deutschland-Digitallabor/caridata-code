import json
import pathlib

import pandas as pd

from utils.schemas_color_mapper import map_colors

SOURCE_PATH = pathlib.Path(__file__).parent.parent.parent.parent

SCHEMAS_RAW_DATA_PATH = (
    SOURCE_PATH
    / "data"
    / "raw"
    / "Schnittstellendefinition_der_GSDA_stand_2023__1_.xlsx"
)

SCHEMAS_OUTPUT_PATH = SOURCE_PATH / "data" / "static" / "schemas"


def read_excel(schema_name: str) -> pd.DataFrame:
    """
    Read the excel file and return the DataFrame

    Parameters:
    ----------
    path : str
        The path to the excel file
    sheet_name : str
        The name of the sheet to be read
    Returns:
    -------
    df : pd.DataFrame
        The DataFrame
    """
    df = pd.read_excel(SCHEMAS_RAW_DATA_PATH, sheet_name=schema_name)
    df = df.rename(str.strip, axis=1)
    return df


def get_position(row: pd.core.series.Series) -> int | None:
    """
    Get the position of the columns in the DataFrame

    Parameters:
    ----------
    df : pd.DataFrame
        The DataFrame
    Returns:
    -------
    position : dict[str, int]
        The position of the columns
    """
    try:
        return int(row["Position"])
    except (ValueError, TypeError):
        return None


def get_variable_name(row: pd.core.series.Series) -> str:
    """
    Get the variable name from the row

    Parameters:
    ----------
    row : pd.core.series.Series
        The row of the DataFrame
    Returns:
    -------
    variable_name : str
        The variable name
    """
    return str(row["Variable"]).strip()


def extract_category(current_index, schema_data) -> list[dict[str, str]]:
    """
    Extract the categories from the DataFrame

    Parameters:
    ----------
    current_index : int
        The current index of the DataFrame
    df : pd.DataFrame
        The DataFrame
    Returns:
    -------
    categories : list[dict[str, str | int]]
        The categories
    current_index : int
        The current index of the DataFrame
    """
    categories = []
    categories.append(
        {
            "value": str(schema_data.iloc[current_index]["Werte(bereich)"]),
            "text": str(schema_data.iloc[current_index]["Kategorien"]).strip(),
        }
    )
    while get_position(schema_data.iloc[current_index + 1]) is None:
        current_index += 1
        categories.append(
            {
                "value": str(schema_data.iloc[current_index]["Werte(bereich)"]),
                "text": str(schema_data.iloc[current_index]["Kategorien"]).strip(),
            }
        )
    return categories


def get_variable_text(row: pd.core.series.Series) -> str | None:
    """
    Get the variable text from the row

    Parameters:
    ----------
    row : pd.core.series.Series
        The row of the DataFrame
    Returns:
    -------
    variable_text : str
        The variable text
    """
    question = str(row["Frage"]).strip() if str(row["Frage"]).strip() != "nan" else ""
    sub_question = (
        str(row["Unterfrage"]).strip()
        if str(row["Unterfrage"]).strip() != "nan"
        else ""
    )
    if question and sub_question:
        return str(question + " - " + sub_question)
    elif question:
        return str(question)
    elif sub_question:
        return str(sub_question)
    else:
        return None


def get_value_type(row: pd.core.series.Series) -> str | None:
    """
    Get the value type from the row

    Parameters:
    ----------
    row : pd.core.series.Series
        The row of the DataFrame
    Returns:
    -------
    value_type : str
        The value type
    """
    value = row["Stellen"].strip()
    value_first_char = value[0]

    match value_first_char:
        case "N":
            if "." in value or "," in value:
                return "float"
            else:
                return "integer"
        case "C":
            return "string"
        case "D":
            return "date"
        case "L":
            return "boolean"
    return None


def get_value_range(
    row: pd.core.series.Series,
) -> tuple[str | None, str | None]:
    values = str(row["Werte(bereich)"]) if "-" in str(row["Werte(bereich)"]) else None
    if values:
        value_range = values.split("-")
        return value_range[0].strip(), value_range[1].strip()
    else:
        return (None, None)


def get_technical_mandatory(row: pd.core.series.Series) -> bool:
    """
    Get the technical mandatory from the row

    Parameters:
    ----------
    row : pd.core.series.Series
        The row of the DataFrame
    Returns:
    -------
    technical_mandatory : bool
        The technical mandatory
    """
    technical_mandatory = str(row["Bemerkungen"]).strip()
    match technical_mandatory:
        case "technisches Pflichtfeld":
            return True
        case "technisches Pflichtfeld (2-stellig wegen potenzieller Erweiterung in den Folgejahren)":
            return True
        case "technische Pflichtvariable":
            return True
    return False


def get_missing(row: pd.core.series.Series) -> str | None:
    # check if row contains missing column
    if "Missing" in row:
        return str(row["Missing"]).strip()
    else:
        missing_candidate = str(row["Bemerkungen"]).strip()
        match missing_candidate:
            case "missing = 0":
                return "0"
            case "missing = 99":
                return "99"
            case "True / False, missing = False":
                return "False"
            case "Missingwert=0":
                return "0"
            case "Missingwert = F":
                return "F"
            case "missing = 0  -  nur für Schwangere":
                return "0  -  nur für Schwangere"
    return None


def parse_schema(
    schema_data: pd.DataFrame, schema_color_mapper: dict, schema_name: str
) -> list[dict]:
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
    for idx, row in schema_data.iterrows():
        categories = []
        position = get_position(row)

        # check if row is category row
        if position is None:
            continue

        # check if variable has categories
        if idx + 1 < len(schema_data):
            next_position = get_position(schema_data.iloc[idx + 1])
            if next_position is None:
                categories = extract_category(
                    current_index=idx, schema_data=schema_data
                )

        variable_name = get_variable_name(row)
        variable_text = get_variable_text(row)

        value_type = get_value_type(row)
        value_from, value_to = get_value_range(row)

        mandatory = schema_color_mapper.get(idx, None)

        technical_mandatory = get_technical_mandatory(row)

        missing = get_missing(row)

        schema.append(
            {
                "position": position,
                "variable_name": variable_name,
                "variable_text": variable_text,
                "value_type": value_type if not categories else "categorical",
                "value_from": value_from if value_from else None,
                "value_to": value_to if value_to else None,
                "categories": categories if categories else None,
                "mandatory": mandatory,
                "technical_mandatory": technical_mandatory,
                "missing": missing,
                "source": schema_name.lower(),
            }
        )
    return schema


def correct_source_SBKERN1(schema_data: pd.DataFrame) -> pd.DataFrame:
    """
    Correct the source of the SBKERN1 schema

    Parameters:
    ----------
    schema : pd.DataFrame
        The DataFrame of the SBKERN1 schema
    Returns:
    -------
    schema : pd.DataFrame
        The corrected DataFrame
    """
    # correct position of the row 302 (position 125, expected: 135)
    schema_data.loc[302, "Position"] = 135

    # correct names of variables (befor03, befor04, expected: berfor3, berfor4)
    schema_data.loc[schema_data["Variable"] == "befor03", "Variable"] = "berfor03"
    schema_data.loc[schema_data["Variable"] == "befor04", "Variable"] = "berfor04"

    return schema_data


def correct_source_SBKERN2(schema_data: pd.DataFrame) -> pd.DataFrame:
    """
    Correct the source of the SBKERN1 schema

    Parameters:
    ----------
    schema : pd.DataFrame
        The DataFrame of the SBKERN1 schema
    Returns:
    -------
    schema : pd.DataFrame
        The corrected DataFrame
    """
    # correct names of variables (ekspa07, bundausw expected: ekspav07, bundesausw)
    schema_data.loc[schema_data["Variable"] == "ekspa07", "Variable"] = "ekspav07"
    schema_data.loc[schema_data["Variable"] == "bundausw", "Variable"] = "bundesausw"
    return schema_data


if __name__ == "__main__":
    schemas = ["SBVERAN", "SBKONT", "SBKERN2_Inhalte", "SBKERN1_Inhalte", "STELLE"]
    schema_names = ["sbveran", "sbkont", "sbkern2", "sbkern1", "stelle"]
    schemas_color_mapper = map_colors(
        schemas=[
            "SBVERAN",
            "SBKONT",
            "SBKERN2_Inhalte",
            "SBKERN1_Inhalte",
            "STELLE",
        ]
    )
    correction_functions = {
        "SBKERN1_Inhalte": correct_source_SBKERN1,
        "SBKERN2_Inhalte": correct_source_SBKERN2,
    }
    for idx, schema_name in enumerate(schemas):
        schema_data = read_excel(schema_name)
        if schema_name in correction_functions:
            schema_data = correction_functions[schema_name](schema_data=schema_data)
        schema = parse_schema(
            schema_data=schema_data,
            schema_color_mapper=schemas_color_mapper[schema_name],
            schema_name=schema_names[idx],
        )
        with open(file=SCHEMAS_OUTPUT_PATH / f"{schema_name}.json", mode="w") as f:
            json.dump(schema, f, indent=4)
