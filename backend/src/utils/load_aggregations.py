import json

SCHEMA_PATH = "./utils/schemata/raw/mock_up_aggregation_scheme_draft_.json"


def load_json(path: str) -> dict[str, list[dict[str, str | bool | dict | None]]]:
    with open(file=path, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_aggregations_data():
    schemas = load_json(SCHEMA_PATH)
    aggegrations_data = []
    for aggregation in schemas:
        aggegrations_data.append(
            {
                "id": aggregation["id"],
                "schema_id": aggregation["schema_id"],
                "name": aggregation["name"],
                "description": aggregation["description_aggregation"],
                "aggregation_variable_id": aggregation["aggregation_variable_id"],
                "group_variable_1_id": aggregation["grouping_variable_1_id"],
                "group_variable_2_id": aggregation["grouping_variable_2_id"],
                "source": aggregation["source"],
            }
        )
    return aggegrations_data


def get_aggregations_schemas():
    schemas = load_json(SCHEMA_PATH)
    aggregation_schemas_data_dict = {}
    for aggegration in schemas:
        if aggregation_schemas_data_dict.get(aggegration["schema_id"]) is None:
            aggregation_schemas_data_dict["schema_id"] = {
                "id": aggegration["schema_id"],
                "description": aggegration["description_scheme"],
                "filter": aggegration["filter"],
                "is_distinct": aggegration["is_distinct"],
                "aggregation_type": aggegration["aggregation_type"],
            }
    aggregation_schemas_data = list(aggregation_schemas_data_dict.values())
    return aggregation_schemas_data
