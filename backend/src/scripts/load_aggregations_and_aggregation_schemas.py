import json
from pathlib import Path

AGGREGATIONS_DIR = (
    Path(__file__).parent.parent.parent.parent / "data" / "static" / "aggregations"
)
AGGREGATIONS_PATH = AGGREGATIONS_DIR / "aggregations.json"
AGGREGATIONS_SCHEMAS_PATH = AGGREGATIONS_DIR / "aggregation_schemas.json"


def load_json(path: Path) -> list[dict[str, str | int | bool | None]]:
    with open(file=path, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_aggregations_data() -> list[dict[str, str | int | None]]:
    aggregations_data = load_json(AGGREGATIONS_PATH)
    return aggregations_data


def get_aggregation_schemas_data() -> list[dict[str, str | int | None]]:
    aggregation_schemas_data = load_json(AGGREGATIONS_SCHEMAS_PATH)
    return aggregation_schemas_data
