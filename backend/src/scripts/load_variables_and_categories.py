import json
from glob import glob
from pathlib import Path

# get paths from file backend/src/utils/schemata
SCHEMA_DIR = Path(__file__).parent.parent.parent.parent / "data" / "static" / "schemas"
print(SCHEMA_DIR)

SCHEMA_PATHS = glob(str(SCHEMA_DIR / "*.json"))


def load_json(path: str) -> list[dict[str, str | int | bool | None]]:
    with open(file=path, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def read_schemas() -> dict[str, list[dict[str, str | int | bool | None]]]:
    schemas = {}
    for path in SCHEMA_PATHS:
        source = path.split("/")[-1].split("_")[0].lower()
        schema = load_json(path)
        schemas[source] = schema
    return schemas


def get_variables_data() -> list[dict[str, str | int | None]]:
    schemas = read_schemas()
    variables_data = []
    for source, schema in schemas.items():
        for variable in schema:
            if variable["variable_name"] in ["tsnr", "fallnr", "lzrnr", "betrnr"]:
                variable_name = (
                    str(variable["variable_name"]) + "_" + str(variable["source"])
                )
            else:
                variable_name = str(variable["variable_name"])
            variables_data.append(
                {
                    "id": variable_name,
                    "name": variable["variable_name"],
                    "source": variable["source"],
                    "text": variable["variable_text"],
                    "type": variable["value_type"],
                    "value_from": str(variable["value_from"]),
                    "value_to": str(variable["value_to"]),
                    "mandatory": variable["mandatory"],
                    "file_position": variable["position"],
                    "missing": variable["missing"],
                    "technical_mandatory": variable["technical_mandatory"],
                }
            )
    return variables_data


def get_categories_data() -> list[dict[str, str | int | bool]]:
    schemas = read_schemas()
    categories_data = []
    for source, schema in schemas.items():
        for variable in schema:
            if variable["variable_name"] in ["tsnr", "fallnr", "lzrnr", "betrnr"]:
                variable_name = str(variable["variable_name"]) + "_" + str(source)
            else:
                variable_name = str(variable["variable_name"])
            if "categories" in variable and variable["categories"] is not None:
                for category in variable["categories"]:  # type: ignore
                    category_text = (
                        "keine_angabe" if category["text"] is None else category["text"]  # type: ignore
                    )
                    categories_data.append(
                        {
                            "id": str(variable_name)
                            + "_"
                            + str(category_text.lower().replace(" ", "_")),
                            "variable_id": variable_name,
                            "value": category["value"],  # type: ignore
                            "name": category["text"],  # type: ignore
                        }  # type: ignore
                    )
    return categories_data


if __name__ == "__main__":
    print(get_variables_data())
    print(get_categories_data())
