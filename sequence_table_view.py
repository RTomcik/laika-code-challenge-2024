"""
Build an HTML table view of certain query fields for Sequences.
"""
from typing import List, Any, Union
import utils.shotgrid
import shotgun_api3
from pprint import pprint

def open_sequence_table(project_id: int) -> None:
    """
    Opens up an HTML based sequence table for via a project ID.

    Args:
        project_id (int): The SG id of a project to open the table for.
    """
    sg = utils.shotgrid.get_shotgrid_python_client()
    sequences = sg.find("Sequence", filters=[["project.Project.id", "is", project_id]], fields=["code"])
    table_data = _build_table_data(sg, sequences)


def _build_table_data(sg, sequences: List[dict]) -> List[dict]:
    """
    Evalutes and structures the fields needed to render the table.

    Args:
        sg (shotgun_api3.Shotgun): The SG connection object.
        sequences (List[dict]): A list of SG sequence entity dictionaries.

    Returns:
        List[dict]: A list of dictionaries containing the necessary fields used in the table.
    """
    table_data = []
    for sequence in sequences:
        row_data = {
            "Sequence Code": sequence.get("code"),
            "ID": sequence.get("id"),
            "Average Cut Duration": _evaluate_shotgrid_query_field(sg, sequence, "sg_cut_duration"),
            "IP Versions": _evaluate_shotgrid_query_field(sg, sequence, "sg_ip_versions")
        }
        table_data.append(row_data)

    # Sort the table in order of id
    table_data.sort(key=lambda x: x.get("id"))
    pprint(table_data)
    return table_data

def _build_html(table_data: List[dict]) -> str:
    """
    Uses the evaluated table data to build HTML as a string and returns it.

    Args:
        table_data (List[dict]): The table data to render into HTML.

    Returns:
        str - The generated HTML as a string.
    """
    ...

def _evaluate_shotgrid_query_field(sg: shotgun_api3.Shotgun, query_field: str, entity: dict = None) -> Any:
    """
    Returns back the expected result from an SG Query field for a certain entity.

    Args:
        sg (shotgun_api3.Shotgun): The SG connection object.
        query_field (str): The query field name to evaluate.
        entity (dict, optional): The SG entity dictionary to replace "Current" summary options. Requires an 'id' and 'type' field. Defaults to None.

     Returns:
        Any - The evaluated query field, data structure could change depending on the query field.
    """
    field_schema = sg.schema_field_read(entity.get("type"), field_name=query_field)
    field_properties = field_schema[query_field]["properties"]
    query_data = field_properties["query"]["value"]
    entity_type = query_data["entity_type"]
    filter_schemas = query_data["filters"]
    summary_filters = [_parse_filters_from_conditions(filter_schemas, entity)]

    summary_field = field_properties["summary_field"]["value"]
    summary_type = field_properties["summary_default"]["value"]
    summary_fields_query = [{"field": summary_field, "type": summary_type}]
    summary = sg.summarize(entity_type, filters=summary_filters, summary_fields=summary_fields_query)
    return summary["summaries"][summary_field]


def _parse_filters_from_conditions(conditions_schema: Union[dict, list], entity: dict = None) -> Union[dict, list]:
    """
    Recursive function to parse out nested filter conditions from the schema.

    Args:
        conditions_schema (dict | list): A portion of the schema conditions to process into filters.
        entity (dict, optional): An entity to replace the "Current" type filter on a summary field. Defaults to None.

    Returns:
        dict | list: The processed conditions schema converted into filters that SG queries can recognize.
    """
    # If the filter is a dictionary then we need to parse what is inside of it
    if type(conditions_schema) == dict:
        # If there is a valid value, then there is filter data to be parsed
        if "values" in conditions_schema.keys():
            if conditions_schema.get("active") == "true":
                filter_values = conditions_schema["values"]

                # Parse if a filter is set to "Current X", substitute current entity if so
                replaced_filter_value = []
                for filter_value in filter_values:        
                    if type(filter_value) is dict and filter_value.get("id") == 0 and "Current " in filter_value.get("name"):
                        replaced_filter_value.append(entity)
                    else:
                        replaced_filter_value.append(filter_value)

                # SG Schema seems to include a list of filters, even for a relation value of "is"
                # If there is only one value in the list, change the filter to just be the dictionary
                if len(filter_values) == 1 and conditions_schema["relation"] == "is":
                    replaced_filter_value = replaced_filter_value[0]
                    
                return [conditions_schema["path"], conditions_schema["relation"], replaced_filter_value]
        else:
            # Value then this is a nested schema, run this function again on its conditions
            return {"filters": _parse_filters_from_conditions(conditions_schema.get("conditions"), entity), "filter_operator":conditions_schema.get("logical_operator") }
    
    # If the filter is a list, then we have to parse each element of the list and return it
    elif type(conditions_schema) == list:
        filters_list = []
        for condition in conditions_schema:
            filters_list.append(_parse_filters_from_conditions(condition, entity))
        return filters_list

if __name__ == "__main__":
    project_id = 85
    open_sequence_table(project_id)
